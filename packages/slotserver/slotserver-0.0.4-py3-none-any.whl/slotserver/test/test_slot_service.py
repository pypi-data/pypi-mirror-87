# Copyright (c) 2020 Hugh Wade
# SPDX-License-Identifier: MIT

import pytest
import slotserver.slot_service as ss
import slotserver.slot_repository as sr


SLOT_1 = "SLOT1"
SLOT_2 = "SLOT2"
SLOTS = [SLOT_1, SLOT_2]

SUBSLOT_1 = "SUBSLOT1"
SUBSLOT_2 = "SUBSLOT2"
SUBSLOTS = [SUBSLOT_1, SUBSLOT_2]

SLOTDATA_1 = "SLOTDATA1"
SLOTDATA_2 = "SLOTDATA2"


def _init_defaults(repo):
    repo.upsert(SLOT_1, SUBSLOT_1, SLOTDATA_1)
    repo.upsert(SLOT_1, SUBSLOT_2, SLOTDATA_2)

    repo.upsert(SLOT_2, SUBSLOT_1, SLOTDATA_1)
    repo.upsert(SLOT_2, SUBSLOT_2, SLOTDATA_2)


def _mem_repo():
    repo = sr.MemorySlotRepository()
    _init_defaults(repo)
    return repo


class TestSlotProducerService(object):
    def test_update_slot(self):
        new_data = "new_data"
        repo = _mem_repo()
        service = ss.SlotProducerService(repo)

        assert repo.get(SLOT_1, SUBSLOT_1, False) != new_data
        service.update_slot(SLOT_1, SUBSLOT_1, new_data)
        assert repo.get(SLOT_1, SUBSLOT_1, False) == new_data

    def test_update_overflow_slot_id(self):
        service = ss.SlotProducerService(_mem_repo())
        overflow = ''.join('a' for _ in range(ss.MAX_ID_LEN + 1))
        with pytest.raises(ss.SlotOverflowException):
            service.update_slot(overflow, SUBSLOT_1, SLOTDATA_1)

    def test_update_overflow_subslot_id(self):
        service = ss.SlotProducerService(_mem_repo())
        overflow = ''.join('a' for _ in range(ss.MAX_ID_LEN + 1))
        with pytest.raises(ss.SlotOverflowException):
            service.update_slot(SLOT_1, overflow, SLOTDATA_1)

    def test_update_overflow_data(self):
        service = ss.SlotProducerService(_mem_repo())
        overflow = ''.join('a' for _ in range(ss.MAX_DATA_LEN + 1))
        with pytest.raises(ss.SlotOverflowException):
            service.update_slot(SLOT_1, SUBSLOT_1, overflow)


class TestSlotConsumerService(object):
    def test_get_slotdata(self):
        service = ss.SlotConsumerService(_mem_repo())
        actual = service.get_slotdata([SLOT_1, SLOT_2], [SUBSLOT_1, SUBSLOT_2])
        assert actual is not None
        assert len(actual) == 2
        assert len(actual[SLOT_1]) == 2
        assert len(actual[SLOT_2]) == 2

    def test_get_slotdata_overflow_slots(self):
        service = ss.SlotConsumerService(_mem_repo())
        slots = [0]*(ss.MAX_BATCH_SLOTS + 1)
        subslots = []
        with pytest.raises(ss.SlotOverflowException):
            service.get_slotdata(slots, subslots)

    def test_get_slotdata_overflow_subslots(self):
        service = ss.SlotConsumerService(_mem_repo())
        slots = []
        subslots = [0]*(ss.MAX_BATCH_SUBSLOTS + 1)
        with pytest.raises(ss.SlotOverflowException):
            service.get_slotdata(slots, subslots)

    def test_get_slotdata_underflow_slots(self):
        service = ss.SlotConsumerService(_mem_repo())
        slots = [0]
        subslots = []
        with pytest.raises(ss.SlotUnderflowException):
            service.get_slotdata(slots, subslots)

    def test_get_slotdata_underflow_subslots(self):
        service = ss.SlotConsumerService(_mem_repo())
        slots = []
        subslots = [0]
        with pytest.raises(ss.SlotUnderflowException):
            service.get_slotdata(slots, subslots)
