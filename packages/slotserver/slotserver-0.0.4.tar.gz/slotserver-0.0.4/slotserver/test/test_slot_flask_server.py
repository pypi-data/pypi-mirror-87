# Copyright (c) 2020 Hugh Wade
# SPDX-License-Identifier: MIT
import pytest
from flask import url_for
import slotserver.slot_flask_server as sfr
import slotserver.slot_repository as sr


SLOT_1 = "SLOT1"
SLOT_2 = "SLOT2"
SLOTS = [SLOT_1, SLOT_2]

SUBSLOT_1 = "SUBSLOT1"
SUBSLOT_2 = "SUBSLOT2"
SUBSLOTS = [SUBSLOT_1, SUBSLOT_2]

SLOTDATA_1 = "SLOTDATA1"
SLOTDATA_2 = "SLOTDATA2"


@pytest.fixture
def app():
    return sfr.create_app()


def test_app_trace():
    sfr.trace('test trace')


def test_app_memory():
    app = sfr.create_app('memory')
    assert type(app.p_service.repo) is sr.MemorySlotRepository


def test_app_pickled():
    app = sfr.create_app('pickle')
    assert type(app.p_service.repo) is sr.PickledSlotRepository


def test_app_consume(client):
    payload = {'slot_ids': SLOTS,
               'subslot_ids': SUBSLOTS}
    actual = client.post(url_for('slots.consume'), json=payload)
    assert actual.status_code == 200


def test_app_produce(client):
    payload = {'slot_id': SLOT_1,
               'subslot_id': SUBSLOT_1,
               'data': SLOTDATA_1}
    actual = client.post(url_for('slots.produce'), json=payload)
    assert actual.status_code == 200


def test_app_consume_empty_body(client):
    payload = {}
    actual = client.post(url_for('slots.consume'), json=payload)
    assert actual.status_code == 500


def test_app_produce_empty_body(client):
    payload = {}
    actual = client.post(url_for('slots.produce'), json=payload)
    assert actual.status_code == 500


def test_app_consume_no_body(client):
    payload = None
    actual = client.post(url_for('slots.consume'), json=payload)
    assert actual.status_code == 500


def test_app_produce_no_body(client):
    payload = None
    actual = client.post(url_for('slots.produce'), json=payload)
    assert actual.status_code == 500
