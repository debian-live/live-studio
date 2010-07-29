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

from live_studio.build.models import Build

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger('live-studio-runner')

        if int(options['verbosity']) > 1:
            self.log.setLevel(logging.DEBUG)

        while True:
            try:
                build = Build.objects.pop()

                def update(**kwargs):
                    self.log.debug('Updating #%d with %r', build.pk, kwargs)
                    Build.objects.filter(pk=build.pk).update(**kwargs)

                update(started=datetime.datetime.utcnow())
                tempdir = tempfile.mkdtemp(prefix='live-studio_')

                self.log.info("Building #%d in %s", build.pk, tempdir)

                try:
                    self.handle_build(build, tempdir)
                    update(finished=datetime.datetime.utcnow(), success=True)
                    self.log.info("#%d built successfully", build.pk)
                except:
                    update(finished=datetime.datetime.utcnow())
                    self.log.exception("#%d failed", build.pk)
                    continue
                finally:
                    self.clean(tempdir)
                    self.log.info("Finished processing #%d", build.pk)

            except IndexError:
                self.log.debug('No items in queue, sleeping for 2s')

                try:
                    time.sleep(2)
                except KeyboardInterrupt:
                    sys.exit(1)

    def handle_build(self, build, tempdir):
        os.chdir(tempdir)
        subprocess.check_call(('lh', 'config') + build.config.options())
        subprocess.check_call(('lh', 'build'))

    def clean(self, tempdir):
        os.chdir(tempdir)
        subprocess.call(('lh', 'clean', '--purge'))
        shutil.rmtree(tempdir)
