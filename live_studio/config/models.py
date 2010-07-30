import datetime

from django.db import models
from django.contrib.auth.models import User

from live_studio import data

class Config(models.Model):
    user = models.ForeignKey(User, related_name='configs')
    created = models.DateTimeField(default=datetime.datetime.now)

    name = models.CharField(
        max_length=150,
        default='Untitled configuration',
    )

    base = models.CharField(
        max_length=8,
        default='standard',
        choices=(
            ('standard',    'Standard Debian GNU/Linux image'),
            ('gnome',       'GNOME desktop environment'),
            ('kde',         'KDE desktop environment'),
            ('xfce',        'Xfce desktop environment'),
            ('rescue',      'Debian GNU/Linux rescue image'),
        ),
    )

    distribution = models.CharField(
        max_length=7,
        default='lenny',
        choices=(
            ('lenny',   'Debian GNU/Linux 5.0 ("lenny")'),
            ('squeeze', 'Debian GNU/Linux testing distribution ("squeeze")'),
            ('sid',     'Debian GNU/Linux unstable distribution ("sid")'),
        ),
    )

    media_type = models.CharField(
        max_length=7,
        default='iso',
        choices=(
            ('iso',     'ISO image for a CD or DVD'),
            ('usb-hdd', 'USB / HDD image'),
        )
    )

    architecture = models.CharField(
        max_length=5,
        default='i386',
        choices=(
            ('i386',  'i386 (x86_32)'),
            ('amd64', 'amd64 (x86_64)'),
        )
    )

    installer = models.CharField(
        max_length=4,
        default='no',
        choices=(
            ('no',   'No installer integration'),
            ('live', '"Live" installer integration'),
            ('yes',  'Standard installer integration'),
        )
    )

    locale = models.CharField(
        default='en_US.UTF-8',
        max_length=30,
        choices=data.LOCALES,
    )

    keyboard_layout = models.CharField(
        default='us',
        max_length=20,
        choices=data.KEYBOARD_LAYOUTS,
    )

    def __unicode__(self):
        return "%s: name=%s" % (self.user.username, self.name)

    @models.permalink
    def get_absolute_url(self):
        return 'config:view', (self.pk,)

    def options(self):
        try:
            language = self.locale.split('_')[0]
        except:
            language = 'en'

        return (
            '--architecture', self.architecture,
            '--packages-lists', self.base,
            '--distribution', self.distribution,
            '--binary-images', self.media_type,
            '--debian-installer', self.installer,
            '--language', language,
            '--bootappend-live',
                'locale=%s keyb=%s' % (self.locale, self.keyboard_layout),
        )
