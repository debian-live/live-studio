import time

from django.core.management.base import NoArgsCommand

from live_studio_www.queue.models import Entry

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.verbose = int(options['verbosity']) > 1

        while True:
            try:
                # Pop
                entry = Entry.objects.all()[0]
                self.handle_entry(entry)
            except IndexError:
                time.sleep(2)

    def handle_entry(self, entry):
        # Process 'entry' here
        pass
