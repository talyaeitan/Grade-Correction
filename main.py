from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QSpinBox,
    QTableWidget, QVBoxLayout, QHBoxLayout
)
from about import AboutWindow


class GradesWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''
        self.header_line = ""

        self.about_window = AboutWindow()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Grades File Updater")
        self.setGeometry(150, 150, 520, 560)

        self.title_label = QLabel("Grades Updater")
        self.title_label.setObjectName("title")

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.about_clicked)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.about_button)

        self.load_button = QPushButton("Load Grades File")
        self.file_label = QLabel("No file selected")

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.load_button)
        file_layout.addWidget(self.file_label)
        file_layout.addStretch()

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])

        self.bonus_label = QLabel("Bonus Points (press Enter):")
        self.bonus_spin = QSpinBox()
        self.bonus_spin.setRange(0, 100)

        self.update_button = QPushButton("Update File")

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.bonus_label)
        bottom_layout.addWidget(self.bonus_spin)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.update_button)

        self.status_label = QLabel("")
        self.status_label.setObjectName("status")

        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addLayout(file_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(bottom_layout)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def about_clicked(self):
        self.about_window.show()

    def closeEvent(self, event):
        self.about_window.close()


if __name__ == "__main__":
    app = QApplication()
    window = GradesWindow()
    window.show()
    app.exec()