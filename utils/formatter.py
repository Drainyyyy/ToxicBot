import datetime


def timedelta(delta: datetime.timedelta):
    return f"{delta.days}d {delta.seconds//3600:02d}h {delta.seconds//60:02d}m {delta.seconds % 60:02d}s"
