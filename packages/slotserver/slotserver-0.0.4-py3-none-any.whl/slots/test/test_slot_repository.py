# Copyright (c) 2020 Hugh Wade
# SPDX-License-Identifier: MIT

import pytest
import slots.slot_repository as sr
from pathlib import Path


SLOT_1 = "SLOT1"
SLOT_2 = "SLOT2"
SLOT_3 = "SLOT3"
SLOT_4 = "SLOT4"
SLOT_5 = "SLOT5"
SLOTS = [SLOT_1, SLOT_2, SLOT_3, SLOT_4, SLOT_5]

SUBSLOT_1 = "SUBSLOT1"
SUBSLOT_2 = "SUBSLOT2"
SUBSLOT_3 = "SUBSLOT3"
SUBSLOT_4 = "SUBSLOT4"
SUBSLOT_5 = "SUBSLOT5"
SUBSLOTS = [SUBSLOT_1, SUBSLOT_2, SUBSLOT_3, SUBSLOT_4, SUBSLOT_5]

SLOTDATA_1 = "SLOTDATA1"
SLOTDATA_2 = "SLOTDATA2"
SLOTDATA_3 = "SLOTDATA3"
SLOTDATA_4 = "SLOTDATA4"
SLOTDATA_5 = "SLOTDATA5"


def _mem_repo(tmp_path):
    mem_repo = sr.MemorySlotRepository()
    _init_defaults(mem_repo)
    return mem_repo


def _pickled_repo(tmp_path):

    pickle_path = tmp_path / 'ut.p'
    pickled_repo = sr.PickledSlotRepository(pickle_path)
    _init_defaults(pickled_repo)
    return pickled_repo


def _init_defaults(repo):
    repo.upsert(SLOT_1, SUBSLOT_1, SLOTDATA_1)
    repo.upsert(SLOT_1, SUBSLOT_2, SLOTDATA_2)
    repo.upsert(SLOT_1, SUBSLOT_3, SLOTDATA_3)
    repo.upsert(SLOT_1, SUBSLOT_4, SLOTDATA_4)
    repo.upsert(SLOT_1, SUBSLOT_5, SLOTDATA_5)

    repo.upsert(SLOT_2, SUBSLOT_1, SLOTDATA_1)
    repo.upsert(SLOT_2, SUBSLOT_2, SLOTDATA_2)
    repo.upsert(SLOT_2, SUBSLOT_3, SLOTDATA_3)
    repo.upsert(SLOT_2, SUBSLOT_4, SLOTDATA_4)
    repo.upsert(SLOT_2, SUBSLOT_5, SLOTDATA_5)

    repo.upsert(SLOT_3, SUBSLOT_1, SLOTDATA_1)
    repo.upsert(SLOT_3, SUBSLOT_2, SLOTDATA_2)
    repo.upsert(SLOT_3, SUBSLOT_3, SLOTDATA_3)
    repo.upsert(SLOT_3, SUBSLOT_4, SLOTDATA_4)
    repo.upsert(SLOT_3, SUBSLOT_5, SLOTDATA_5)

    repo.upsert(SLOT_4, SUBSLOT_1, SLOTDATA_1)
    repo.upsert(SLOT_4, SUBSLOT_2, SLOTDATA_2)
    repo.upsert(SLOT_4, SUBSLOT_3, SLOTDATA_3)
    repo.upsert(SLOT_4, SUBSLOT_4, SLOTDATA_4)
    repo.upsert(SLOT_4, SUBSLOT_5, SLOTDATA_5)

    repo.upsert(SLOT_5, SUBSLOT_1, SLOTDATA_1)
    repo.upsert(SLOT_5, SUBSLOT_2, SLOTDATA_2)
    repo.upsert(SLOT_5, SUBSLOT_3, SLOTDATA_3)
    repo.upsert(SLOT_5, SUBSLOT_4, SLOTDATA_4)
    repo.upsert(SLOT_5, SUBSLOT_5, SLOTDATA_5)


class TestSlotRepositoryInterface(object):
    '''
    Abstract interface test
    Check that interface is actually abstract
    '''

    def test_abstract(self):
        with pytest.raises(TypeError):
            sr.SlotRepositoryInterface()


