"""Test project geneset functions."""

from geneweaver.db.aio.project import (
    add_geneset_to_project as async_add_geneset_to_project,
)
from geneweaver.db.aio.project import (
    delete_geneset_from_project as async_delete_geneset_to_project,
)
from geneweaver.db.project import add_geneset_to_project, delete_geneset_from_project

from tests.unit.testing_utils import (
    async_create_execute_raises_error_test,
    async_create_fetchone_raises_error_test,
    create_execute_raises_error_test,
    create_fetchone_raises_error_test,
)

test_add_execute_raises_error = create_execute_raises_error_test(
    add_geneset_to_project, 1, 1
)

test_add_fetchone_raises_error = create_fetchone_raises_error_test(
    add_geneset_to_project, 1, 1
)

test_async_add_execute_raises_error = async_create_execute_raises_error_test(
    async_add_geneset_to_project, 1, 1
)

test_async_add_fetchone_raises_error = async_create_fetchone_raises_error_test(
    async_add_geneset_to_project, 1, 1
)

test_add_execute_raises_error = create_execute_raises_error_test(
    delete_geneset_from_project, 1, 1
)

test_add_fetchone_raises_error = create_fetchone_raises_error_test(
    delete_geneset_from_project, 1, 1
)

test_async_add_execute_raises_error = async_create_execute_raises_error_test(
    async_delete_geneset_to_project, 1, 1
)

test_async_add_fetchone_raises_error = async_create_fetchone_raises_error_test(
    async_delete_geneset_to_project, 1, 1
)
