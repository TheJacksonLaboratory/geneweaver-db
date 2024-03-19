"""Test the get db exec functions (sync and async)."""

from geneweaver.core.enum import Species
from geneweaver.db.aio.gene import get as async_get
from geneweaver.db.gene import get

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)

test_get_execute_raises_error = create_execute_raises_error_test(
    get, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_get_fetchall_raises_error = create_fetchall_raises_error_test(
    get, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_async_get_execute_raises_error = async_create_execute_raises_error_test(
    async_get, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_async_get_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_get, ["a", "b", "c"], Species.GALLUS_GALLUS
)
