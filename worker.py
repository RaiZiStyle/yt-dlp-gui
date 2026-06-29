from PySide6.QtCore import QObject, Signal, Slot


class Worker(QObject):
    finished = Signal()
    result = Signal(object)
    error = Signal(Exception)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.result.emit(result)
        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()