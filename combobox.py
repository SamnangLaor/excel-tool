from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox
)


class ConversionChoicesWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.comboBox = QComboBox()
        self.choices = ['CSV', 'XLSX', 'JSON']
        self.comboBox.addItems(self.choices)
        self.comboBox.activated.connect(self.check_index)

        layout.addWidget(self.comboBox)
        self.setLayout(layout)

    def check_index(self):
        cindex = self.comboBox.currentIndex()

        return cindex

    def current_text(self): # We receive the index, but don't use it.
        ctext = self.comboBox.currentText()

        return ctext

    def remove_item(self, index):
        #Reload items before remove
        self.comboBox.clear()
        self.comboBox.addItems(self.choices)

        # Remove item
        self.comboBox.removeItem(index)

