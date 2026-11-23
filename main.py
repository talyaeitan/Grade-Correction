from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QSpinBox,
    QTableWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QFileDialog
)
from about import AboutWindow
import os
import sys
import subprocess

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
        self.load_button.clicked.connect(self.load_file_clicked)
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
        self.bonus_spin.editingFinished.connect(self.bonus_entered)

        self.update_button = QPushButton("Update File")
        self.update_button.clicked.connect(self.update_file_clicked)

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

    def load_file_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Grades File", "", "CSV Files (*.csv)")
        if file_path == "":
            return

        self.selected_file = file_path
        self.file_label.setText(file_path)

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        with open(self.selected_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        self.header_line = lines[0].strip()

        for line in lines[1:]:
            clean_line = line.strip()
            if clean_line != "":
                parts = clean_line.split(",")
                student_id = parts[0].strip()
                grade = int(float(parts[1].strip()))

                self.student_ids.append(student_id)
                self.original_grades.append(grade)
                self.corrected_grades.append(grade)

        self.update_table()
        self.status_label.setText("הקובץ נטען בהצלחה.")

    def update_table(self):
        self.table.setRowCount(len(self.student_ids))
        for i in range(len(self.student_ids)):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.student_ids[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.original_grades[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.corrected_grades[i])))

    def bonus_entered(self):
        if len(self.original_grades) == 0:
            self.status_label.setText("יש לטעון קובץ ציונים תחילה.")
            return

        bonus = self.bonus_spin.value()
        self.corrected_grades = []

        for orig_grade in self.original_grades:
            new_grade = orig_grade + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades.append(new_grade)

        self.update_table()
        self.status_label.setText(f"חושבו ציונים מתוקנים עם תוספת של {bonus} נקודות.")
    
    def update_file_clicked(self):
        if self.selected_file == "":
            self.status_label.setText("לא נבחר קובץ לעדכון.")
            return

        with open(self.selected_file, "w", encoding="utf-8") as f:
            f.write(self.header_line + "\n")
            for i in range(len(self.student_ids)):
                f.write(f"{self.student_ids[i]},{self.corrected_grades[i]}\n")

        self.status_label.setText("הקובץ עודכן ונפתח.")

        if sys.platform == "win32":
            os.startfile(self.selected_file)
        elif sys.platform == "darwin":
            subprocess.run(["open", self.selected_file])
        else:
            subprocess.run(["xdg-open", self.selected_file])

    def about_clicked(self):
        self.about_window.show()

    def closeEvent(self, event):
        self.about_window.close()


if __name__ == "__main__":
    app = QApplication()
    window = GradesWindow()
    window.show()
    app.exec()