import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from .handler import handler
from .informations import JobWindow
from .logwindow import LogWindow
from .mainwindow import MainWindow


def main():
    """The application's entry point.

    This creates the Qt application, and connects all slots and signals.
    After that, it will automatically look for jobs of this username, and list
    them within the main window.
    """

    app = QApplication(sys.argv)

    window = QMainWindow()
    main_window = MainWindow(window)

    job_window = JobWindow()
    main_window.display_request.connect(job_window.show)
    main_window.update_request.connect(job_window.update)

    log = LogWindow()
    main_window.pbLog.clicked.connect(log.display)
    handler.log.connect(log.log)

    # Display the main window, through its parent.
    window.show()

    log.log('Launched')
    main_window.list_jobs()

    sys.exit(app.exec_())
