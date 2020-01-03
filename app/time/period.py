import time

class Period:
    """Class describing a period of time.
    """

    start = None

    finish = None

    duration = None

    def __init__(self, manual_start = False):
        """Crete a new period of time.
        
        Keyword Arguments:
    
            manual_start {bool} -- Whether to start the period manually by calling `.begin()` (default: {False})
        """
        if not manual_start:
            self.start = time.time()

    def begin(self):
        """Begin the time period. Note that this is nod needed unless you've
        specified manual starting in constructor argument.
        """
        self.start = time.time()

    def end(self) -> float:
        """End the period.
        
        Returns:
            float -- The period duration in seconds
        """
        self.finish = time.time()
        self.duration = self.finish - self.start
        return self.duration
    
    def __str__(self):
        if self.duration is not None:
            return self.format(self.duration)
        return 'period not ended'

    def format(self, duration: float) -> str:
        """Format the given duration in seconds into a human readable string.
        
        Arguments:

            duration {float} -- The duration in seconds
        
        Returns:

            str -- Human readable string describing the duration
        """
        h = 0
        m = 0
        s = 0

        if duration % 3600 > 0:
            h = int(duration / 3600)
            duration = duration % 3600
        if duration % 60 > 0:
            m = int(duration / 60)
            duration = duration % 60
        s = int(duration)

        second = 'second' if s == 1 else 'seconds'
        output = '{} {}'.format(s, second)

        if m > 0:
            minute = 'minute' if m == 1 else 'minutes'
            output = '{} {} {}'.format(m, minute, output)
        if h > 0:
            hour = 'hour' if h == 1 else 'hours'
            output = '{} {} {}'.format(h, hour, output)
        
        return output
