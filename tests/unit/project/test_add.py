"""Test the project.add function."""

from geneweaver.core.schema.project import ProjectCreate
from geneweaver.db.aio.project import add as async_add
from geneweaver.db.project import add

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchone_raises_error_test,
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)

EXAMPLE_PROJECT = ProjectCreate(name="test name", notes="test notes")

test_add_execute_raises_error = create_execute_raises_error_test(
    add, EXAMPLE_PROJECT, 1, 1
)

test_add_fetchone_raises_error = create_fetchone_raises_error_test(
    add, EXAMPLE_PROJECT, 1, 1
)

test_async_add_execute_raises_error = async_create_execute_raises_error_test(
    async_add, EXAMPLE_PROJECT, 1, 1
)

test_async_add_fetchone_raises_error = async_create_fetchone_raises_error_test(
    async_add, EXAMPLE_PROJECT, 1, 1
)
