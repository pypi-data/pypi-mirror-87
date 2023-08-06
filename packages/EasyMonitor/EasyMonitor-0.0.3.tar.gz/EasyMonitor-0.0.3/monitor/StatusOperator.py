#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rx
from .Status import StatusFlag, HandlerStatusInfo
from PySide2.QtCore import Signal, QObject


class StatusOperator(QObject):
    startSignal = Signal(None)
    endSignal = Signal(None)
    processChangeSignal = Signal(HandlerStatusInfo)

    StatusUnkown = 0
    StatusStart = 1
    StatusDoing = 2
    StatusEnd = 3

    def __init__(self):
        QObject.__init__(self)
        self.currentStatus = -1

    def operator(self):
        def _Scheduler(source):
            def subscribe(observer, scheduler=None):
                def on_next(value):
                    if isinstance(value, HandlerStatusInfo):
                        value: HandlerStatusInfo = value
                        if StatusFlag.Start == value.flag:
                            self.currentStatus = self.StatusStart
                            self.startSignal.emit()
                        elif StatusFlag.End == value.flag:
                            self.currentStatus = self.StatusEnd
                            self.endSignal.emit()
                        elif StatusFlag.Process == value.flag:
                            self.currentStatus = self.StatusDoing
                            self.processChangeSignal.emit(value)
                    else:
                        observer.on_next(value)

                def on_completed():
                    if self.currentStatus != self.StatusEnd:
                        self.currentStatus = self.StatusEnd
                        self.endSignal.emit()
                    observer.on_completed()

                def on_error(error):
                    if self.currentStatus != self.StatusEnd:
                        self.currentStatus = self.StatusEnd
                        self.endSignal.emit()
                    observer.on_error(error)

                return source.subscribe(
                    on_next,
                    on_error,
                    on_completed,
                    scheduler)

            return rx.create(subscribe)

        return _Scheduler
