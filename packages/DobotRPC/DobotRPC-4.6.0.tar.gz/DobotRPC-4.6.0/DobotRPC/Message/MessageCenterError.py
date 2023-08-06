# python3
# -*- encoding: utf-8 -*-
"""
@Author:
    JoMar Wu (sos901012@gmail.com)
@Create Time:
    2019-08-28 18:07:25
@License:
    Copyright © 2019 Shenzhen Yuejiang Co., Ltd.
@Desc:
    None
"""
from typing import List, Any


class MessageCenterError(Exception):
    pass


class IsNotMessageHandler(MessageCenterError):
    def __init__(self, obj: object):
        super().__init__(f"{obj} is not MessageHandler.")


class MustRegisterOrphan(MessageCenterError):
    def __init__(self):
        super().__init__("Must register orphan.")


class CannotFoundModule(MessageCenterError):
    def __init__(self, name: object):
        super().__init__(f"{name} can not found.")


class CannotFoundFunc(MessageCenterError):
    def __init__(self, name: object):
        super().__init__(f"{name} can not found.")


class InvalidMethodFormat(MessageCenterError):
    def __init__(self, method: object):
        super().__init__(f"{method}")


class CanNotFoundCallback(MessageCenterError):
    def __init__(self, callback_id: object):
        super().__init__(f"callback({callback_id}) can not found.")


class InvaildCallback(MessageCenterError):
    def __init__(self, obj: object):
        super().__init__(f"objest({obj}) is not callable.")


class InvaildParams(MessageCenterError):
    def __init__(self, args: List[Any]):
        super().__init__(f"{args} is invaild params.")


class CannotFoundMethod(MessageCenterError):
    pass