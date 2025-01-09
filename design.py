import sys
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QLineEdit, QFormLayout
from PySide6.QtCore import QTimer
from logic import Worker
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor")
        self.setGeometry(100, 100, 400, 250)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.cpu_label = QLabel("CPU Usage: 0%")
        self.memory_label = QLabel("Memory Usage: 0%")
        self.disk_label = QLabel("Disk Usage: 0%")

        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.memory_label)
        self.layout.addWidget(self.disk_label)

        self.start_button = QPushButton("Начать запись")
        self.stop_button = QPushButton("Остановить")
        self.stop_button.setVisible(False)

        self.timer_label = QLabel("Время записи: 0 сек")
        self.timer_label.setVisible(False)

        self.interval_input = QLineEdit()
        self.interval_input.setPlaceholderText("Время обновления (сек)")
        self.interval_input.setText("1")

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.button_layout.addWidget(self.timer_label)

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Интервал обновления:", self.interval_input)

        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.button_layout)

        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        self.worker = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.db = Database()
        self.elapsed_seconds = 0


    def start_recording(self):
        """Начало записи."""
        interval = max(1, int(self.interval_input.text()))
        self.start_button.setVisible(False)
        self.stop_button.setVisible(True)
        self.timer_label.setVisible(True)
        self.timer.start(interval * 1000)
        self.worker = Worker(interval=interval)
        self.worker.update_signal.connect(self.update_labels)
        self.worker.start()
        self.elapsed_seconds = 0


    def stop_recording(self):
        """Конец записи."""
        self.start_button.setVisible(True)
        self.stop_button.setVisible(False)
        self.timer_label.setVisible(False)
        self.timer.stop()
        self.worker.stop()
        self.worker.wait()
        self.timer_label.setText("Время записи: 0 сек")


    def update_labels(self, cpu_usage, memory_usage, disk_usage):
        """Обновление данных."""
        self.cpu_label.setText(f"CPU Usage: {cpu_usage:.2f}%")
        self.memory_label.setText(f"Memory Usage: {memory_usage:.2f}%")
        self.disk_label.setText(f"Disk Usage: {disk_usage:.2f}%")

        self.db.insert_data(cpu_usage, memory_usage, disk_usage)


    def update_timer(self):
        """Обновление таймера."""
        interval = max(1, int(self.interval_input.text()))
        self.elapsed_seconds += interval
        self.timer_label.setText(f"Время записи: {self.elapsed_seconds} сек")
