# Copyright (c) 2020 Hugh Wade
# SPDX-License-Identifier: MIT
import pytest
import slotserver.slot_http_client as sfc

SLOT_1 = "SLOT1"
SLOT_2 = "SLOT2"
SLOTS = [SLOT_1, SLOT_2]

SUBSLOT_1 = "SUBSLOT1"
SUBSLOT_2 = "SUBSLOT2"
SUBSLOTS = [SUBSLOT_1, SUBSLOT_2]

SLOTDATA_1 = "SLOTDATA1"
SLOTDATA_2 = "SLOTDATA2"

BASE_URL = 'http://127.0.0.1:5000'


class TestSlotProducerClient(object):
    @pytest.mark.vcr()
    def test_produce(self):
        client = sfc.SlotProducerClient(BASE_URL)
        client.produce(SLOT_1, SUBSLOT_1, SLOTDATA_1)


class TestSlotConsumerClient(object):
    @pytest.mark.vcr()
    def test_consume(self):
        client = sfc.SlotConsumerClient(BASE_URL)
        client.consume(SLOTS, SUBSLOTS)
