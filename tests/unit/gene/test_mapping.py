"""Test the mapping gene db exec functions (sync and async)."""
from geneweaver.core.enum import Species
from geneweaver.db.aio.gene import mapping as async_mapping
from geneweaver.db.gene import mapping

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)

test_mapping_execute_raises_error = create_execute_raises_error_test(
    mapping, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_mapping_fetchall_raises_error = create_fetchall_raises_error_test(
    mapping, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_async_mapping_execute_raises_error = async_create_execute_raises_error_test(
    async_mapping, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_async_mapping_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_mapping, ["a", "b", "c"], Species.GALLUS_GALLUS
)
