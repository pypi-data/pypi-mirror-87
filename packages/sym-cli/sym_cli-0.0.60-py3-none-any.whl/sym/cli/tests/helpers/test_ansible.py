from unittest.mock import patch

from expects import expect, match

from sym.cli.helpers.ansible import get_ansible_bucket_name
from sym.cli.helpers.params import Profile
from sym.cli.tests.commands.test_ansible import TEST_ACCOUNT, get_caller_identity_stub


def create_fake_profile_with_ansible_bucket(resource: str) -> Profile:
    """Mock function to return the sym organization's "test" AWS profile."""
    return Profile(
        display_name="Test",
        region="us-east-1",
        arn="arn:aws:iam::838419636750:role/SSMTestRole",
        ansible_bucket="foo",
    )


class TestAnsibleHelpers:
    """Test suite for ansible helper methods."""

    def test_get_default_ansible_bucket_name(self, boto_stub, saml_client):
        get_caller_identity_stub(boto_stub)
        actual = get_ansible_bucket_name(saml_client)
        expect(actual).to(match(f"sym-ansible-{TEST_ACCOUNT}"))

    @patch(
        "sym.cli.saml_clients.saml_client.get_profile",
        new=create_fake_profile_with_ansible_bucket,
    )
    def test_get_ansible_bucket_name_from_profile(self, boto_stub, saml_client):
        actual = get_ansible_bucket_name(saml_client)
        expect(actual).to(match("foo"))
