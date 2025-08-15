import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

def set_widget_to_top(widget):
    # Get the desktop geometry
    desktop = QApplication.desktop()

    # Get the screen resolution
    screen_width = desktop.screenGeometry().width()
    screen_height = desktop.screenGeometry().height()

    # Calculate the top position
    top_position = 0

    # Set the widget's geometry
    widget.setGeometry(0, top_position, 120, 120)

# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Top of Screen Widget")
    window.setWindowIcon(QIcon("icon.png"))

    # Set the widget to the top of the screen
    set_widget_to_top(window)

    window.show()
    sys.exit(app.exec_())