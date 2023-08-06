#!/usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
import ssl
import http

h1 = http.client.HTTPSConnection(
    "192.168.2.121", context=ssl._create_unverified_context()
)
# h1.request(
# "POST",
# "/v1/tokens:request",
# '{"reqId":"123456","intent":"requestToken","clientId":"homeass_nbhQ43","username":"homeassistant_user","name":"HA User","role":3}'
# )
# r1 = h1.getresponse()
# print(r1.status, r1.reason)


def on_message(ws, message):
    print("%s", message)
    # print('to {"intent":"pong"}')
    ws.send('{"intent":"pong"}')
    print('{"intent":"pong"}')


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("on close")


def on_open(ws):
    print("on open")
    ws.send('{"intent":"ping"}')


# websocket.enableTrace(True)
ws = websocket.WebSocketApp(
    "wss://192.168.2.117/ws/json?clientId=homeass_nbhQ43&username=homeassistant_user&token=09addbafd811485382b03ff97021bcf3",
    on_message=on_message,
    on_error=on_error,
    on_open=on_open,
    on_close=on_close,
)
# ws.connect("wss://192.168.2.121/ws/json?clientId=homeass_nbhQ43&username=homeassistant_user&token=09addbafd811485382b03ff97021bcf3",
# on_message = on_message,
# on_error = on_error,
# on_close = on_close)
# ws.on_open = on_open
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
