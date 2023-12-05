"""Test the geneset.update_date function."""
import pytest
from geneweaver.db.geneset import update_date


@pytest.mark.parametrize(
    "example_dates",
    [
        ("2020-05-06 09:19:44.883323",),
        ("2007-03-14 00:00:00",),
        ("2007-04-11 00:00:00",),
        ("2010-12-21 18:51:21.456925",),
        ("2010-12-21 18:51:22.067045",),
        ("2015-07-15 20:43:04.532024",),
        ("2018-01-19 10:50:09.552803",),
        ("2020-05-06 09:19:44.883324",),
        ("2020-05-06 09:49:44.883323",),
    ],
)
def test_update_date(example_dates, cursor, example_primary_key):
    """Test the geneset.update_date function."""
    cursor.fetchone.return_value = example_dates
    update_date(cursor, example_primary_key)
    assert cursor.execute.call_count == 1
    assert cursor.fetchone.call_count == 1
    assert cursor.connection.commit.call_count == 1
    assert cursor.fetchall.call_count == 0
    assert "UPDATE" in cursor.execute.call_args[0][0]
    assert "NOW()" in cursor.execute.call_args[0][0]
    assert example_primary_key in cursor.execute.call_args[0][1].values()
