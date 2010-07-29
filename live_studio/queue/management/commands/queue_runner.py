import time
import shutil
import logging
import datetime
import tempfile
import traceback

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
                    shutil.rmtree(tempdir)
                    self.log.info("Finished processing #%d", entry.pk)

            except IndexError:
                self.log.debug('No items in queue, sleeping for 2s')
                time.sleep(2)

    def handle_entry(self, entry, tempdir):
        # Process 'entry' here
        pass
