# encoding: utf-8

import pytest

import ckan.tests.factories as factories
from ckan import model
from ckan.model.system_info import SystemInfo, set_system_info


@pytest.mark.usefixtures("clean_db")
def test_set_value():

    key = "config_option_1"
    value = "test_value"
    set_system_info(key, value)

    results = model.Session.query(SystemInfo).filter_by(key=key).all()

    assert len(results) == 1

    obj = results[0]

    assert obj.key == key
    assert obj.value == value


@pytest.mark.usefixtures("clean_db")
def test_sets_new_value_for_same_key():

    config = factories.SystemInfo()
    first_revision = config.revision_id
    config = factories.SystemInfo()

    new_config = (
        model.Session.query(SystemInfo).filter_by(key=config.key).first()
    )

    assert config.id == new_config.id
    assert first_revision != new_config.revision_id

    assert config.id == new_config.id


@pytest.mark.usefixtures("clean_db")
def test_does_not_set_same_value_for_same_key():

    config = factories.SystemInfo()

    set_system_info(config.key, config.value)

    new_config = (
        model.Session.query(SystemInfo).filter_by(key=config.key).first()
    )

    assert config.id == new_config.id
