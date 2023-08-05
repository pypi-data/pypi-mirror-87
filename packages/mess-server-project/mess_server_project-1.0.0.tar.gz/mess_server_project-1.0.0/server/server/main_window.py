from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QTimer
from server.statistic_window import StatisticWindow
from server.config_window import ConfigWindow
from server.registration import UserRegistration
from server.remove_user import DeleteUserWindow


class MainWindow(QMainWindow):
    """Основное окно сервера"""
    def __init__(self, database, server, config):
        super().__init__()
        self.database = database
        self.server_thread = server
        self.config = config

        self.exit_action = QAction('Выход', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(qApp.quit)

        self.refresh_button = QAction('Обновить список', self)
        self.config_button = QAction('Настройки сервера', self)
        self.register_btn = QAction('Регистрация пользователя', self)
        self.remove_btn = QAction('Удаление пользователя', self)
        self.show_history_button = QAction('История клиентов', self)

        self.statusBar()
        self.statusBar().showMessage('Сервер запущен')

        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_button)
        self.toolbar.addAction(self.register_btn)
        self.toolbar.addAction(self.remove_btn)
        self.toolbar.addAction(self.exit_action)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Мессенджер-сервер Alpha release')

        self.label = QLabel('Список подключенных клиентов:', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 25)

        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 45)
        self.active_clients_table.setFixedSize(780, 400)

        self.timer = QTimer()
        self.timer.timeout.connect(self.create_users_model)
        self.timer.start(1000)

        self.refresh_button.triggered.connect(self.create_users_model)
        self.show_history_button.triggered.connect(self.show_statistics)
        self.config_button.triggered.connect(self.server_config)
        self.register_btn.triggered.connect(self.reg_user)
        self.remove_btn.triggered.connect(self.remove_user)

        self.show()

    def create_users_model(self):
        """Метод заполняющий таблицу активных пользователей."""
        list_users = self.database.active_users_list()
        list_ = QStandardItemModel()
        list_.setHorizontalHeaderLabels(
            ['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
        for row in list_users:
            user, ip, port, time = row
            user = QStandardItem(user)
            user.setEditable(False)
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(str(port))
            port.setEditable(False)
            time = QStandardItem(str(time.replace(microsecond=0)))
            time.setEditable(False)
            list_.appendRow([user, ip, port, time])
        self.active_clients_table.setModel(list_)
        self.active_clients_table.resizeColumnsToContents()
        self.active_clients_table.resizeRowsToContents()

    def show_statistics(self):
        """Метод создающий окно со статистикой клиентов."""
        global stat_window
        stat_window = StatisticWindow(self.database)
        stat_window.show()

    def server_config(self):
        """Метод создающий окно с настройками сервера."""
        global config_window
        config_window = ConfigWindow(self.config)

    def reg_user(self):
        """Метод создающий окно регистрации пользователя."""
        global reg_window
        reg_window = UserRegistration(self.database, self.server_thread)
        reg_window.show()

    def remove_user(self):
        """Метод создающий окно удаления пользователя."""
        global rem_window
        rem_window = DeleteUserWindow(self.database, self.server_thread)
        rem_window.show()
