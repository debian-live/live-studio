import os
import sys
import time
import shutil
import logging
import datetime
import tempfile
import subprocess

from django.conf import settings
from django.core.management.base import NoArgsCommand

from live_studio.build.models import Build
from live_studio.templatetags.text import command_line_options

def call(logfile, args):
    logfile.write('# %s\n' % command_line_options(args))
    p = subprocess.Popen(args, stdout=logfile, stderr=logfile)
    p.wait()
    assert p.returncode == 0

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
                target_dir = os.path.join(settings.BUILDS_ROOT, build.ident)

                os.makedirs(target_dir)
                logfile = open(os.path.join(target_dir, 'log.txt'), 'a')

                self.log.info("Building #%d in %s", build.pk, tempdir)

                try:
                    filename = self.handle_build(build, tempdir, target_dir, logfile)

                    update(
                        finished=datetime.datetime.utcnow(),
                        filename=filename,
                    )

                    self.log.info("#%d built successfully", build.pk)
                except:
                    update(finished=datetime.datetime.utcnow())
                    self.log.exception("#%d failed", build.pk)
                    continue
                finally:
                    self.clean(tempdir, logfile)
                    self.log.info("Finished processing #%d", build.pk)

            except IndexError:
                self.log.debug('No items in queue, sleeping for 2s')
                try:
                    time.sleep(2)
                except KeyboardInterrupt:
                    sys.exit(1)

    def handle_build(self, build, tempdir, target_dir, logfile):
        os.chdir(tempdir)

        call(logfile, ('lh', 'config') + build.config.options())
        open('binary.iso', 'w').write('iso here') #call(logfile, ('lh', 'build'))

        for extension in ('iso', 'img'):
            if not os.path.exists('binary.%s' % extension):
                continue

            filename = '%s.%s' % (build.ident, extension)
            os.rename(
                'binary.%s' % extension,
                os.path.join(target_dir, filename),
            )

            return filename

        assert False, "Did not create any image"

    def clean(self, tempdir, logfile):
        os.chdir(tempdir)
        call(logfile, ('lh', 'clean', '--purge'))
        shutil.rmtree(tempdir)
