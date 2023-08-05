# Copyright (c) 2020 Hugh Wade
# SPDX-License-Identifier: MIT
import slotserver.slot_repository as sr
import slotserver.slot_service as ss
from flask import Flask, request, Blueprint, current_app
slotapp = Blueprint('slots', __name__, '/')

FAIL = ("Failure. When your best isn't good enough.", 500)
OK = ("Good job.", 200)


def create_app(*args):
    app = Flask(__name__)
    mode = None
    repo = None
    print(args)
    if args:
        mode = args[0]
    if not mode or mode == 'memory':
        repo = sr.MemorySlotRepository()
    elif(mode == 'pickle'):
        repo = sr.PickledSlotRepository('slotserver.pickle')
    app.p_service = ss.SlotProducerService(repo)
    app.c_service = ss.SlotConsumerService(repo)
    app.register_blueprint(slotapp)
    return app


@slotapp.route('/consume', methods=['POST'])
def consume():
    data = request.get_json(force=True, silent=True)
    if data:
        try:
            return (current_app.c_service.get_slotdata(data['slot_ids'],
                                                       data['subslot_ids']),
                    200)
        except Exception as ex:
            trace(ex)
            return FAIL
    else:
        return FAIL


@slotapp.route('/produce', methods=['POST'])
def produce():
    data = request.get_json(force=True, silent=True)
    if data:
        try:
            current_app.p_service.update_slot(data['slot_id'],
                                              data['subslot_id'],
                                              data['data'])
        except Exception as ex:
            trace(ex)
            return FAIL
        return OK
    else:
        return FAIL


def trace(msg: str):
    print(msg)
