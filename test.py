import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PyQt5.QtCore import QAbstractTableModel, Qt

class MyTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()
        data = [
            ['Row 0, Column 0', 'Row 0, Column 1'],
            ['Row 1, Column 0', 'Row 1, Column 1'],
            ['Row 1, Column 0', 'Row 1, Column 1'],['Row 1, Column 0', 'Row 1, Column 1'],
            ['Row 1, Column 0', 'Row 1, Column 1'],
            ['Row 1, Column 0', 'Row 1, Column 1']
        ]
        self.model = MyTableModel(data)
        self.table.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
