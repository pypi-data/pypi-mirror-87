from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class DeleteUserWindow(QDialog):
    """Окно для удаления контакта"""
    def __init__(self, database, server):
        super().__init__()
        self.database = database
        self.server = server

        self.setFixedSize(350, 120)
        self.setWindowTitle('Удаление пользователя')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите пользователя:')
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_delete = QPushButton('Удалить', self)
        self.btn_delete.setFixedSize(100, 30)
        self.btn_delete.move(230, 20)
        self.btn_delete.clicked.connect(self.remove_user)

        self.btn_close = QPushButton('Отмена', self)
        self.btn_close.setFixedSize(100 ,30)
        self.btn_close.move(230, 60)
        self.btn_close.clicked.connect(self.close)

        self.fill_users()

    def fill_users(self):
        """Метод заполняющий список пользователей."""
        self.selector.addItems([user[0] for user in self.database.users_list()])

    def remove_user(self):
        """Метод - обработчик удаления пользователя."""
        self.database.remove_user(self.selector.currentText())
        if self.selector.currentText() in self.server.names:
            sock = self.server.names[self.selector.currentText()]
            del self.server.names[self.selector.currentText()]
            self.server.remove_client(sock)
        self.server.service_update_lists()
        self.close()
