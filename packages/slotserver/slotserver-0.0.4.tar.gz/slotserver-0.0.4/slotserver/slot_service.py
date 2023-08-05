# Copyright (c) 2020 Hugh Wade
# SPDX-License-Identifier: MIT
import slotserver.slot_repository as sr

MAX_ID_LEN = 1024
MAX_DATA_LEN = 1024 * 8
MAX_BATCH_SLOTS = 10
MAX_BATCH_SUBSLOTS = 10


class SlotOverflowException(Exception):
    '''
    Raised when something is bigger than allowed
    '''
    pass


class SlotUnderflowException(Exception):
    '''
    Raised when something is smaller than allowed
    '''
    pass


class SlotConsumerService():
    '''
    Read only interface to slot data.
    Enforces size constraints that mitigate DOS attack vectors.
    '''

    def __init__(self, repo: sr.SlotRepositoryInterface):
        self.repo = repo

    def get_slotdata(self, slot_ids: object, subslot_ids: object) -> object:
        '''
        Get data for a set of slot/subslots.
        Returned as a Dictionary of Dictionaries:  data[slot_id][subslot_id]
        '''
        if(len(slot_ids) > MAX_BATCH_SLOTS or
           len(subslot_ids) > MAX_BATCH_SUBSLOTS):
            raise SlotOverflowException()

        if(len(slot_ids) == 0 or
           len(subslot_ids) == 0):
            raise SlotUnderflowException()

        results = {}
        for slot_id in slot_ids:
            results[slot_id] = {}
            for subslot_id in subslot_ids:
                results[slot_id][subslot_id] = \
                    self.repo.get(slot_id, subslot_id, False)

        return results


class SlotProducerService():
    '''
    Write only interface to slot data.
    Enforces size constraints that mitigate DOS attack vectors.
    '''

    def __init__(self, repo: sr.SlotRepositoryInterface):
        self.repo = repo

    def update_slot(self, slot_id: str, subslot_id: str, data: str) -> None:
        if(len(slot_id) > MAX_ID_LEN or
           len(subslot_id) > MAX_ID_LEN or
           len(data) > MAX_DATA_LEN):
            raise SlotOverflowException()

        self.repo.upsert(slot_id, subslot_id, data)
