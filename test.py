import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QLineEdit, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegularExpression
import sqlite3
import Show_data.goal_stats_for_teams


class DesignDetailWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Details !!!")
        self.setGeometry(100, 100, 800, 400)

        # Setup the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create a single filter widget
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Filter all columns")
        self.filter_edit.textChanged.connect(self.set_filter)
        main_layout.addWidget(self.filter_edit)

        # Create the QTreeView
        self.tree = QTreeView()
        main_layout.addWidget(self.tree)

        # Setup the model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "ID", "Game_ID", "League", "Time", "Home", "Goal_Home", "Goal_Away", "Away", "Corner", "Corner_half",
            "Dangerous_Attacks", "Shots"
        ])

        # Setup the proxy model for filtering
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(-1)  # Allow filtering on all columns
        self.tree.setModel(self.proxy_model)
        self.tree.setSortingEnabled(True)
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Populate the QTreeView
        self.populate_treeview()

        # Connect the double-click event
        self.tree.doubleClicked.connect(self.on_double_click)

    def populate_treeview(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM table_team_games')
        rows = c.fetchall()
        for row in rows:
            items = [QStandardItem(str(field)) for field in row]
            self.model.appendRow(items)
        conn.close()

    def on_double_click(self, index):
        index = self.proxy_model.mapToSource(index)
        item = self.model.itemFromIndex(index)
        my_game = [self.model.item(item.row(), col).text() for col in range(self.model.columnCount())]
        Show_data.goal_stats_for_teams.start(my_game[4], my_game[7])
        print(f"Selected ID: {my_game}")

    def set_filter(self):
        filter_text = self.filter_edit.text()
        regex = QRegularExpression(filter_text, QRegularExpression.CaseInsensitiveOption)
        self.proxy_model.setFilterRegularExpression(regex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesignDetailWindow()
    window.show()
    sys.exit(app.exec_())
