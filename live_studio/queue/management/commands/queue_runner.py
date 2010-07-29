import time
import shutil
import datetime
import tempfile
import traceback

from django.core.management.base import NoArgsCommand

from live_studio.queue.models import Entry

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.verbose = int(options['verbosity']) > 1

        while True:
            try:
                entry = Entry.objects.pop()

                def update(**kwargs):
                    print entry.pk, kwargs
                    Entry.objects.filter(pk=entry.pk).update(**kwargs)

                update(started=datetime.datetime.utcnow())

                tempdir = tempfile.mkdtemp(prefix='live-studio_')

                try:
                    self.handle_entry(entry, tempdir)
                    update(success=True)
                except:
                    traceback.print_exc()
                    continue
                finally:
                    update(finished=datetime.datetime.utcnow())
                    shutil.rmtree(tempdir)

            except IndexError:
                time.sleep(2)

    def handle_entry(self, entry, tempdir):
        # Process 'entry' here
        pass
