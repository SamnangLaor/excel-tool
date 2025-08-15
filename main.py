import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from converter import ConverterApp
from csv_splitter import SplitterApp


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = '🇰🇭 CSV file utility'
        self.left = 0
        self.top = 0
        self.width = 520
        self.height = 200
        self.setWindowTitle(self.title)
        self.set_widget_to_horizontal_center()

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()

    def set_widget_to_horizontal_center(self):
      # Get the desktop geometry
      desktop = QApplication.desktop()

      # Get the screen resolution
      screen_width = desktop.screenGeometry().width()
      screen_height = desktop.screenGeometry().height()

      # Calculate the center point horizontally
      center_x = int(screen_width / 2)

      # Set the widget's geometry
      self.setGeometry(center_x - int(self.width / 2), self.top, self.width, int(screen_height/4))


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = ConverterApp()
        self.tab2 = SplitterApp()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Converter")
        self.tabs.addTab(self.tab2,"Splitter")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())