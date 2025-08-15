import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QProgressBar, QVBoxLayout
import pandas as pd


class ProgressBarWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.popUpDialog = QMessageBox()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)
        self.progress_bar.hide()

    def showPopUp(self, title='Something happen', text='Everything gonna be alright', icon=QMessageBox.Information):
        self.popUpDialog.setWindowTitle(title)
        self.popUpDialog.setText(text)
        self.popUpDialog.setIcon(icon)
        self.popUpDialog.show()

    def start(self, data, output_file, thread):
        # Sample DataFrame
        # self.data = read_json(json_file)
        self.df = pd.DataFrame(data)

        # Start the thread
        self.progress_bar.show()
        self.thread = thread(self.df, output_file)
        self.thread.start()
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.finished.connect(self.hide_progress)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def hide_progress(self):
        if self.progress_bar.value() == 100:
            self.progress_bar.hide()
            self.showPopUp('Operation Complete', 'File conversion complete, cheers!')
