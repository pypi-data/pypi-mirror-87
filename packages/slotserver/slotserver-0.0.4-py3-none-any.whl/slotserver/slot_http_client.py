# Copyright (c) 2020 Hugh Wade
# SPDX-License-Identifier: MIT
import requests


class SlotConsumerClient():
    '''
    Client for slotserver's consumer http endpoint
    '''
    def __init__(self, base_address):
        self.base_address = base_address

    def consume(self, slot_ids: object, subslot_ids: object):
        url = self.base_address + '/consume'
        response = requests.post(url, json={'slot_ids': slot_ids,
                                            'subslot_ids': subslot_ids})
        print(response)


class SlotProducerClient():
    '''
    Client for slotserver's producer http endpoint
    '''
    def __init__(self, base_address):
        self.base_address = base_address

    def produce(self, slot_id: str, subslot_id: str, data: str):
        url = self.base_address + '/produce'
        requests.post(url, json={'slot_id': slot_id,
                                 'subslot_id': subslot_id,
                                 'data': data})
