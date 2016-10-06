class TimeUnit(object):
    def __init__(self, converter):
        self.converter = converter

    def as_minutes(self, t):
        return self.converter(t)


class Time(object):
    SECOND = TimeUnit(lambda t : t/60)
    MINUTE = TimeUnit(lambda t: t)
    HOUR   = TimeUnit(lambda t: t*60)

    def __init__(self, time, timeUnit):
        self.duration = timeUnit.as_minutes(time)

    def getValue(self):
        return self.duration
