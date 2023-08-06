# python3
# -*- encoding: utf-8 -*-
"""
@Author:
    JoMar Wu (sos901012@gmail.com)
@Create Time:
    2019-10-24 16:47:51
@License:
    Copyright © 2019 Shenzhen Yuejiang Co., Ltd.
@Desc:
    None
"""

import json
import demjson
import websockets
import asyncio
from websockets import WebSocketServerProtocol
from .Utils import loggers
from .Message import message_center as mc
from typing import Any, NoReturn
from . import NetworkError

LOGGER_NAME = "RPCServer"


class RPCServer(object):
    def __init__(self,
                 loop: asyncio.BaseEventLoop,
                 ip="0.0.0.0",
                 port=9091,
                 on_disconnected=None,
                 on_connected=None):
        if on_disconnected is not None and not callable(on_disconnected):
            raise Exception("on_disconnected should callable")
        if on_connected is not None and not callable(on_connected):
            raise Exception("on_connected should callable")

        self.__on_disconnected = on_disconnected
        self.__on_connected = on_connected
        self.__loop: asyncio.BaseEventLoop = loop
        self.__server_name = "DobotRPC-WSServer"

        self.__ban_list = (
            # "192.168.53.103",
            # "192.168.53.100"
        )
        self.__ws_clients = set()

        self.__rpc_id = 0
        self.__coroutines = {}
        self.__tasks = []
        self.__server = None

        self.__sender_ws = None

        async def init_worker() -> Any:
            nonlocal ip, port
            self.__server = await websockets.serve(self.__on_new_onnection, ip,
                                                   port)

        self.__loop.run_until_complete(init_worker())

    def __del__(self):
        if self.__server and self.__loop.is_running():
            self.__server.close()
            self.__server.wait_closed()
            del self.__server

        self.__coroutines.clear()

    @property
    def current_sender(self):
        '''
        @desc: 谨慎使用
        '''
        if self.__sender_ws:
            return self.__sender_ws.remote_address
        else:
            return None

    async def __call_worker(self, websocket, rpc_id, method, **params) -> None:
        try:
            self.__sender_ws = websocket
            rpc_result = await mc.call(method, **params)
            feedback = self.__pack_rpc(rpc_id, rpc_result)
        except Exception as e:
            feedback = self.__pack_rpc(rpc_id, e)

        address = f"{websocket.host}:{websocket.port}"
        remote_address = f"{websocket.remote_address[0]}:\
{websocket.remote_address[1]}"

        loggers.get(LOGGER_NAME).debug(
            f"S({address}) >> C({remote_address}): {feedback}")
        await websocket.send(feedback)

    async def __on_new_onnection(self, websocket: WebSocketServerProtocol,
                                 _) -> NoReturn:
        ip, port = websocket.remote_address
        address = f"{websocket.host}:{websocket.port}"
        remote_address = f"{ip}:{port}"

        if ip in self.__ban_list:
            loggers.get(LOGGER_NAME).warning(f"{ip} had been baned.")
            send_str = "You had been baned."

            loggers.get(LOGGER_NAME).debug(
                f"S({address}) >> C({remote_address}): {send_str}")
            await websocket.send(send_str)
            return

        loggers.get(LOGGER_NAME).info(f"Client({ip}:{port}) connected.")
        self.__ws_clients.add(websocket)

        if self.__on_connected:
            result = self.__on_connected(websocket.remote_address)
            if asyncio.iscoroutine(result):
                await result

        while True:
            try:
                message = await websocket.recv()
                loggers.get(LOGGER_NAME).debug(
                    f"S({address}) << C({remote_address}): {message}")
            except Exception as e:
                loggers.get(LOGGER_NAME).error(e, exc_info=True)
                break

            try:
                # result和error字段暂时不使用
                # 因为作为服务端不主动调用客户端
                rpc_id, method, params, _, _ = self.__unpack_rpc(message)

                if "dobotlink" not in method:
                    # dobotlink的数据尽管透传
                    method = self.__convert_lower_case_name(method)
                    params = self.__convert_lower_case_params(params)

                self.__loop.create_task(
                    self.__call_worker(websocket, rpc_id, method, **params))
            except Exception as e:
                loggers.get(LOGGER_NAME).error(e, exc_info=True)
                loggers.get(LOGGER_NAME).debug(
                    f"S({address}) >> C({remote_address}): {e}")
                await websocket.send(str(e))
                continue

        loggers.get(LOGGER_NAME).warning(
            f"{ip}:{port} had disconnected!!!!!!!!")
        self.__ws_clients.remove(websocket)

        if self.__on_disconnected:
            result = self.__on_disconnected(websocket.remote_address)
            if asyncio.iscoroutine(result):
                await result

    def __unpack_rpc(self, message: str) -> (int, str, str, str, Exception):
        try:
            data = json.loads(message)
        except Exception as e:
            raise NetworkError.InvaildJsonMsg(e)

        rpc_id = data.get("id", None)
        if type(rpc_id) is not int:
            raise NetworkError.RpcIdInvaild()

        rpc_verison = data.get("jsonrpc", None)
        if rpc_verison != "2.0":
            raise NetworkError.RpcVersionInvaild()

        method = data.get("method", None)
        params = data.get("params", None)
        result = data.get("result", None)
        error = data.get("error", None)
        if error:
            error = Exception(error)

        return rpc_id, method, params, result, error

    def __pack_rpc(self, rpc_id: int, rpc_playload: Any,
                   method: str = None) -> str:
        if rpc_id is None:
            data = {"jsonrpc": "2.0"}
        else:
            data = {"id": rpc_id, "jsonrpc": "2.0"}

        if method:
            data["method"] = method
            data["params"] = rpc_playload
        else:
            if isinstance(rpc_playload, Exception):
                # TODO: 所有异常捕捉并处理
                error_str = str(rpc_playload)
                if "code" in error_str:
                    rpc_playload = demjson.decode(error_str)
                else:
                    rpc_playload = {"code": -32000, "message": f"{error_str}"}
                loggers.get(LOGGER_NAME).error(rpc_playload, exc_info=True)
                data["error"] = rpc_playload
            else:
                data["result"] = rpc_playload

        rpc_packet = json.dumps(data)
        return rpc_packet

    def __convert_lower_case_name(self, name):
        lst = []
        last_char_flag = False
        for char in name:
            if last_char_flag and char.isupper():
                lst.append("_")
            lst.append(char)

            if char == ".":
                last_char_flag = False
            else:
                last_char_flag = True

        return "".join(lst).lower()

    def __convert_lower_case_params(self, params):
        params = {} if params is None else params
        new_params = {}
        for key, value in params.items():
            key = self.__convert_lower_case_name(key)
            new_params[key] = value

        return new_params

    @property
    def is_connected(self) -> bool:
        return len(self.__ws_clients) != 0

    async def notify(self, method: str, data: Any) -> Any:
        if self.is_connected is False:
            return
            # raise Exception("Had not connected!")

        rpc_packet = self.__pack_rpc(None, data, method)
        tasks = []
        for websocket in self.__ws_clients:
            address = f"{websocket.host}:{websocket.port}"
            remote_address = f"{websocket.remote_address[0]}:\
{websocket.remote_address[1]}"
            loggers.get(LOGGER_NAME).debug(
                f"S({address}) >> C({remote_address}): {rpc_packet}")
            tasks.append(websocket.send(rpc_packet))
        await asyncio.wait(tasks)

    def register(self, module_name: str, module: object) -> None:
        """
        @Create Time:
            2019-09-04 15:58:51
        @Desc:
            1. 注册模块到消息中心
            2. 模块对象挂在MC的对象树中
        @param {module_name: str}:
            模块名字
        @param {module: object}:
            模块对象
        @return {}:
            None
        """
        mc.register(module_name, module)

    def remove(self, module_name: str) -> None:
        """
        @Create Time:
            2019-09-04 15:58:51
        @Desc:
            1. 从消息中心删除模块对象
            2. 从MC的对象树中删除模块对象
        @param {module_name: str}:
            模块名字
        @return {}:
            None
        """
        mc.remove(module_name)
