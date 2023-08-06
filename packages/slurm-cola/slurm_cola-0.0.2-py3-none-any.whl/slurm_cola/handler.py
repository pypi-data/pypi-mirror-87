import os
import subprocess
import sys

from subprocess import PIPE
from typing import Dict, List, Optional

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox


USERNAME = sys.argv[1] if len(sys.argv) == 2 else os.environ['USER']


class JobInterface(QObject):
    """This object is the only place talking to the system.
    The rest of the application deals with dictionaries objects.

    This object is designed to handle operations serially. Its architecture
    does not lend itself to parallelized operations.

    The motivation for this class to inherit QObject is to send log messages
    via signals to the logging window.
    """

    log = pyqtSignal(str)

    def list_jobs(self, mode: Optional[str] = None) -> Optional[Dict[str, Dict[str, str]]]:  # noqa
        """Check for jobs, and return a dictionary of
        {jobid (str): job_properties}.

        job_properties is also a dictionary that contains further information
        about the job, such as the notebook it runs, its dependencies (if any),
        node, and more."""
        self.log.emit('Listing jobs')

        cmd = f'squeue -u {USERNAME}'
        if mode is not None:
            cmd += f' -t {mode}'

        ret = subprocess.run(cmd.split(), stderr=PIPE, stdout=PIPE)

        if ret.returncode != 0:
            self.log.emit(f'An error occured:\n {ret.stderr}')
            return

        # The following tediously converts the space-separated csv output into
        # lists and gets the job ids. This is equivalent to
        # awk 'NR>1 { print $1 }'
        lines = [line.strip().split()
                 for line in ret.stdout.decode().splitlines()[1:]]
        job_ids = [line[0] for line in lines]

        self.log.emit(f'Retrieving information for {len(job_ids)} jobs')

        statuses = {}
        for job in job_ids:
            cmd = f'scontrol show jobid -dd {job}'
            ret = subprocess.run(cmd.split(), stderr=PIPE, stdout=PIPE)
            if ret.returncode != 0:
                if 'Invalid job id specified' not in ret.stderr:
                    self.log.emit(f'Getting details for {job} failed:\n {ret.stderr}')  # noqa
                continue

            # The output of show jobid is several lines of property=value
            # that is here converted to a dictionary.
            # There are 3 types of lines:
            # - 'JobState=RUNNING'
            # - 'TRES=cpu=72,node=1,billing=72'
            # - 'Power='
            # As such, we split on the first = sign, and what comes after is
            # either the value, or the empty string.
            # Slurm's representation of None is '(null)', which is also set to
            # the empty string.
            ret = [line.strip() for line in ret.stdout.decode().split() if line]  # noqa

            properties = {}
            for line in ret:
                try:
                    key, content = line.split('=', maxsplit=1)
                except ValueError:
                    continue  # meh. this key had no value anyway...
                if content == '(null)':
                    content = ''
                properties[key] = content

            statuses[job] = properties

        return statuses or None

    def cancel_jobs(self, jobs: List[str]):
        """Cancel all the given jobs"""
        self.log.emit(f'Cancelling job(s) {jobs}')

        ret = subprocess.run(['scancel', *jobs], stderr=subprocess.PIPE)

        if ret.returncode != 0:
            error = ret.stderr.decode()
            msg = f'There was an issue cancelling these jobs:\n{error}'
            self.log.emit(msg)
            QMessageBox.warning(self.parent(), 'Oops', msg)


# A poor man's singleton
handler = JobInterface()
del JobInterface
