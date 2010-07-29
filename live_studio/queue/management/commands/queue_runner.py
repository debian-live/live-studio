import time
import datetime

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

                try:
                    self.handle_entry(entry)
                    update(success=True)
                except:
                    continue
                finally:
                    update(finished=datetime.datetime.utcnow())

            except IndexError:
                time.sleep(2)

    def handle_entry(self, entry):
        # Process 'entry' here
        pass
