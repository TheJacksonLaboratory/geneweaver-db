"""Test the aon_mapping gene db exec functions (sync and async)."""

from geneweaver.core.enum import Species
from geneweaver.db.aio.gene import aon_mapping as async_aon_mapping
from geneweaver.db.gene import aon_mapping

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchall_raises_error_test,
    create_execute_raises_error_test,
    create_fetchall_raises_error_test,
)

test_aon_mapping_execute_raises_error = create_execute_raises_error_test(
    aon_mapping, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_aon_mapping_fetchall_raises_error = create_fetchall_raises_error_test(
    aon_mapping, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_async_aon_mapping_execute_raises_error = async_create_execute_raises_error_test(
    async_aon_mapping, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_async_aon_mapping_fetchall_raises_error = async_create_fetchall_raises_error_test(
    async_aon_mapping, ["a", "b", "c"], Species.GALLUS_GALLUS
)
