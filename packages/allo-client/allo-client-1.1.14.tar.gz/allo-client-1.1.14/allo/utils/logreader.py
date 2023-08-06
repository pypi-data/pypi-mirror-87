import threading
import os
import time

import progressbar
from allo.model.colors import BColors


class LogReader(threading.Thread):
    def __init__(self, threadid, filename, progress):
        threading.Thread.__init__(self)
        self.threadID = threadid
        self.filename = filename
        self._stop_event = threading.Event()
        self.progress = progress
        self.bar = None
        self._release = ""
        self.release_mode = False
        self.failed = False

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def follow(self):
        """
        generator function that yields new lines in a file
        """
        # seek the end of the file
        self.logfile.seek(0, os.SEEK_END)

        first_line = True
        # start infinite loop
        while True:
            if self.stopped():
                return
            # read last line of file
            line = self.logfile.readline()
            # sleep if file hasn't been updated
            if not line:
                if self.stopped():
                    return
                if self.bar is not None:
                    self.bar.update(1)
                time.sleep(0.1)
                continue
            if first_line:
                first_line = False
            if not self.have_to_handle_special_line(line):
                yield line

    def have_to_handle_special_line(self, line):
        handled = False
        if self.bar is not None:
            if "RELEASE_END" in line:
                self.release_mode = False
                handled = True
            elif "RELEASE" in line:
                self.release_mode = True
                handled = True
            elif "RESCUE" in line:
                self.bar.finish(end=BColors.error(" Erreur de mise à jour. Restauration en cours...\n", False))
                self.failed = True
                handled = True
            elif "FAILED" in line:
                self.bar.finish(end=BColors.error(" ERREUR CRITIQUE\n", False))
                self.failed = True
                handled = True
            elif self.release_mode:
                self._release = self._release + line
                handled = True
            else:
                self.bar.finish(end=BColors.success(" OK\n", False))
                if "ENDED" in line:
                    BColors.success("Mise à jour terminée")
                    self.stop()
                    handled = True
        return handled

    def run(self):
        while not os.path.exists(self.filename):
            if self.stopped():
                return
            time.sleep(1)

        self.logfile = open(self.filename, "r")
        loglines = self.follow()
        # iterate over the generator
        for line in loglines:
            if self.progress:
                self.bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength, widgets=[
                    line.rstrip() + " ", progressbar.AnimatedMarker()
                ])
            else:
                print(line, end="")

        if not self.failed and self._release:
            BColors.info("Note de version - Informations supplémentaires: ")
            print(self._release)
