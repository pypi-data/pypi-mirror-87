from zuper_commons.ui import duration_compact


def test_duration1():
    duration_compact(0.001)
    duration_compact(0.01)
    duration_compact(0.1)
    duration_compact(1)
    duration_compact(10)
    duration_compact(60)
    duration_compact(61.2)
    duration_compact(100)
    duration_compact(1000)
    duration_compact(10000)
    duration_compact(100000)
    duration_compact(1000000)
    duration_compact(100000000)