@pytest.mark.parametrize("repo_factory", [_mem_repo, _pickled_repo])
class TestSlotRepositoryFunctional(object):
    '''
    Generic public interface test.
    Repositories should have a factory added to the parmeterization list
    '''

    def test_get_existing(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        actual = repo.get(SLOT_1, SUBSLOT_1, False)
        assert actual == SLOTDATA_1

    def test_get_existing_throw(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        actual = repo.get(SLOT_1, SUBSLOT_1, True)
        assert actual == SLOTDATA_1

    def test_get_missing_slot(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        actual = repo.get("not_a_slot", SUBSLOT_1, False)
        assert actual is None

    def test_get_missing_subslot(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        actual = repo.get(SLOT_1, "not_a_subslot", False)
        assert actual is None

    def test_get_missing_slot_throw(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        with pytest.raises(sr.SlotNotFoundException):
            repo.get("not_a_slot", SUBSLOT_1, True)

    def test_get_missing_subslot_throw(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        with pytest.raises(sr.SlotNotFoundException):
            repo.get(SLOT_1, "not_a_subslot", True)

    def test_upsert_missing_slot(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        new_slot = "new_slot"
        new_slot_data = "new_slot_data"
        assert repo.get(new_slot, SUBSLOT_1, False) is None

        repo.upsert(new_slot, SUBSLOT_1, new_slot_data)
        assert repo.get(new_slot, SUBSLOT_1, False) == new_slot_data

    def test_upsert_missing_subslot(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        new_sub_slot = "new_sub_slot"
        new_slot_data = "new_slot_data"
        assert repo.get(SLOT_1, new_sub_slot, False) is None

        repo.upsert(SLOT_1, new_sub_slot, new_slot_data)
        assert repo.get(SLOT_1, new_sub_slot, False) == new_slot_data

    def test_upsert_existing(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        new_slot_data = "new_slot_data"
        assert repo.get(SLOT_1, SUBSLOT_1, False) == SLOTDATA_1

        repo.upsert(SLOT_1, SUBSLOT_1, new_slot_data)
        assert repo.get(SLOT_1, SUBSLOT_1, False) == new_slot_data
        assert repo.get(SLOT_1, SUBSLOT_2, False) == SLOTDATA_2
        assert repo.get(SLOT_2, SUBSLOT_1, False) == SLOTDATA_1
        assert repo.get(SLOT_2, SUBSLOT_2, False) == SLOTDATA_2

    def test_delete_missing_slot(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        repo.delete("not_a_slot", SUBSLOT_1)
        assert repo.get(SLOT_1, SUBSLOT_1, False) == SLOTDATA_1
        assert repo.get(SLOT_1, SUBSLOT_2, False) == SLOTDATA_2

    def test_delete_missing_subslot(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        repo.delete(SLOT_1, "not_a_subslot")
        assert repo.get(SLOT_1, SUBSLOT_1, False) == SLOTDATA_1
        assert repo.get(SLOT_1, SUBSLOT_2, False) == SLOTDATA_2

    def test_delete_existing(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        repo.delete(SLOT_1, SUBSLOT_1)
        assert repo.get(SLOT_1, SUBSLOT_1, False) is None

    def test_slots(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        actual = repo.slots()
        assert actual == SLOTS

    def test_subslots_existing(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        actual = repo.subslots(SLOT_1)
        assert actual == SUBSLOTS

    def test_subslots_missing(self, repo_factory, tmp_path):
        repo = repo_factory(tmp_path)
        actual = repo.subslots("not_a_slot")
        assert actual == []


class TestPickledSlotRepository(object):
    '''
    Pickle specific tests
    '''

    def test_persistance(self, tmp_path):
        '''
        Verify that changes are persisted across instances of the repo
        '''
        changed_data = "changed data"
        repo = _pickled_repo(tmp_path)

        # Pickle file should exist
        assert Path(repo.pickle_path).exists()

        # Upserted item should be a new object with the same value
        repo.upsert(SLOT_1, SUBSLOT_1, changed_data)
        expected = repo.get(SLOT_1, SUBSLOT_1, False)
        repo = sr.PickledSlotRepository(repo.pickle_path)
        actual = repo.get(SLOT_1, SUBSLOT_1, False)
        assert actual is not expected
        assert actual == expected

        # Deleted item should no longer exist
        repo.delete(SLOT_1, SUBSLOT_1)
        repo = sr.PickledSlotRepository(repo.pickle_path)
        actual = repo.get(SLOT_1, SUBSLOT_1, False)
        assert actual is None
