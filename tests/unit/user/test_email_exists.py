"""Test the sso_id_exists function."""
from geneweaver.db.user import email_exists

from tests.unit.testing_utils import (
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)

test_sso_id_exists_execute_raises_error = create_execute_raises_error_test(
    email_exists, "email@email.com"
)

test_sso_id_exists_fetchone_raises_error = create_fetchone_raises_error_test(
    email_exists, "email@email.com"
)


def test_sso_id_exists_returns_true_when_sso_id_exists(cursor):
    """Test that sso_id_exists returns True when the sso id exists."""
    cursor.execute.return_value = [(1,)]
    assert email_exists(cursor, "email@email.com")


def test_sso_id_exists_returns_false_when_sso_id_dn_exists(cursor):
    """Test that sso_id_exists returns True when the sso id exists."""
    cursor.execute.return_value = []
    assert email_exists(cursor, "email@email.com")
