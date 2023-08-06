from configparser import ConfigParser
from contextlib import contextmanager
from copy import copy
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
from unittest.mock import ANY, patch

import pytest
from expects import expect, have_keys

from sym.cli.actions.write_creds_action import WriteCredsAction
from sym.cli.data.request_data import RequestData
from sym.cli.errors import CliError
from sym.cli.helpers.config import Config
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.tests.conftest import _env_str
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.helpers.sandbox import Sandbox

TEST_PROFILE = "foobar-9000"
TEST_RESOURCE = "test"

# mapping of keys stored in .aws/credentials to internal keys
# in the case they're different, as we change some during write_creds
CRED_KEYS_MAPPING = {
    "REGION": "AWS_REGION",
    "X_SECURITY_TOKEN_EXPIRES": "AWS_CREDENTIAL_EXPIRATION",
}


class TestWriteCreds:
    """write_creds testing suite.

    Includes tests for click commands / user interaction
    and the internal module code separately.

    This class is broken into 2 distinct parts:
        1. pytest test cases
        2. pytest fixture and data creation helper methods

    To run the tests you may, from the runtime/sym-cli project folder:
    - Run the entire test suite:
        python -m pytest sym/cli/tests/commands/test_write_creds.py

    - Run a single test method:
        python -m pytest sym/cli/tests/commands/test_write_creds.py::TestWriteCreds::test_execute_write_creds
    """

    def test_execute_write_creds(
        self, sandbox, credentials_path, creds_env, capture_command
    ):
        with self.write_creds_context_manager(capture_command, sandbox, creds_env):
            global_options = GlobalOptions(saml_client_type=AwsOkta)

            request_data = RequestData(
                action="write_creds",
                resource=TEST_RESOURCE,
                global_options=global_options,
                params={"path": str(credentials_path), "profile": TEST_PROFILE},
            )
            action = WriteCredsAction()
            action.execute(request_data)

            written_creds = self.get_credentials_from_file(credentials_path, TEST_PROFILE)
            expect(written_creds).to(have_keys(creds_env))

    def test_execute_write_creds_without_aws_okta_fails(
        self, sandbox, credentials_path, capture_command, creds_env
    ):
        with pytest.raises(CliError, match="Unable to find aws-okta in your path!"):
            with self.write_creds_context_manager(
                capture_command, sandbox, create_binary=False
            ):
                global_options = GlobalOptions(saml_client_type=AwsOkta)

                request_data = RequestData(
                    action="write_creds",
                    resource=TEST_RESOURCE,
                    global_options=global_options,
                    params={"path": str(credentials_path), "profile": TEST_PROFILE},
                )
                action = WriteCredsAction()
                action.execute(request_data)

    @patch("sym.cli.saml_clients.saml_client.SAMLClient._ensure_session")
    def test_execute_write_creds_expiring_force_ensures_session(
        self, _ensure_session, sandbox, credentials_path, capture_command, creds_env
    ):
        creds = copy(creds_env)
        creds["AWS_OKTA_SESSION_EXPIRATION"] = str(int(datetime.now().timestamp()))

        with self.write_creds_context_manager(capture_command, sandbox, creds):
            global_options = GlobalOptions(saml_client_type=AwsOkta)

            request_data = RequestData(
                action="write_creds",
                resource=TEST_RESOURCE,
                global_options=global_options,
                params={"path": str(credentials_path), "profile": TEST_PROFILE},
            )

            action = WriteCredsAction()
            action.execute(request_data)

            _ensure_session.assert_called_once_with(force=True)

            written_creds = self.get_credentials_from_file(credentials_path, TEST_PROFILE)

            # Ideally we'd like to make sure the written_creds expiration is in
            # the future, not what we set as creds["AWS_OKTA_SESSION_EXPIRATION"],
            # but since we stub the subprocess, we can't get updated creds.
            # So the real test here is _ensure_session.assert_called and this check
            # is extra.
            expect(written_creds).to(have_keys(creds))

    @patch(
        "sym.cli.saml_clients.saml_client.SAMLClient._profile_matches_caller_identity",
        return_value=False,
    )
    @patch("sym.cli.saml_clients.saml_client.SAMLClient._ensure_session")
    def test_execute_write_creds_profile_mismatch_force_ensures_session(
        self,
        _ensure_session,
        _profile_match,
        sandbox,
        credentials_path,
        capture_command,
        creds_env,
    ):
        creds = copy(creds_env)

        # _profile_matches_caller_identity doesn't get called if creds are expiring
        future_datetime = datetime.now() + timedelta(minutes=30)
        creds["AWS_OKTA_SESSION_EXPIRATION"] = str(int(future_datetime.timestamp()))

        with self.write_creds_context_manager(capture_command, sandbox, creds):
            global_options = GlobalOptions(saml_client_type=AwsOkta)

            request_data = RequestData(
                action="write_creds",
                resource=TEST_RESOURCE,
                global_options=global_options,
                params={"path": str(credentials_path), "profile": TEST_PROFILE},
            )

            action = WriteCredsAction()
            action.execute(request_data)

            _profile_match.assert_called_once()
            _ensure_session.assert_called_once_with(force=True)

            written_creds = self.get_credentials_from_file(credentials_path, TEST_PROFILE)

            expect(written_creds).to(have_keys(creds))

    def test_write_creds_no_login_errors(self, command_login_tester):
        command_login_tester(["write-creds"])
        command_login_tester(["write-creds", TEST_RESOURCE])
        command_login_tester(["write-creds"], {"SYM_RESOURCE": TEST_RESOURCE})
        command_login_tester(["write-creds"], {"ENVIRONMENT": TEST_RESOURCE})

    def test_write_creds_command_executes_correct_action_with_params(
        self, simple_command_tester, capture_command, creds_env, credentials_path, sandbox
    ):
        with self.write_creds_context_manager(capture_command, sandbox, creds_env):
            sandbox.create_binary(f"bin/aws")
            sandbox.create_binary(f"bin/session-manager-plugin")

            with patch.object(WriteCredsAction, "write_creds") as mock_write_creds:
                result = simple_command_tester(
                    [
                        "write-creds",
                        TEST_RESOURCE,
                        "--profile",
                        TEST_PROFILE,
                        "--path",
                        str(credentials_path),
                    ],
                )

                assert result.exit_code == 0
                mock_write_creds.assert_called_once_with(
                    TEST_RESOURCE, ANY, str(credentials_path), TEST_PROFILE
                )

    ##############################################################################################
    # SECTION 2
    # pytest fixture and testing data preparation
    # and data creation helper methods
    #
    ##############################################################################################

    @pytest.fixture
    def credentials_path(self, sandbox: Sandbox):
        """Create `.aws/credentials` file in the sandbox environment
        and return the path.
        """

        credentials_path = sandbox.path / ".aws" / "credentials"

        try:
            credentials_path.parent.mkdir(parents=True)
            credentials_path.touch()
        except FileExistsError:
            # Allow tests to use this fixture to get the path even
            # if they've already used this fixture to create the file.
            pass

        return credentials_path

    def get_credentials_from_file(self, path: Path, profile: str) -> dict:
        """Read AWS credentials file at path and return all creds
        for the provided profile as a dict.

        Does some replacements to reverse changes we make when writing
        credentials to the file so it can be compared to internal dicts
        like the creds_env fixture easily.
        """

        config = ConfigParser()
        with open(path) as f:
            config.read_file(f)

        creds = config.items(profile)
        creds_dict = {k.upper(): v for k, v in creds}

        for file_key_name, internal_key_name in CRED_KEYS_MAPPING.items():
            val = creds_dict.pop(file_key_name)
            creds_dict[internal_key_name] = val

        return creds_dict

    @contextmanager
    def write_creds_context_manager(
        self,
        capture_command: CaptureCommand,
        sandbox: Sandbox,
        creds_env: Optional[Dict[str, str]] = None,
        create_binary: bool = True,
    ):
        """Load all required context for executing WriteCredsAction.

        Initializes capture_command for stubbing subprocesses,
        stubs the process to get creds from the environment,
        simulates a sym login with the "sym" org and "y@symops.io" email,
        and initializes a sandbox with an AwsOkta binary.

        See test_execute_write_creds as an example of usage.

        Args:
            capture_command: instance of CaptureCommand to stub subprocesses
            sandbox: instance of Sandbox to keep tests isolated
            creds_env: key/value pairs to set as the result for the subprocess
                that retrieves creds from the local environment
            create_binary: whether to create the AwsOkta binary
        """

        if not creds_env:
            creds_env = {}

        with capture_command():
            capture_command.register_output(r"env", _env_str(creds_env))

            with sandbox.push_xdg_config_home():
                Config.instance()["org"] = "sym"
                Config.instance()["email"] = "y@symops.io"

                if create_binary:
                    sandbox.create_binary(f"bin/{AwsOkta.binary}")

                with sandbox.push_exec_path():
                    yield
