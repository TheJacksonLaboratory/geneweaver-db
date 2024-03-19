"""Test the get_preferred db exec functions (sync and async)."""

from geneweaver.core.enum import Species
from geneweaver.db.aio.gene import get_preferred as async_get_preferred
from geneweaver.db.gene import get_preferred

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchone_raises_error_test,
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)

test_get_preferred_execute_raises_error = create_execute_raises_error_test(
    get_preferred, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_get_preferred_fetchone_raises_error = create_fetchone_raises_error_test(
    get_preferred, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_async_get_preferred_execute_raises_error = async_create_execute_raises_error_test(
    async_get_preferred, ["a", "b", "c"], Species.GALLUS_GALLUS
)

test_async_get_preferred_fetchone_raises_error = (
    async_create_fetchone_raises_error_test(
        async_get_preferred, ["a", "b", "c"], Species.GALLUS_GALLUS
    )
)
