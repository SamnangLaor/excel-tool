from PyQt5.QtCore import QThread, pyqtSignal
import json
import pandas as pd
import csv


class WriteJSONThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, df, file_path, orient='records', lines=True):
        super().__init__()
        self.df = df
        self.file_path = file_path
        self.orient = orient
        self.lines = lines

    def run(self):
        total_rows = len(self.df)
        written_rows = 0

        with open(self.file_path, 'w') as f:
            for index, chunk in self.df.iterrows():
                d = json.dumps(chunk.to_dict(), ensure_ascii=False, indent=4, default=str)

                if index == 0:
                    f.write('[' + d + ',\n')
                elif index == len(self.df) - 1:
                    f.write(d + ']\n')
                else:
                    f.write(d + ',\n')

                written_rows += 1
                progress = (written_rows / total_rows) * 100
                self.progress_signal.emit(int(progress))


class WriteCSVThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, df, file_path):
        super().__init__()
        self.df = df
        self.file_path = file_path

    def run(self):
        total_rows = len(self.df)
        written_rows = 0

        with open(self.file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.df.columns)

            for chunk in self.df.iterrows():
                writer.writerow(chunk[1])
                written_rows += 1
                progress = (written_rows / total_rows) * 100
                self.progress_signal.emit(int(progress))


class WriteExcelThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, df, file_path, sheet_name='Sheet1', rows_per_loop=100):
        super().__init__()
        self.df = df
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.rows_per_loop = rows_per_loop

    def run(self):
        total_rows = len(self.df)
        num_loops = (int(total_rows/self.rows_per_loop) + 1) #rows_per_loop + 1
        writer = pd.ExcelWriter(self.file_path, engine='xlsxwriter')
        progress = 0

        for i in range(num_loops):
            start_index = i * self.rows_per_loop
            end_index = min((i + 1) * self.rows_per_loop, total_rows)

            chunk = self.df.iloc[start_index:end_index, :]
            chunk.to_excel(writer, sheet_name='Sheet1', startrow=start_index, index=False)
            progress = end_index / total_rows * 100
            self.progress_signal.emit(int(progress))  # Signal completion

        writer._save()
        self.progress_signal.emit(100)  # Signal completion

