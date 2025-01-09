import time
import psutil

from PySide6.QtCore import QThread, Signal


class Worker(QThread):
    update_signal = Signal(float, float, float)


    def __init__(self, interval):
        """Инициализация класса."""
        super().__init__()
        self.interval = interval
        self.running = True
    

    def run(self):
        """Выполнение потока и получение данных."""
        while self.running:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            self.update_signal.emit(cpu_usage, memory_usage, disk_usage)
            time.sleep(self.interval)
    

    def stop(self):
        """Остановка выполнения потока."""
        self.running = False
