from click import BadParameter

from sym.cli.helpers.contexts import push_env
from sym.cli.sym import sym as click_command
from sym.cli.version import __version__


def test_version(click_setup):
    with click_setup(set_org=False, set_client=False) as runner:
        result = runner.invoke(click_command, ["version"])
        assert result.exit_code == 0
        assert result.output == f"{__version__}\n"


def test_login(click_setup):
    with click_setup(set_org=False) as runner:
        result = runner.invoke(
            click_command, ["login", "--org", "sym", "--email", "y@symops.io"]
        )
        assert result.exit_code == 0
        assert result.output == "Sym successfully initalized!\n"


def test_resources(click_setup):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["resources"])
        assert result.exit_code == 0
        assert (
            result.output
            == "test (Test)\ntest_euw1 (Test: EU West 1)\ntest-custom (TestCustom)\n"
        )


def test_exec(click_setup, saml_client):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["exec", "test", "--", "aws"])
        assert result.exit_code == 0


def test_env_vars(click_setup):
    with click_setup() as runner:
        with push_env("SYM_RESOURCE", "test"):
            result = runner.invoke(click_command, ["exec", "--", "aws"])
            assert result.exit_code == 0


def test_env_vars_invalid(click_setup):
    with click_setup() as runner:
        with push_env("SYM_RESOURCE", "tesst"):
            result = runner.invoke(click_command, ["exec", "--", "aws"])
            assert result.exit_code == BadParameter.exit_code
            assert "Invalid resource: tesst" in result.output


def test_env_vars_override(click_setup):
    with click_setup() as runner:
        with push_env("SYM_RESOURCE", "invalid"):
            result = runner.invoke(click_command, ["exec", "test", "--", "true"])
            assert result.exit_code == 0


def test_env_vars_override_invalid(click_setup):
    with click_setup() as runner:
        with push_env("SYM_RESOURCE", "invalid"):
            result = runner.invoke(click_command, ["exec", "invalid2", "--", "true"])
            assert result.exit_code == BadParameter.exit_code
            assert "Invalid resource: invalid" in result.output
