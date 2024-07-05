import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg


class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My title")


        # set layout
        self.setLayout(qtw.QVBoxLayout())
        my_label = qtw.QLabel("aaaaaaaaaa")
        my_label.setFont(qtg.QFont('Arial', 25))

        self.layout().addWidget(my_label)

        my_entry = qtw.QLineEdit("ttttt")
        my_entry.setObjectName("name_field")
        self.layout().addWidget(my_entry)

        my_spin = qtw.QDoubleSpinBox(self,
                               value=10,
                               maximum=100,
                               minimum = 0,
                               singleStep =5.5,
                               prefix ='dd',
                               suffix='gg')

        self.layout().addWidget(my_spin)


        my_button = qtw.QPushButton("iiii",
            clicked = lambda: press_it())
        self.layout().addWidget(my_button)




        self.show()

        def press_it():

            my_label.setText(f'you picked: {my_spin.text()}')

app = qtw.QApplication([])
mw = MainWindow()

app.exec_()
