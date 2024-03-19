"""Test the create_sso_user function."""

from geneweaver.db.user import create_sso_user

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)

test_create_sso_user_execute_raises_error = create_execute_raises_error_test(
    create_sso_user, "test", "", "auth0|5f9b7b7a9a9a9a9a9a9a9a9a"
)

test_create_sso_user_fetchone_raises_error = create_fetchone_raises_error_test(
    create_sso_user, "test", "", "auth0|5f9b7b7a9a9a9a9a9a9a9a9a"
)
