"""Test the species get_by_id function (sync and async)."""
from geneweaver.db.aio.species import get_by_id as async_get_by_id
from geneweaver.db.species import get_by_id

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchone_raises_error_test,
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)

test_get_by_id_execute_raises_error = create_execute_raises_error_test(get_by_id, 1234)

test_get_by_id_fetchone_raises_error = create_fetchone_raises_error_test(
    get_by_id, 1234
)

test_async_get_by_id_execute_raises_error = async_create_execute_raises_error_test(
    async_get_by_id, 1234
)

test_async_get_by_id_fetchone_raises_error = async_create_fetchone_raises_error_test(
    async_get_by_id, 1234
)
