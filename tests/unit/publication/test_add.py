"""Test the publication.add function."""

from geneweaver.core.schema.publication import PublicationInfo
from geneweaver.db.aio.publication import add as async_add
from geneweaver.db.publication import add

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchone_raises_error_test,
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)

EXAMPLE_PUBLICATION = PublicationInfo(
    authors="Author 1",
    title="Title 1",
    abstract="Abstract 1",
    journal="Journal 1",
    pubmed_id="12345678",
    pages=1,
    month="Dec",
    year=2021,
)

test_add_execute_raises_error = create_execute_raises_error_test(
    add, EXAMPLE_PUBLICATION
)

test_add_fetchone_raises_error = create_fetchone_raises_error_test(
    add, EXAMPLE_PUBLICATION
)

test_async_add_execute_raises_error = async_create_execute_raises_error_test(
    async_add, EXAMPLE_PUBLICATION
)

test_async_add_fetchone_raises_error = async_create_fetchone_raises_error_test(
    async_add, EXAMPLE_PUBLICATION
)
