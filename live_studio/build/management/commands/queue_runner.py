import os
import sys
import time
import shutil
import logging
import datetime
import tempfile
import subprocess

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.management.base import NoArgsCommand, make_option
from django.contrib.sites.models import Site

from live_studio.build.models import Build
from live_studio.templatetags.text import command_line_options

def call(logfile, args):
    logfile.write('$ %s\n' % command_line_options(args))
    logfile.flush()
    subprocess.check_call(args, stdout=logfile, stderr=logfile)

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--pidfile', dest='pidfile', help="Pidfile", default=None),
        make_option('--logfile', dest='logfile', help="Log file", default=None),
    )

    def handle_noargs(self, **options):
        if options['pidfile']:
            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0) # Exit first parent.
            except OSError, e:
                print >>sys.stderr, "fork #1 failed: (%d) %s" % (e.errno, e.strerror)
                sys.exit(1)

            # Decouple from parent environment.
            os.chdir('/')
            os.umask(0)
            os.setsid()

            # Do second fork.
            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0)
            except OSError, e:
                print >>sys.stderr, "fork #2 failed: (%d) %s" % (e.errno, e.strerror)
                sys.exit(1)

            # Redirect standard file descriptors.
            si = open('/dev/null', 'r')
            so = open('/dev/null', 'a+')
            se = open('/dev/null', 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

            f = open(options['pidfile'], 'a+')
            f.write(str(os.getpid()))
            f.close()

        logging.basicConfig(filename=options['logfile'], level=logging.INFO)
        self.log = logging.getLogger('live-studio-runner')

        if int(options['verbosity']) > 1:
            self.log.setLevel(logging.DEBUG)

        while True:
            try:
                self.run()
            except Exception:
                self.log.exception("Caught exception")

    def run(self):
        try:
            build = Build.objects.pop()
        except IndexError:
            self.log.debug('No items in queue, sleeping for 2s')

            try:
                time.sleep(2)
            except KeyboardInterrupt:
                sys.exit(1)

            return

        def update(**kwargs):
            self.log.debug('Updating #%d with %r', build.pk, kwargs)
            Build.objects.filter(pk=build.pk).update(**kwargs)

            # Also set attributes on the local object so the are up to date
            for k, v in kwargs.iteritems():
                setattr(build, k, v)

        update(started=datetime.datetime.now())

        tempdir = tempfile.mkdtemp(prefix='live-studio_')
        target_dir = os.path.join(settings.BUILDS_ROOT, build.ident)

        os.makedirs(target_dir)
        logfile = open(os.path.join(target_dir, 'log.txt'), 'a')

        self.log.info("Building #%d in %s", build.pk, tempdir)

        try:
            filename = self.build(build, tempdir, logfile, target_dir)

            status = 'success'
            self.log.info("#%d built successfully", build.pk)

            update(
                filename=filename,
                finished=datetime.datetime.now(),
            )

        except:
            status = 'failure'
            self.log.error("#%d failed to build", build.pk)
            update(finished=datetime.datetime.now())
            raise

        finally:
            os.chdir(tempdir)
            call(logfile, ('lh', 'clean', '--purge'))
            shutil.rmtree(tempdir)

            context = {
                'site': Site.objects.get_current(),
                'build': build,
            }

            subject = render_to_string(
                'builds/%s_subject.txt' % status,
                context,
            )

            send_mail(
                ''.join(subject.splitlines()),
                render_to_string('builds/%s_body.txt' % status, context),
                settings.DEFAULT_FROM_EMAIL,
                (build.config.user.email,),
            )

            self.log.info("Finished processing #%d", build.pk)

    def build(self, build, tempdir, logfile, target_dir):
        os.chdir(tempdir)

        call(logfile, ('lh', 'config') + build.config.options())

        if settings.DEBUG:
            open('binary.iso', 'w').write('iso here')
        else:
            call(logfile, ('lh', 'build'))

        # Find file that was created, if any
        filename = None
        for extension in ('iso', 'img'):
            if not os.path.exists('binary.%s' % extension):
                continue

            filename = 'Debian_Live_Studio_%s.%s' % (build.ident, extension)

            os.rename(
                'binary.%s' % extension,
                os.path.join(target_dir, filename),
            )

            return filename

        assert False, "Did not create any image"
