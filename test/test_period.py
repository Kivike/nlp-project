import unittest
import time
from app.time.period import Period

class TestHeapMap(unittest.TestCase):

    def test_captures_values_properly(self):
        """Test values are captured properly during initialization and ending.
        """
        period = Period()

        # Assert that the values have 3 same decimals
        self.assertAlmostEqual(period.start, time.time(), 3)
        self.assertEqual(period.duration, None)
        self.assertEqual(period.finish, None)

        duration = period.end()

        self.assertAlmostEqual(time.time(), period.finish, 2)
        self.assertEqual(duration, period.duration)
        self.assertNotEqual(period.duration, None)

    def test_formats_seconds_properly(self):
        """Test that the duration in seconds is formatted properly.
        """
        period = Period()

        # 1 minute, 12 seconds
        value1 = 72.0

        # 3 hours, 47 minutes, 28 seconds
        value2 = 3 * 60 * 60.0 + 47 * 60 + 28.0

        # 1 hour, 1 minute, 1 second
        value3 = 1 * 60 * 60.0 + 1 * 60 + 1

        self.assertEqual(period.format(value1), '1 minute 12 seconds')
        self.assertEqual(period.format(value2), '3 hours 47 minutes 28 seconds')
        self.assertEqual(period.format(value3), '1 hour 1 minute 1 second')


if __name__ == '__main__':
    unittest.main()