import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QInputDialog,
    QLineEdit,
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QPushButton,
    QGridLayout,
    QErrorMessage,
    QMessageBox
)
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
import pandas as pd


VALIDATION_ERROR = 'Validation Error'

class SplitterApp(QWidget):

    def __init__(self):
        super().__init__()
        self.title = '🇰🇭 CSV file splitter'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.fileNameInput = QLineEdit(self)
        self.filePathInput = QLineEdit(self)
        self.rowSizeInput = QLineEdit(self)
        self.errorDialog = QErrorMessage(self)
        self.popUpDialog = QMessageBox(self)
        self.btnBox = QDialogButtonBox()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(270*2, 120)

        dlgLayout = QVBoxLayout()
        # Create a form layout and add widgets
        gridLayout = QGridLayout()
        gridLayout.addWidget(QLabel("File Name:"), 0,0)
        gridLayout.addWidget(self.fileNameInput, 0,1)

        # Row: 1
        btnBrowse = QPushButton('Browse')
        btnBrowse.clicked.connect(self.openFileNameDialog)
        gridLayout.addWidget(btnBrowse, 0,2)

        # Row: 2
        gridLayout.addWidget(QLabel("File Path:"), 1,0)
        gridLayout.addWidget(self.filePathInput, 1,1)

        # Row: 3
        gridLayout.addWidget(QLabel("#Row / File:"), 2,0)
        gridLayout.addWidget(self.rowSizeInput, 2,1)
        reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QRegExpValidator(reg_ex, self.rowSizeInput)
        self.rowSizeInput.setValidator(input_validator)

        # Row: 4
        gridLayout.addWidget(QLabel("All right reserve Ⓒ Sagittech Inc."), 3,1)

        # Add a button box
        self.btnBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        # On OK clicked
        self.btnBox.accepted.connect(self.doSplittingFile)

        #On Cancel clicked
        self.btnBox.rejected.connect(self.closeApp)

        # Set the layout on the dialog
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addWidget(self.btnBox)

        #
        self.errorDialog.setWindowModality(Qt.WindowModal)

        self.setLayout(dlgLayout)
        self.center()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"File explorer", "","All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            print(fileName)
            head, tail = os.path.split(fileName)
            self.fileNameInput.setText(tail)
            self.filePathInput.setText(head)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def showPopUp(self, title='Something happen', text='Everything gonna be alright', icon=QMessageBox.Information):
        self.popUpDialog.setWindowTitle(title)
        self.popUpDialog.setText(text)
        self.popUpDialog.setIcon(icon)
        self.popUpDialog.show()

    def doSplittingFile(self):
        print('Starting ...')
        button = self.btnBox.button(QDialogButtonBox.Ok)
        button.setEnabled(False)

        if self.rowSizeInput.text() == '':
            self.showPopUp(VALIDATION_ERROR, '#Row / File: field is required.', QMessageBox.Warning)
            button.setEnabled(True)
            return

        if self.fileNameInput.text() == '':
            self.showPopUp(VALIDATION_ERROR, 'No file is inputted or chosen', QMessageBox.Warning)
            button.setEnabled(True)
            return

        if not self.fileNameInput.text().endswith('.csv'):
            self.showPopUp(VALIDATION_ERROR, 'Only CSV file is allowed', QMessageBox.Warning)
            button.setEnabled(True)
            return

        try:
            input_file = os.path.join(self.filePathInput.text(), self.fileNameInput.text())

            #get the number of lines of the csv file to be read
            number_lines = sum(1 for row in (open(input_file)))

            #size of rows of data to write to the csv,
            row_size = int(self.rowSizeInput.text())

            #start looping through data writing it to a new file for each set
            new_directory = os.path.join(os.path.dirname(input_file), self.fileNameInput.text().split('.')[0])
            os.makedirs(new_directory, exist_ok=True)

            for i in range(1,number_lines,row_size):
                df = pd.read_csv(input_file,
                    header=None,
                    nrows=row_size,#number of rows to read at each loop
                    skiprows=i,
                    dtype = str)#skip rows that have been read
                #csv to write data to a new file with indexed name. input_1.csv etc.
                out_csv = os.path.join(new_directory, os.path.splitext(self.fileNameInput.text())[0] + '__' + str(i) + '.csv')
                df.to_csv(out_csv,
                    index=False,
                    header=False,
                    mode='a', #append data to csv file
                    chunksize=row_size) #size of data to append for each loop

            self.showPopUp('For your information', 'Splitting completed, cheers !!!')

        except Exception as err:
            self.showPopUp('Error', str(err), QMessageBox.Critical)

        button.setEnabled(True)

    def closeApp(self):
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SplitterApp()
    sys.exit(app.exec_())
