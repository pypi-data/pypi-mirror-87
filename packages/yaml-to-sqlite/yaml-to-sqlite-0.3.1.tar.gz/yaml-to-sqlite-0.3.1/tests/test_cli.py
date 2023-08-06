from click.testing import CliRunner
from yaml_to_sqlite import cli
import sqlite_utils
import json


TEST_YAML = """
- name: datasette-cluster-map
  url: https://github.com/simonw/datasette-cluster-map
- name: datasette-vega
  url: https://github.com/simonw/datasette-vega
  nested_with_date:
  - title: Hello
    date: 2010-01-01
"""
EXPECTED = [
    {
        "name": "datasette-cluster-map",
        "url": "https://github.com/simonw/datasette-cluster-map",
        "nested_with_date": None,
    },
    {
        "name": "datasette-vega",
        "url": "https://github.com/simonw/datasette-vega",
        "nested_with_date": json.dumps([{"title": "Hello", "date": "2010-01-01"}]),
    },
]


def test_without_pk(tmpdir):
    db_path = tmpdir / "db.db"
    assert (
        0
        == CliRunner()
        .invoke(cli.cli, [str(db_path), "items", "-"], input=TEST_YAML)
        .exit_code
    )
    db = sqlite_utils.Database(str(db_path))
    assert EXPECTED == list(db["items"].rows)
    # Run it again should get double the rows
    CliRunner().invoke(cli.cli, [str(db_path), "items", "-"], input=TEST_YAML)
    assert EXPECTED + EXPECTED == list(db["items"].rows)


def test_with_pk(tmpdir):
    db_path = tmpdir / "db.db"
    assert (
        0
        == CliRunner()
        .invoke(cli.cli, [str(db_path), "items", "-", "--pk", "name"], input=TEST_YAML)
        .exit_code
    )
    db = sqlite_utils.Database(str(db_path))
    assert EXPECTED == list(db["items"].rows)
    # Run it again should get same number of rows
    CliRunner().invoke(cli.cli, [str(db_path), "items", "-"], input=TEST_YAML)
    assert EXPECTED == list(db["items"].rows)
