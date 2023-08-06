#!/usr/bin/env python
# -*- coding: utf-8 -*-

class StatusFlag:
    Start = "start"
    End = "end"
    Process = "process"


class HandlerStatusInfo:
    flag: str = None
    msg: str = None
    value: float = 0

    def __init__(self, flag: str = None, msg: str = None, value: float = 0):
        self.flag = flag
        self.msg = msg
        self.value = value
