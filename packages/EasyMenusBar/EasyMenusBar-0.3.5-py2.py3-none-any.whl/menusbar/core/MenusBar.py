#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QWidget, QFileSystemModel, QTreeView, QAction, QMenu, QVBoxLayout, QAbstractItemView, \
    QShortcut
from PySide2 import QtCore, QtGui
from PySide2.QtCore import QMargins, QFileInfo, QUrl, Qt
from PySide2.QtGui import QMouseEvent, QDesktopServices, QKeySequence
from menusbar.core.FileUtils import FileUtils
from .Dialog import Dialog as MKDialog
import json
import os


class MemusBar(QWidget):
    handlerAfterSignal = QtCore.Signal(int, str)
    handlerBeforeSignal = QtCore.Signal(int, str)
    openFileSignal = QtCore.Signal(QFileInfo)

    HANLDER_CREATE_DIR = 0
    HANLDER_DELETE_DIR = 1
    HANLDER_CREATE_FILE = 2
    HANLDER_DELETE_FILE = 3

    def __init__(self, parent=None, settingFileName: str = "setting.json"):
        QWidget.__init__(self, parent)
        self.settingFileName = settingFileName
        self.init()
        self._initUI()
        self.initEvent()

    def init(self):
        self.filtersList = list()
        self.isLive = False
        self.workDir = None
        self.defualtSuffix = 'md'
        self.defualtSuffixList = None
        self.settingFileSavePath = None
        self.fileUtils = FileUtils()
        self.SP_KEY_WORKDIR = "lastWorkDirRecord"
        self.defaultContent: list = None

    def checkWorkDir(self) -> bool:
        if self.workDir and os.path.exists(self.workDir) and os.path.isdir(self.workDir):
            return True
        else:
            return False

    def createDir(self, value):
        if self.checkWorkDir():
            self.fileUtils.createDir(self.workDir, value)
        else:
            raise RuntimeError('This workd dir is not init')

    def createFile(self, value):
        if self.checkWorkDir():
            self.fileUtils.createFile(self.workDir, value, self.defaultContent)
        else:
            raise RuntimeError('This workd dir is not init')

    def initEvent(self):
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_D), self)
        shortcut.activated.connect(self.deleteShortcutEvent)

        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_K), self)
        shortcut.activated.connect(self.createFileShortcutEvent)

        shortcut = QShortcut(QKeySequence(Qt.SHIFT + Qt.CTRL + Qt.Key_K), self)
        shortcut.activated.connect(self.createDirShortcutEvent)

    def createDirShortcutEvent(self):
        if self.isLive == False:
            return
        fileInfo = self.treeModel.fileInfo(self.treeView.currentIndex())
        text = MKDialog().inputDirNameDialog()
        if text:
            if self._handlerBeforeEvent(self.HANLDER_CREATE_DIR, os.path.join(self.getDir(fileInfo), text)):
                self.fileUtils.createDir(self.getDir(fileInfo), text)
                self._handlerAfterEvent(self.HANLDER_CREATE_DIR, os.path.join(self.getDir(fileInfo), text))

    def createFileShortcutEvent(self):
        if self.isLive == False:
            return
        fileInfo = self.treeModel.fileInfo(self.treeView.currentIndex())
        text = MKDialog().inputFileNameDialog()
        temp = str(text).split(".")
        if len(temp) < 2:
            text = text + "." + self.defualtSuffix
        else:
            fileSuffix = temp[len(temp) - 1]
            if self.defualtSuffixList:
                if fileSuffix not in self.defualtSuffixList:
                    text = text + "." + self.defualtSuffix
            elif self.defualtSuffix and self.defualtSuffix != fileSuffix:
                text = text + "." + self.defualtSuffix
        if text:
            if self._handlerBeforeEvent(self.HANLDER_CREATE_FILE, os.path.join(self.getDir(fileInfo), text)):
                self.fileUtils.createFile(self.getDir(fileInfo), text)
                self._handlerAfterEvent(self.HANLDER_CREATE_FILE, os.path.join(self.getDir(fileInfo), text))

    def deleteShortcutEvent(self):
        if self.isLive == False:
            return
        fileInfo = self.treeModel.fileInfo(self.treeView.currentIndex())
        if fileInfo.isFile():
            if self._handlerBeforeEvent(self.HANLDER_DELETE_FILE, fileInfo.filePath()):
                self.fileUtils.deleteFile(fileInfo.filePath())
                self._handlerAfterEvent(self.HANLDER_DELETE_FILE, fileInfo.filePath())
        else:
            if self._handlerBeforeEvent(self.HANLDER_DELETE_DIR, fileInfo.filePath()):
                self.fileUtils.deleteDir(fileInfo.filePath())
                self._handlerAfterEvent(self.HANLDER_DELETE_DIR, fileInfo.filePath())

    def getSettingSavePath(self):
        if not self.settingFileSavePath:
            self.settingFileSavePath = self.fileUtils.getProjectPath()
        return self.settingFileSavePath

    def getSettingFile(self):
        if not os.path.exists(os.path.join(self.getSettingSavePath(), self.settingFileName)):
            with open(os.path.join(self.getSettingSavePath(), self.settingFileName), mode='w')  as _:
                pass
        with open(os.path.join(self.getSettingSavePath(), self.settingFileName), mode='r') as jsonFile:
            try:
                data = json.load(jsonFile)
                return data
            except Exception as e:
                print(e)
                return {}

    def saveSettingFile(self, setting):
        with open(os.path.join(self.getSettingSavePath(), self.settingFileName), mode='w') as jsonFile:
            json.dump(setting, jsonFile)

    def getLastWorkDirRecord(self):
        setting: dict = self.getSettingFile()
        if self.SP_KEY_WORKDIR in setting.keys():
            return setting[self.SP_KEY_WORKDIR]
        else:
            return os.environ['HOME']

    def updateWorkDirRecord(self, value) -> str:
        setting = self.getSettingFile()
        setting[self.SP_KEY_WORKDIR] = value
        self.saveSettingFile(setting)
        return value

    def initWorkDir(self, workDir: str = None, settingFilePath: str = None):
        if settingFilePath:
            self.settingFileSavePath = settingFilePath
        if not workDir:
            workDir = self.getLastWorkDirRecord()
        self.updateWorkDir(workDir=workDir)

    def updateWorkDir(self, workDir: str):
        self.updateWorkDirRecord(workDir)
        self.workDir = workDir
        self.treeModel.setRootPath(self.workDir)
        self.treeView.setRootIndex(self.treeModel.index(self.workDir))
        self.filtersList.clear()
        if self.defualtSuffixList:
            for s in self.defualtSuffixList:
                self.filtersList.append("*.%s" % s)
        else:
            self.filtersList.append("*.%s" % self.defualtSuffix)
        self.treeModel.setNameFilters(self.filtersList)



    def _initUI(self):
        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))

        self.treeModel = QFileSystemModel(self)
        self.treeModel.setReadOnly(False)
        self.treeView = QTreeView(self)
        self.treeView.setDragDropMode(QAbstractItemView.InternalMove)
        self.treeView.setDragEnabled(True)
        self.treeView.setAcceptDrops(True)
        self.treeView.setDropIndicatorShown(True)
        self.setMinimumHeight(100)
        self.treeView.setModel(self.treeModel)
        self.treeView.setSortingEnabled(True)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        self.treeView.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)
        self.mainLayout.addWidget(self.treeView, 1)
        self.setLayout(self.mainLayout)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            # 是否按下左键
            index = self.treeView.indexAt(event.pos())
            if index.isValid():
                fileInfo = self.treeModel.fileInfo(index)
                self.openFileSignal.emit(fileInfo)
        else:
            event.accept()

    def showContextMenu(self, pos):
        index = self.treeView.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            action = QAction(menu)
            action.setObjectName("create_dir")
            action.setProperty("pos", pos)
            action.setText("创建目录")
            action.triggered.connect(self.actionHandler)
            menu.addAction(action)

            action = QAction(menu)
            action.setObjectName("delete_dir")
            action.setProperty("pos", pos)
            action.setText("删除目录")
            action.triggered.connect(self.actionHandler)
            menu.addAction(action)

            action = QAction(menu)
            action.setObjectName("create_file")
            action.setProperty("pos", pos)
            action.setText("创建文件")
            action.triggered.connect(self.actionHandler)
            menu.addAction(action)

            action = QAction(menu)
            action.setObjectName("delete_file")
            action.setProperty("pos", pos)
            action.setText("删除文件")
            menu.addAction(action)
            action.triggered.connect(self.actionHandler)

            action = QAction(menu)
            action.setObjectName("reveal_resources")
            action.setProperty("pos", pos)
            action.setText("打开资源")
            menu.addAction(action)
            action.triggered.connect(self.actionHandler)

            menu.exec_(self.treeView.mapToGlobal(pos))

    def handlerBeforeEvent(self, type: int, filePath: str) -> bool:
        return True

    def _handlerBeforeEvent(self, type: int, filePath: str) -> bool:
        self.handlerBeforeSignal.emit(type, filePath)
        return self.handlerBeforeEvent(type, filePath)

    def _handlerAfterEvent(self, type: int, filePath: str):
        self.handlerAfterSignal.emit(type, filePath)
        self.handlerAfterEvent(type, filePath)

    def handlerAfterEvent(self, type: int, filePath: str):
        pass

    def actionHandler(self):
        if not self.checkWorkDir():
            raise RuntimeError('This workd dir is not init')

        type = self.sender().objectName()
        fileInfo = self.treeModel.fileInfo(self.treeView.currentIndex())
        # print(fileInfo.fileName())
        # print(fileInfo.filePath())
        # print(fileInfo.path())
        # print(fileInfo.isRoot())
        file = fileInfo.filePath()
        if type == "create_dir":
            text = MKDialog().inputDirNameDialog()
            if text:
                if self._handlerBeforeEvent(self.HANLDER_CREATE_DIR, os.path.join(self.getDir(fileInfo), text)):
                    self.fileUtils.createDir(self.getDir(fileInfo), text)
                    self._handlerAfterEvent(self.HANLDER_CREATE_DIR, os.path.join(self.getDir(fileInfo), text))

        elif type == "delete_dir":
            if self._handlerBeforeEvent(self.HANLDER_DELETE_DIR, fileInfo.filePath()):
                self.fileUtils.deleteDir(fileInfo.filePath())
                self._handlerAfterEvent(self.HANLDER_DELETE_DIR, fileInfo.filePath())

        elif type == "create_file":
            text = MKDialog().inputFileNameDialog()
            temp = str(text).split(".")
            if len(temp) < 2:
                text = text + "." + self.defualtSuffix
            else:
                fileSuffix = temp[len(temp) - 1]
                if self.defualtSuffixList:
                    if fileSuffix not in self.defualtSuffixList:
                        text = text + "." + self.defualtSuffix
                elif self.defualtSuffix and self.defualtSuffix != fileSuffix:
                    text = text + "." + self.defualtSuffix
            if text:
                if self._handlerBeforeEvent(self.HANLDER_CREATE_FILE, os.path.join(self.getDir(fileInfo), text)):
                    self.fileUtils.createFile(self.getDir(fileInfo), text)
                    self._handlerAfterEvent(self.HANLDER_CREATE_FILE, os.path.join(self.getDir(fileInfo), text))

        elif type == "delete_file":
            if self._handlerBeforeEvent(self.HANLDER_DELETE_FILE, file):
                self.fileUtils.deleteFile(file)
                self._handlerAfterEvent(self.HANLDER_DELETE_FILE, file)
        elif type == "reveal_resources":
            url = QUrl("file:%s" % self.getDir(fileInfo), QUrl.TolerantMode)
            QDesktopServices.openUrl(url)

    def getDir(self, fileInfo: QFileInfo):
        if fileInfo.isFile():
            return fileInfo.path()
        else:
            return fileInfo.filePath()

    def setSupportFileSuffix(self, suffix: list, defualtSuffix: str):
        self.defualtSuffixList = suffix
        self.defualtSuffix = defualtSuffix

    def enterEvent(self, event: QtCore.QEvent):
        self.isLive = True

    def leaveEvent(self, event: QtCore.QEvent):
        self.isLive = False
