from PySide2 import QtCore
import rx


class PySild2QtScheduler(QtCore.QObject):
    _instance = None
    call = QtCore.Signal(object)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PySild2QtScheduler, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def initSignal(self):
        self.call.connect(self.onUICall)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self)

    @QtCore.Slot(object)
    def onUICall(self, method):
        method()

    def QtScheduler(self):
        def _Scheduler(source):
            def subscribe(observer, scheduler=None):
                def on_next(value):
                    qtScheduler.call.emit(lambda: observer.on_next(value))

                def on_completed():
                    qtScheduler.call.emit(lambda: observer.on_completed())

                def on_error(error):
                    qtScheduler.call.emit(lambda: observer.on_error(error))

                return source.subscribe(
                    on_next,
                    on_error,
                    on_completed,
                    scheduler)

            return rx.create(subscribe)
        return _Scheduler


qtScheduler = PySild2QtScheduler()
