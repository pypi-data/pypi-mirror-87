"""detect_sharpWaveRipples - detect sharp wave ripple events from electrophysiological data"""

__version__ = '\0.1.0'
__author__ = 'Demetris Roumis <roumis.d+package@gmail.com>'
__all__ = []

# logging
# adding NullHandler() to prevent log messages if the user does not want to see them
# see http://docs.python-guide.org/en/latest/writing/logging/#logging-in-a-library
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
