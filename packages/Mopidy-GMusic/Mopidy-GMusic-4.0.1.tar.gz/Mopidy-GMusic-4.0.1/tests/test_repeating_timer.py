import logging
import unittest
from threading import Event

from mopidy_gmusic.repeating_timer import RepeatingTimer

logger = logging.getLogger(__name__)


class ExtensionTest(unittest.TestCase):
    def setUp(self):
        self._event = Event()

    def _run_by_timer(self):
        self._event.set()
        logger.debug("Tick.")

    def test_init(self):
        timer = RepeatingTimer(self._run_by_timer, 0.5)
        timer.start()
        assert self._event.wait(1), "timer was not running"
        self._event.clear()
        assert self._event.wait(1), "timer was not running"
        timer.cancel()

    def test_stop(self):
        timer = RepeatingTimer(self._run_by_timer, 10)
        timer.start()
        assert timer.is_alive(), "timer is not running"
        timer.cancel()
        timer.join(1)
        assert not timer.is_alive(), "timer is still alive"
