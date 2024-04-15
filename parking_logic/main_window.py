import sys, os
from subprocess import call
from dataclasses import dataclass

from main_autopark import MainAutopark
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QWidget, QFormLayout, QComboBox, QDial, QCheckBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Система автоматической парковки")
        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.x_edit = QLineEdit(self)
        self.x_edit.setInputMask("00")
        layout.addRow("Стартовая позиция X:", self.x_edit)

        self.y_edit = QLineEdit(self)
        self.y_edit.setInputMask("00")
        layout.addRow("Стартовая позиция Y:", self.y_edit)

        self.psi_edit = QLineEdit(self)
        self.psi_edit.setInputMask("000")
        layout.addRow("Стартовый угол автомобиля:", self.psi_edit)

        self.parking_slot_chooser = QComboBox()
        for i in range(1, 25):
            self.parking_slot_chooser.addItem(str(i))
        layout.addRow("Парковочное место №", self.parking_slot_chooser)

        self.add_more_walls_flag = QCheckBox()
        layout.addRow("Добавить дополнительные препятствия", self.add_more_walls_flag)

        self.parking_btn = QPushButton("Рассчитать траекторию движения по парковке")
        self.parking_btn.clicked.connect(self.calculate_parking_process)
        layout.addRow(self.parking_btn)

        self.parking_btn = QPushButton("Показать данные предыдущего выполнения")
        self.parking_btn.clicked.connect(self.show_image_data)
        layout.addRow(self.parking_btn)

        widget.setLayout(layout)

        self.show()
    
    
    def calculate_parking_process(self):
        args = Arguments(x_start=int(self.x_edit.text()),
                         y_start=int(self.y_edit.text()),
                         psi_start=int(self.psi_edit.text()),
                         parking=int(self.parking_slot_chooser.currentText()),
                         add_more_walls=self.add_more_walls_flag.isChecked())
        
        MainAutopark(args)

    def show_image_data(self):
        current_working_directory = os.getcwd()
        target = current_working_directory + "/log_results"
        call(["open", target])

@dataclass
class Arguments:
    x_start: int = 0
    y_start: int = 90
    x_end: int = 90
    y_end: int = 80
    parking: int = 1
    add_more_walls: bool = False
    psi_start: int = 0


app = QApplication(sys.argv)
window = MainWindow()
app.exec()
