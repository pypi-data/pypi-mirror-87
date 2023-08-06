import sys

from collections import defaultdict
from typing import Dict, List, Tuple

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QRect, Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QCheckBox, QListWidget, QListWidgetItem,
                             QMessageBox, QPushButton)

from .handler import handler, USERNAME


class MainWindow(QObject):
    """MainWindow is the entry point of slurm-cola.
    It contains a list of jobs for this user.
    """
    display_request = pyqtSignal(str, object)
    update_request = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        parent.setObjectName('mainWindow')
        parent.setWindowTitle(f'Slurm-Cola Job Administation for {USERNAME}')
        parent.resize(800, 600)

        self._timer = QTimer(parent=self)
        self._timer.setInterval(3 * 1000)
        self._timer.timeout.connect(self.list_jobs)

        lwJobs = QListWidget(parent)
        lwJobs.setObjectName('jobList')
        lwJobs.setGeometry(QRect(20, 30, 760, 470))
        lwJobs.setFont(QFont('monospace'))
        lwJobs.itemDoubleClicked.connect(self.check_item)
        lwJobs.currentItemChanged.connect(self.on_currentItemChanged)
        self.lwJobs = lwJobs

        cbAutoRefresh = QCheckBox(parent)
        cbAutoRefresh.setObjectName('cbAutoRefresh')
        cbAutoRefresh.setGeometry(QRect(20, 540, 100, 40))
        cbAutoRefresh.setText('Auto Refresh')
        cbAutoRefresh.setToolTip('Refresh every 3 seconds')
        cbAutoRefresh.stateChanged.connect(self.on_cbAutoRefresh_clicked)

        pbRefresh = QPushButton(parent)
        pbRefresh.setObjectName('pbRefresh')
        pbRefresh.setGeometry(QRect(120, 540, 100, 40))
        pbRefresh.setText('Refresh')
        pbRefresh.setToolTip(f"Rescan {USERNAME} jobs")
        pbRefresh.clicked.connect(self.list_jobs)

        pbProperties = QPushButton(parent)
        pbProperties.setObjectName('pbProperties')
        pbProperties.setGeometry(QRect(260, 540, 100, 40))
        pbProperties.setText('Properties')
        pbProperties.setToolTip("The selected job's properties")
        pbProperties.clicked.connect(self.on_pbProperties_clicked)

        pbCancel = QPushButton(parent)
        pbCancel.setObjectName('pbCancel')
        pbCancel.setGeometry(QRect(400, 540, 100, 40))
        pbCancel.setText('Cancel jobs')
        pbCancel.setToolTip('Cancel checked jobs')
        pbCancel.clicked.connect(self.on_pbCancel_clicked)

        pbLog = QPushButton(parent)
        pbLog.setObjectName('pbLog')
        pbLog.setGeometry(QRect(540, 540, 100, 40))
        pbLog.setText('View Logs')
        self.pbLog = pbLog

        pbQuit = QPushButton(parent)
        pbQuit.setObjectName('pbQuit')
        pbQuit.setGeometry(QRect(680, 540, 100, 40))
        pbQuit.setText('Quit')
        pbQuit.clicked.connect(sys.exit)

        # self.jobs is set in self.list_jobs()
        self.jobs: Dict[str: Dict[str, str]] = None

    def list_jobs(self):
        self.lwJobs.clear()
        self.jobs = handler.list_jobs()

        if self.jobs is None:
            self.lwJobs.addItem(f'Nothing running for {USERNAME} now')
            return

        # Group jobs by their name.
        # This step is required as jobs belonging together are not necessarily
        # allocated together: it might be that a job launches a related job
        # at a later point.
        groups: Dict[str, List[Tuple[int, Dict[str, str]]]] = defaultdict(list)
        for job_id, properties in self.jobs.items():
            groups[properties['JobName']].append((job_id, properties))

        for group in groups.values():
            for job_id, properties in group:
                line = job_id + '    '
                line += properties['JobState'].ljust(12)
                line += properties['StartTime'].ljust(22)
                line += properties['RunTime'].ljust(12)
                line += properties['NodeList'].ljust(14)
                line += properties['JobName']

                item = QListWidgetItem()
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                item.setText(line)

                self.lwJobs.addItem(item)
            self.lwJobs.addItem('')  # Add a blank line between groups

    @pyqtSlot(QListWidgetItem)
    def check_item(self, item: QListWidgetItem):
        if not item.text():
            return  # FIXME: make textless items uncheckable
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    @pyqtSlot(QListWidgetItem)
    def open_properties(self, item: QListWidgetItem):
        if item is None or not item.text() or 'Nothing running' in item.text():
            return

        job = item.text().split()[0]
        properties = self.jobs[job]

        self.display_request.emit(job, properties)

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_currentItemChanged(self, current: QListWidgetItem, previous: QListWidgetItem):  # noqa
        if current is None or not current.text() or 'Nothing running' in current.text():  # noqa
            return

        job = current.text().split()[0]
        properties = self.jobs[job]

        self.update_request.emit(job, properties)

    def on_pbProperties_clicked(self):
        item = self.lwJobs.currentItem()
        if item is None:
            item = self.lwJobs.item(0)
        self.open_properties(item)

    def on_pbCancel_clicked(self):
        selection = []
        for idx in range(self.lwJobs.count()):
            item = self.lwJobs.item(idx)
            if item.checkState() == Qt.Checked:
                selection.append(item.text().split()[0])

        if not selection:
            return

        msg = f'You are about to cancel {len(selection)} jobs, continue?'
        ret = QMessageBox.warning(self.parent(), 'Confirmation', msg,
                                  QMessageBox.Cancel | QMessageBox.Yes,
                                  QMessageBox.Cancel)
        if ret == QMessageBox.Cancel:
            return

        handler.cancel_jobs(selection)

        # Refresh the list
        ticking = self._timer.isActive()
        self._timer.stop()

        self.list_jobs()

        if ticking:
            self._timer.start()

    @pyqtSlot(int)
    def on_cbAutoRefresh_clicked(self, state):
        if state == Qt.Checked:
            self._timer.start()
        else:
            self._timer.stop()
