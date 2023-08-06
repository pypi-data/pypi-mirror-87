#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QStatusBar, QProgressBar


class StatusCenter:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StatusCenter, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.init()

    def init(self):
        self.statusBar: QStatusBar = None

    def setStatusBar(self, statusBar: QStatusBar):
        self.statusBar = statusBar

    def pushStatus(self):
        progressBar = QProgressBar()
        progressBar.setValue(10)
        self.statusBar.addWidget(progressBar)


statusCenter = StatusCenter()
