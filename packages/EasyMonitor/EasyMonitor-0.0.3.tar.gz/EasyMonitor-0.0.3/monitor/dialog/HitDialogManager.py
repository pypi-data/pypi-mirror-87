#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QMessageBox, QErrorMessage
from PySide2.QtCore import QSize


class HitDialogManager:
    _instance = None
    _object = None

    @classmethod
    def getInstance(cls):
        if not cls._object:
            cls._object = HitDialogManager()
        return cls._object

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HitDialogManager, cls).__new__(
                cls, *args, **kwargs)

        return cls._instance

    def createMessageBox(self, title: str = "温馨提示", content: str = "", justYes: bool = True) -> QMessageBox:
        msgBox = QMessageBox()
        size = QSize()
        msgBox.setFixedSize(size)
        msgBox.setText(title)
        msgBox.setInformativeText(content)
        if justYes:
            msgBox.setStandardButtons(QMessageBox.Yes)
        else:
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        return msgBox
