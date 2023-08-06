#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

payload = '{"ee":{"entities":[{"reqId":"123456","intent":"requestToken","clientId":\
        "homeass_nbhQ43","username":"homeassistant_user","name":"HA User",\
        "role":3,"entities":[{"aa":"bb"},{"aa":"cc"}]}]}}'


class BasicRequest:
    def __init__(self, reqId, intent):
        self.reqId = reqId
        self.intent = reqId
        self.reqId = reqId


class BasicEntity:
    def __init__(self):
        pass


class DeviceEntity(BasicEntity):
    def __init__(self):
        pass


# class RequestTokenReq:
# def __init__(self,

# print(payload)


def decode_p(d):
    print("11111sdfsadfasdfasdf")
    print(d)
    if "entities" in d:
        if type(d["entities"]) == list:
            print("yes, it's list", len(d["entities"]))
        print(d["entities"])
        print("got entities", d["entities"])
        return d["entities"]
    if "reqId" in d:
        return d["reqId"]
    return d


br = BasicRequest("sdfsdfd", "sync")
# print(json.dumps(br.__dict__))
# print(payload)
obj = json.loads(payload, object_hook=decode_p)
print(obj)
# print(obj['ee'])
# json.loads(payload, object_pairs_hook=decode_p)
