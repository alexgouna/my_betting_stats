import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
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
        layout = QVBoxLayout(central_widget)

        # Create the QTreeView
        self.tree = QTreeView()
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.tree)

        # Setup the model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "ID", "Game_ID", "League", "Time", "Home", "Goal_Home", "Goal_Away", "Away", "Corner", "Corner_half",
            "Dangerous_Attacks", "Shots"
        ])
        self.tree.setModel(self.model)

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
        item = self.model.itemFromIndex(index)
        my_game = [self.model.item(item.row(), col).text() for col in range(self.model.columnCount())]
        Show_data.goal_stats_for_teams.start(my_game[4], my_game[7])
        print(f"Selected ID: {my_game}")


