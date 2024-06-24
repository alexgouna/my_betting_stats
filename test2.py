import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


class LineDrawer(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(100, 200)  # Set a minimum size for the drawing widget

    def paintEvent(self, event):
        painter = QPainter(self)
        print(int(self.width()/100))
        for i in range(100):
            painter.setPen(QPen(Qt.black, int(self.width()/100), Qt.SolidLine))
            painter.drawLine(i*int(self.width()/100), 0, i*int(self.width()/100),20)
        # painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        # painter.drawLine(20, 0, 20, 20)

class TableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3x3 Table with Lines in the Middle Cell")
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget(3, 3)

        # Create a widget for the center cell
        self.line_drawer = LineDrawer()

        # Set the center cell to contain the line drawing widget
        self.table.setCellWidget(1, 1, self.line_drawer)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableWindow()
    window.show()
    sys.exit(app.exec_())
