import contextlib
import functools
import sys

from .tecutil_connector import _tecutil_connector, _tecutil


@contextlib.contextmanager
def lock(with_recording=True):
    """
    ParentLockStart takes a boolean: ShutdownImplicitRecording
    ShutdownImplicitRecording = True -> No recording
    ShutdownImplicitRecording = False -> With Recording
    """
    lock.FORCE_RECORDING = getattr(lock, 'FORCE_RECORDING', False)
    if _tecutil_connector.connected:
        yield
    else:
        _tecutil.ParentLockStart(not (with_recording or lock.FORCE_RECORDING))
        try:
            yield
        finally:
            _tecutil.handle.tecUtilParentLockFinish()


@contextlib.contextmanager
def force_recording():
    """Do not disable implicit recording when locking the engine."""
    if lock.FORCE_RECORDING:
        yield
    else:
        try:
            lock.FORCE_RECORDING = True
            yield
        finally:
            lock.FORCE_RECORDING = False


if sys.version_info < (3, 3):
    """
    This allows the contextmanager lock
    to be used as a decorator as well as a
    context. (This is already included in Py 3.3+)
    """
    _lock = lock

    class lock(object):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self._cm = _lock

        def __enter__(self, *args, **kwargs):
            self.cm = self._cm(*self.args, **self.kwargs)
            return self.cm.__enter__(*args, **kwargs)

        def __exit__(self, *args, **kwargs):
            return self.cm.__exit__(*args, **kwargs)

        def __call__(self, func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with self._cm(*self.args, **self.kwargs):
                    return func(*args, **kwargs)

            return wrapper
