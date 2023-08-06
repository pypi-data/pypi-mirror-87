#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .StatusOperator import StatusOperator, HandlerStatusInfo
from .dialog.LoadingHitDialog import LoadingHitDialog
from PySide2.QtCore import QObject


class DialogStatusOperator(QObject):
    def __init__(self):
        self.statusOperator = StatusOperator()
        self.statusOperator.startSignal.connect(self.startLoginHit)
        self.statusOperator.endSignal.connect(self.endLoginHit)
        self.statusOperator.processChangeSignal.connect(self.handlerProcessChange)

    def startLoginHit(self):
        LoadingHitDialog.getInstance().show("登录中，请稍后。。。")

    def endLoginHit(self):
        LoadingHitDialog.getInstance().hide()

    def handlerProcessChange(self, value: HandlerStatusInfo):
        LoadingHitDialog.getInstance().updateProgressvalue(value.value)
        if value.msg and value.msg != "":
            LoadingHitDialog.getInstance().updateHitMessage(value.msg)

    def operator(self):
        return self.statusOperator.operator()
