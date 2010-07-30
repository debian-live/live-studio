import os
import sys
import time
import daemon
import shutil
import logging
import datetime
import tempfile
import subprocess

from daemon import pidlockfile

from django.conf import settings
from django.core.management.base import NoArgsCommand, make_option

from live_studio.build.models import Build
from live_studio.templatetags.text import command_line_options

def call(logfile, args):
    logfile.write('$ %s\n' % command_line_options(args))
    logfile.flush()
    subprocess.check_call(args, stdout=logfile, stderr=logfile)

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--pidfile', dest='pidfile', help="Pidfile", default=None),
    )

    def handle_noargs(self, **options):
        if options['pidfile']:
            pidfile = pidlockfile.PIDLockFile(options['pidfile'])
            daemon.DaemonContext(pidfile=pidfile).open()

        self.run(options)

    def run(self, options):
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

                update(started=datetime.datetime.now())

                tempdir = tempfile.mkdtemp(prefix='live-studio_')
                target_dir = os.path.join(settings.BUILDS_ROOT, build.ident)

                os.makedirs(target_dir)
                logfile = open(os.path.join(target_dir, 'log.txt'), 'a')

                self.log.info("Building #%d in %s", build.pk, tempdir)

                try:
                    os.chdir(tempdir)

                    call(logfile, ('lh', 'config') + build.config.options())

                    if settings.DEBUG:
                        open('binary.iso', 'w').write('iso here')
                    else:
                        call(logfile, ('lh', 'build'))

                    # Find file that was created
                    filename = None
                    for extension in ('iso', 'img'):
                        if not os.path.exists('binary.%s' % extension):
                            continue

                        filename = '%s.%s' % (build.ident, extension)
                        os.rename(
                            'binary.%s' % extension,
                            os.path.join(target_dir, filename),
                        )

                        break

                    assert filename, "Did not create any image"

                    update(
                        finished=datetime.datetime.now(),
                        filename=filename,
                    )

                    self.log.info("#%d built successfully", build.pk)
                except:
                    update(finished=datetime.datetime.now())
                    self.log.exception("#%d failed", build.pk)
                    continue
                finally:
                    os.chdir(tempdir)
                    call(logfile, ('lh', 'clean', '--purge'))
                    shutil.rmtree(tempdir)

                    self.log.info("Finished processing #%d", build.pk)

            except IndexError:
                self.log.debug('No items in queue, sleeping for 2s')
                try:
                    time.sleep(2)
                except KeyboardInterrupt:
                    sys.exit(1)
