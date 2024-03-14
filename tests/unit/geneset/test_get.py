"""Test the general geneset.get function."""
from geneweaver.db.aio.geneset import get as async_get
from geneweaver.db.geneset import get

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)

test_get_execute_raises_error = create_execute_raises_error_test(
    get,
)

test_get_fetchall_raises_error = create_fetchall_raises_error_test(
    get,
)

test_async_get_execute_raises_error = async_create_execute_raises_error_test(
    async_get,
)

test_async_get_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_get,
)
