import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QFileDialog,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QPushButton,
    QGridLayout,
    QErrorMessage,
    QMessageBox,
)
from PyQt5.QtCore import Qt
import pandas as pd
import json
from progress_bar import ProgressBarWidget
from combobox import ConversionChoicesWidget
from writer import WriteJSONThread, WriteCSVThread, WriteExcelThread


VALIDATION_ERROR = 'Validation Error'
ALLOW_FILE_EXTENSION = ('.csv', '.xlsx', '.json')

class ConverterApp(QWidget):

    def __init__(self):
        super().__init__()
        self.title = '🇰🇭 CSV file utility'
        self.left = 0
        self.top = 210
        self.width = 520
        self.height = 120
        self.fileNameInput = QLineEdit(self)
        self.filePathInput = QLineEdit(self)
        self.errorDialog = QErrorMessage(self)
        self.popUpDialog = QMessageBox(self)
        self.conversionChoices = ConversionChoicesWidget()
        self.progressBar = ProgressBarWidget()
        self.btnBox = QDialogButtonBox()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

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
        gridLayout.addWidget(QLabel('Convert to:'), 2, 0)
        gridLayout.addWidget(self.conversionChoices, 2, 1)

        # Row: 5
        gridLayout.addWidget(QLabel("All right reserve Ⓒ Sagittech Inc."), 3,1)

        # Add a button box
        self.btnBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        # On OK clicked
        self.btnBox.accepted.connect(self.doConvertingFile)

        #On Cancel clicked
        self.btnBox.rejected.connect(self.closeApp)

        # Set the layout on the dialog
        dlgLayout.addWidget(self.progressBar)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addWidget(self.btnBox)

        #
        self.errorDialog.setWindowModality(Qt.WindowModal)

        self.setLayout(dlgLayout)
        self.set_widget_to_horizontal_center()
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

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"File explorer", "","All Files (*);;CSV Files (*.csv);;Excel Files (*.xlsx);;JSON Files (*.json)", options=options)
        if fileName:
            print(fileName)
            head, tail = os.path.split(fileName)
            self.fileNameInput.setText(tail)
            self.filePathInput.setText(head)

            file_extension = os.path.splitext(tail)[1]

            if file_extension == '.csv':
                self.conversionChoices.remove_item(0)
            if file_extension == '.xlsx':
                self.conversionChoices.remove_item(1)
            if file_extension == '.json':
                self.conversionChoices.remove_item(2)

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

    def other_to_json(self, input_file):
        file_extension = os.path.splitext(input_file)[1]

        if file_extension == '.csv':
            data = pd.read_csv(input_file)
        else:
            data = pd.read_excel(input_file, sheet_name='Sheet1')

        self.trim_all(data.copy())

        return json.loads(self.trim_all(data.copy()).to_json(orient='records'))

    def convert_to_json(self, input_file, output_file):
        with open(output_file, 'w') as f:
            f.write(json.dumps(self.other_to_json(input_file), indent=4))

    def trim_all(self, df: pd):
        # Select columns with string dtype (object)
        string_cols = df.select_dtypes(include=['object'])
        format_pattern = r"[0-9\.,]"  # Adjust the pattern as needed

        # Apply strip function to each string column
        return df.assign(**string_cols.apply(lambda x: x.str.strip().replace(format_pattern, "")))

    def convert_csv_to_other(self, input_file: str, output_file: str):
        to_date = {'cif': str, 'submit_date': str, 'repayment_date': str}
        data = pd.read_csv(input_file, converters=to_date)
        trim_data = self.trim_all(data.copy())

        output_file_extension = os.path.splitext(output_file)[1]

        if output_file_extension == '.xlsx':
            self.progressBar.start(trim_data, output_file, WriteExcelThread)
        else:
            self.progressBar.start(trim_data, output_file, WriteJSONThread)

    def convert_excel_to_other(self, input_file: str, output_file: str):
        # to_date = {'cif': str, 'submit_date': str, 'repayment_date': str}
        data = pd.read_excel(input_file)
        trim_data = self.trim_all(data.copy())

        output_file_extension = os.path.splitext(output_file)[1]

        if output_file_extension == '.csv':
            # Write the dataframe object into csv file
            self.progressBar.start(trim_data, output_file, WriteCSVThread)
        else:
            self.progressBar.start(trim_data, output_file, WriteJSONThread)

    def read_json(self, filename: str) -> dict:
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except:
            raise Exception(f"Reading {filename} file encountered an error")

        return data

    def convert_json_to_other(self, input_file: str, output_file: str):
        data = self.read_json(input_file)
        df = pd.json_normalize(data)
        output_file_extension = os.path.splitext(output_file)[1]

        print(output_file_extension)

        if output_file_extension == '.xlsx':
            self.progressBar.start(df, output_file, WriteExcelThread)
        else:
            self.progressBar.start(df, output_file, WriteCSVThread)

    def doConvertingFile(self):
        print('Starting ...')
        button = self.btnBox.button(QDialogButtonBox.Ok)
        button.setEnabled(False)

        if self.fileNameInput.text() == '':
            self.showPopUp(VALIDATION_ERROR, 'No file is inputted or chosen', QMessageBox.Warning)
            button.setEnabled(True)
            return

        if not self.fileNameInput.text().endswith(ALLOW_FILE_EXTENSION):
            self.showPopUp(VALIDATION_ERROR, f'Only {', '.join(ALLOW_FILE_EXTENSION)} file are allowed', QMessageBox.Warning)
            button.setEnabled(True)
            return

        try:
            input_file = os.path.join(self.filePathInput.text(), self.fileNameInput.text())
            new_directory = os.path.join(os.path.dirname(input_file), 'converted_csv')
            os.makedirs(new_directory, exist_ok=True)

            input_file_extension = os.path.splitext(input_file)[1]
            new_file_extension = f'.{self.conversionChoices.current_text().lower()}'
            new_file = os.path.join(new_directory, os.path.splitext(self.fileNameInput.text())[0] + new_file_extension)

            if input_file_extension == '.csv':
                self.convert_csv_to_other(input_file, new_file)
            elif input_file_extension == '.xlsx':
                self.convert_excel_to_other(input_file, new_file)
            else:
                self.convert_json_to_other(input_file, new_file)

        except Exception as err:
            self.showPopUp('Error', str(err), QMessageBox.Critical)

        button.setEnabled(True)

    def closeApp(self):
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterApp()
    sys.exit(app.exec_())
