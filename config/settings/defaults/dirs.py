from os.path import dirname, join, abspath

LIVE_STUDIO_BASE = dirname(dirname(dirname(dirname(abspath(__file__)))))

TEMPLATE_DIRS = (
    join(LIVE_STUDIO_BASE, 'templates'),
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join(LIVE_STUDIO_BASE, 'media')
