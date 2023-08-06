"""Fixtures for all tests."""
# pylint: disable=redefined-outer-name

import os
import pathlib

import pytest
import sqlalchemy
from sqlalchemy import orm

from open_alchemy import helpers


@pytest.fixture(scope="function", params=["sqlite:///:memory:"])
def engine(request):
    """Creates a sqlite engine."""
    return sqlalchemy.create_engine(request.param)


@pytest.fixture(scope="function")
def sessionmaker(engine):
    """Creates a sqlite session."""
    return orm.sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def _clean_remote_schemas_store():
    """Clean remote schemas store before and after test execution."""
    # pylint: disable=protected-access

    helpers.ref._remote_schema_store.reset()

    yield

    helpers.ref._remote_schema_store.reset()


@pytest.fixture(scope="function")
def _remember_current_directory():
    """Remember the current directory and make sure to switch back to it."""
    current_dir = pathlib.Path.cwd()

    yield

    os.chdir(current_dir)
