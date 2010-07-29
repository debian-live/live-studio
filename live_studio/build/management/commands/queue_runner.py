import os
import sys
import time
import shutil
import logging
import datetime
import tempfile
import traceback
import subprocess

from django.core.management.base import NoArgsCommand

from live_studio.queue.models import Entry

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger('live-studio-runner')

        if int(options['verbosity']) > 1:
            self.log.setLevel(logging.DEBUG)

        while True:
            try:
                entry = Entry.objects.pop()

                def update(**kwargs):
                    self.log.debug('Updating #%d with %r', entry.pk, kwargs)
                    Entry.objects.filter(pk=entry.pk).update(**kwargs)

                update(started=datetime.datetime.utcnow())
                tempdir = tempfile.mkdtemp(prefix='live-studio_')

                self.log.info("Building #%d in %s", entry.pk, tempdir)

                try:
                    self.handle_entry(entry, tempdir)
                    update(finished=datetime.datetime.utcnow(), success=True)
                    self.log.info("Entry #%d built successfully", entry.pk)
                except:
                    update(finished=datetime.datetime.utcnow())
                    self.log.exception("Entry #%d failed", entry.pk)
                    continue
                finally:
                    self.clean(tempdir)
                    self.log.info("Finished processing #%d", entry.pk)

            except IndexError:
                self.log.debug('No items in queue, sleeping for 2s')

                try:
                    time.sleep(2)
                except KeyboardInterrupt:
                    sys.exit(1)

    def handle_entry(self, entry, tempdir):
        os.chdir(tempdir)
        subprocess.check_call(('lh', 'config') + entry.config.options())
        subprocess.check_call(('lh', 'build'))

    def clean(self, tempdir):
        os.chdir(tempdir)
        subprocess.call(('lh', 'clean', '--purge'))
        shutil.rmtree(tempdir)
