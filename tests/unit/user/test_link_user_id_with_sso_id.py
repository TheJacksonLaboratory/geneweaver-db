"""Test the link_user_id_with_sso_id function."""
from unittest.mock import patch

import pytest
from geneweaver.db.user import link_user_id_with_sso_id


@pytest.mark.parametrize("sso_id_exists_return", [True, False])
def test_link_user_id_with_sso_id(sso_id_exists_return, cursor) -> None:
    """Test that link_user_id_with_sso_id executes correctly."""
    with patch(
        "geneweaver.db.user.sso_id_exists", return_value=sso_id_exists_return
    ) as sso_id_exists:
        if sso_id_exists_return is False:
            link_user_id_with_sso_id(cursor, 1, "auth0|5f9b7b7a9a9a9a9a9a9a9a9a")
            assert cursor.execute.call_count == 1
            assert cursor.connection.commit.call_count == 1
            assert cursor.fetchone.call_count == 1
        else:
            with pytest.raises(
                ValueError, match="SSO ID is already linked to a different account"
            ):
                link_user_id_with_sso_id(cursor, 1, "auth0|5f9b7b7a9a9a9a9a9a9a9a9a")
            assert cursor.execute.call_count == 0
            assert cursor.connection.commit.call_count == 0
            assert cursor.fetchone.call_count == 0

        assert sso_id_exists.call_count == 1
        assert cursor.fetchall.call_count == 0


@patch("geneweaver.db.user.sso_id_exists", return_value=False)
def test_link_user_id_with_sso_id_execute_raises_error(
    sso_id_exists, all_psycopg_errors, cursor_execute_raises_error
) -> None:
    """Test that it raises an error when cursor.execute raises an error."""
    with pytest.raises(all_psycopg_errors, match="Error message"):
        link_user_id_with_sso_id(
            cursor_execute_raises_error, 1, "auth0|5f9b7b7a9a9a9a9a9a9a9a9a"
        )
    assert cursor_execute_raises_error.execute.call_count == 1
    assert cursor_execute_raises_error.fetchone.call_count == 0
    assert cursor_execute_raises_error.fetchall.call_count == 0
    assert sso_id_exists.call_count == 1


@patch("geneweaver.db.user.sso_id_exists", return_value=False)
def test_link_user_id_with_sso_id_fetchone_raises_error(
    sso_id_exists, all_psycopg_errors, cursor_fetchone_raises_error
) -> None:
    """Test that it raises an error when cursor.fetchone raises an error."""
    with pytest.raises(all_psycopg_errors, match="Error message"):
        link_user_id_with_sso_id(
            cursor_fetchone_raises_error, 1, "auth0|5f9b7b7a9a9a9a9a9a9a9a9a"
        )
    assert cursor_fetchone_raises_error.execute.call_count == 1
    assert cursor_fetchone_raises_error.fetchone.call_count == 1
    assert cursor_fetchone_raises_error.fetchall.call_count == 0
    assert sso_id_exists.call_count == 1
