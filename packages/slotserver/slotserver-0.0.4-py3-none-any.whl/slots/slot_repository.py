# Copyright (c) 2020 Hugh Wade
# SPDX-License-Identifier: MIT

import abc
import threading
import pickle
import os.path


class SlotRepositoryInterface(metaclass=abc.ABCMeta):
    '''
    Slot server repository.
    Logical datashape is a Dictionary of Dictionaries.
    Persists instance data used by IOT dashboard elements.
    '''
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get') and
                callable(subclass.get) and
                hasattr(subclass, 'upsert') and
                callable(subclass.upsert) and
                hasattr(subclass, 'delete') and
                callable(subclass.delete) and
                hasattr(subclass, 'slots') and
                callable(subclass.slots) and
                hasattr(subclass, 'subslots') and
                callable(subclass.subslots) or
                NotImplemented)

    @abc.abstractmethod
    def get(self, slot_id: str, subslot_id: str, raise_error: bool) -> object:
        '''
        Get the data for a slot.
        A SlotNotFoundException will be raised if the slot is missing
        and raise_error is True
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def upsert(self, slot_id: str, subslot_id: str, data: object) -> None:
        '''
        Upsert data in a slot.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, slot_id: str, subslot_id: str) -> None:
        '''
        Delete data in a slot.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def slots(self) -> object:
        '''
        Returns a list of existing slot_ids
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def subslots(self, slot_id: str) -> object:
        '''
        Returns a list of existing subslot_ids under a slot_id
        '''
        raise NotImplementedError


class SlotNotFoundException(Exception):
    '''
    Raised when the requested slot does not exist.
    '''
    pass


class MemorySlotRepository(SlotRepositoryInterface):
    '''
    Memory backed slot repository. Threadsafe, should be used as a singleton.
    '''

    def __init__(self):
        self.backing = {}
        self.lock = threading.RLock()

    def get(self, slot_id: str, subslot_id: str, raise_error: bool) -> object:
        result = None
        with self.lock:
            slot = self.backing.get(slot_id)
            result = slot.get(subslot_id) if slot else None
            if result is None and raise_error is True:
                raise SlotNotFoundException
        return result

    def upsert(self, slot_id: str, subslot_id: str, data: object) -> None:
        with self.lock:
            slot = self.backing.get(slot_id)
            if slot is None:
                slot = {}
                self.backing[slot_id] = slot
            slot[subslot_id] = data

    def delete(self, slot_id: str, subslot_id: str) -> None:
        with self.lock:
            slot = self.backing.get(slot_id)
            if slot is not None:
                slot.pop(subslot_id, None)

    def slots(self) -> object:
        keys = []
        with self.lock:
            keys = self.backing.keys()
        return list(keys)

    def subslots(self, slot_id: str) -> object:
        keys = []
        with self.lock:
            slot = self.backing.get(slot_id)
            if slot is not None:
                keys = slot.keys()
        return list(keys)


class PickledSlotRepository(SlotRepositoryInterface):
    '''
    Disk backed slot repository. Threadsafe, should be used as a singleton.
    Pickle file should be protected as depickling can create code execution
    vulns.
    '''

    def __init__(self, pickle_path):
        self.backing = MemorySlotRepository()
        self.pickle_path = pickle_path
        self.unpickle()

    def pickle(self):
        pickle.dump(self.backing.backing, open(self.pickle_path, "wb"))

    def unpickle(self):
        if os.path.exists(self.pickle_path) is True:
            self.backing.backing = pickle.load(open(self.pickle_path, "rb"))

    def get(self, slot_id: str, subslot_id: str, raise_error: bool) -> object:
        result = None
        with self.backing.lock:
            result = self.backing.get(slot_id, subslot_id, raise_error)
        return result

    def upsert(self, slot_id: str, subslot_id: str, data: object) -> None:
        with self.backing.lock:
            self.backing.upsert(slot_id, subslot_id, data)
            self.pickle()

    def delete(self, slot_id: str, subslot_id: str) -> None:
        with self.backing.lock:
            self.backing.delete(slot_id, subslot_id)
            self.pickle()

    def slots(self) -> object:
        return self.backing.slots()

    def subslots(self, slot_id: str) -> object:
        return self.backing.subslots(slot_id)
