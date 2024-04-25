from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys, os


def find_mdm_files(folder_path):
    mdm_files = []  # Создаем пустой список для хранения путей к .mdm файлам

    # Используем os.walk() для рекурсивного обхода всех файлов и папок в указанной директории
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".mdm"):  # Проверяем, что файл имеет расширение .mdm (регистронезависимо)
                mdm_files.append(os.path.join(root, file))  # Добавляем путь к .mdm файлу в список

    return mdm_files

def parse_mdm_filename(path):

    filename = path.split('\\')[-1]

    sections = filename.split("~")  # Разделяем название файла по символу "~"
    keys = ["chip_number", "transistor_type", "characteristic", "temperature", "radiation_intensity"]
    parsed_info = dict(zip(keys, sections))  # Создаем словарь из ключей и значений

    # Исключаем расширение файла из значений температуры и интенсивности радиации
    parsed_info["temperature"] = parsed_info["temperature"].split(".")[0]
    if "radiation_intensity" in parsed_info:
        parsed_info["radiation_intensity"] = parsed_info["radiation_intensity"].split(".")[0]
    parsed_info["path"] = path
    return parsed_info

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.knopka.triggered.connect(self.loadFolder)
    
    def loadFolder(self):
        path = QFileDialog.getExistingDirectory()
        files = find_mdm_files(path)
        label = "\n".join(str(d) for d in [parse_mdm_filename(i) for i in files])
        self.label_2.setText(label)
        self.label_2.setWordWrap(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec())