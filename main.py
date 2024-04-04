import re
import json
import operations
from PyQt5 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление компьютером')
        self.setFixedSize(400, 230)
        self.setWindowIcon(QtGui.QIcon('icons/icon.ico'))
        self.ip = '192.168.0.106'
        self.mac_address = '00:30:67:25:79:43'
        self.use_ip = False
        self.username = 'damir'
        self.password = '123'
        self.profile_file = 'profiles.json'
        self.init_ui()
        self.show()

    def init_ui(self):
        self.main_vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.vbox1 = QtWidgets.QVBoxLayout()
        self.vbox2 = QtWidgets.QVBoxLayout()

        self.label_status = QtWidgets.QLabel('Статус: Неизвестно.', self)
        self.main_vbox.addWidget(self.label_status)

        self.label_ip = QtWidgets.QLabel(f'IP адрес компьютера: \n{self.ip}', self)
        self.vbox1.addWidget(self.label_ip)

        self.label_mac_address = QtWidgets.QLabel(f'MAC адрес компьютера: \n{self.mac_address}', self)
        self.vbox1.addWidget(self.label_mac_address)

        self.label_use_ip = QtWidgets.QLabel(f'Использовать IP адрес: \n{"Да" if self.use_ip else "Нет"}', self)
        self.vbox1.addWidget(self.label_use_ip)

        self.label_username = QtWidgets.QLabel(f'Имя пользователя: \n{self.username}', self)
        self.vbox1.addWidget(self.label_username)

        self.label_password = QtWidgets.QLabel(f'Пароль пользователя: \n{self.password}', self)
        self.vbox1.addWidget(self.label_password)

        self.label_select = QtWidgets.QLabel('Выберите действие:')
        self.vbox2.addWidget(self.label_select)

        self.button_wake = QtWidgets.QPushButton(QtGui.QIcon('icons/on.ico'), 'Включить компьютер', self)
        self.button_wake.clicked.connect(self.button_wake_clicked)
        self.vbox2.addWidget(self.button_wake)

        self.button_ssh = QtWidgets.QPushButton(QtGui.QIcon('icons/ssh.ico'), 'Подключиться по ssh', self)
        self.button_ssh.clicked.connect(self.button_ssh_clicked)
        self.vbox2.addWidget(self.button_ssh)

        self.button_shutdown = QtWidgets.QPushButton(QtGui.QIcon('icons/off.ico'), 'Выключить компьютер', self)
        self.button_shutdown.clicked.connect(self.button_shutdown_clicked)
        self.vbox2.addWidget(self.button_shutdown)

        self.button_settings = QtWidgets.QPushButton(QtGui.QIcon('icons/settings.ico'), 'Параметры', self)
        self.button_settings.clicked.connect(self.button_settings_clicked)
        self.vbox2.addWidget(self.button_settings)

        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.main_vbox.addLayout(self.hbox)
        self.setLayout(self.main_vbox)

    def button_wake_clicked(self):
        self.label_status.setText('Статус: Включение компьютера...')
        QtCore.QCoreApplication.processEvents()
        result = operations.wake_on_lan(self.mac_address, self.ip) if self.use_ip else operations.wake_on_lan(
            self.mac_address)
        if result:
            self.label_status.setText('Ошибка: ' + result)
        else:
            self.label_status.setText('Статус: Компьютер включен.')

    def button_ssh_clicked(self):
        result = operations.connect_by_ssh(self.ip, self.username)
        if result:
            self.label_status.setText('Ошибка: ' + result)
        else:
            self.label_status.setText('Статус: Подключение по ssh выполнено.')

    def button_shutdown_clicked(self):
        result = operations.shutdown(self.ip, self.username, self.password)
        if result:
            self.label_status.setText('Ошибка: ' + result)
        else:
            self.label_status.setText('Статус: Компьютер выключен.')

    def button_settings_clicked(self):
        self.settings = SettingsWindow(self.ip, self.mac_address, self.use_ip, self.username,
                                       self.password, self.settings_changed)

    def settings_changed(self, setting_name, new_value):
        if setting_name == 'ip':
            self.ip = new_value
            self.label_ip.setText(f'IP адрес компьютера: \n{self.ip}')
        elif setting_name =='mac_address':
            self.mac_address = new_value
            self.label_mac_address.setText(f'MAC адрес компьютера: \n{self.mac_address}')
        elif setting_name == 'use_ip':
            self.use_ip = new_value
            self.label_use_ip.setText(f'Использовать IP адрес: \n{"Да" if self.use_ip else "Нет"}')
        elif setting_name == 'username':
            self.username = new_value
            self.label_username.setText(f'Имя пользователя: \n{self.username}')
        elif setting_name == 'password':
            self.password = new_value
            self.label_password.setText(f'Пароль пользователя: \n{self.password}')


class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, ip, mac_address, use_ip, username, password, settings_changed):
        super().__init__()
        self.setWindowTitle('Настройки')
        self.setFixedSize(300, 300)
        self.setWindowIcon(QtGui.QIcon('icons/settings.ico'))
        self.ip = ip
        self.mac_address = mac_address
        self.use_ip = use_ip
        self.username = username
        self.password = password
        self.settings_changed = settings_changed
        self.init_ui()
        self.show()

    def init_ui(self):
        self.vbox = QtWidgets.QVBoxLayout()

        self.label_ip = QtWidgets.QLabel('IP-адрес компьютера:')
        self.vbox.addWidget(self.label_ip)

        self.lineEdit_ip = QtWidgets.QLineEdit()
        self.lineEdit_ip.setInputMask('000.000.000.000')
        self.lineEdit_ip.setText(self.ip)
        self.vbox.addWidget(self.lineEdit_ip)

        self.label_mac_address = QtWidgets.QLabel('MAC-адрес компьютера:')
        self.vbox.addWidget(self.label_mac_address)

        self.lineEdit_mac_address = QtWidgets.QLineEdit()
        self.lineEdit_mac_address.setText(self.mac_address)
        self.lineEdit_mac_address.setInputMask('HH:HH:HH:HH:HH:HH')
        self.vbox.addWidget(self.lineEdit_mac_address)

        self.label_username = QtWidgets.QLabel('Имя пользователя:')
        self.vbox.addWidget(self.label_username)

        self.lineEdit_username = QtWidgets.QLineEdit()
        self.lineEdit_username.setText(self.username)
        self.vbox.addWidget(self.lineEdit_username)

        self.label_password = QtWidgets.QLabel('Пароль пользователя:')
        self.vbox.addWidget(self.label_password)

        self.lineEdit_password = QtWidgets.QLineEdit()
        self.lineEdit_password.setText(self.password)
        self.vbox.addWidget(self.lineEdit_password)

        self.checkBox_use_ip = QtWidgets.QCheckBox('[Wake-on-LAN] Использовать IP-адрес')
        self.checkBox_use_ip.setChecked(self.use_ip)
        self.vbox.addWidget(self.checkBox_use_ip)

        self.button_save = QtWidgets.QPushButton(QtGui.QIcon('icons/save.ico'), 'Сохранить и закрыть', self)
        self.button_save.clicked.connect(self.button_save_clicked)
        self.vbox.addWidget(self.button_save)

        self.setLayout(self.vbox)

    def button_save_clicked(self):
        new_ip = self.lineEdit_ip.text().strip()  # Удаляем лишние пробелы
        new_mac_address = self.lineEdit_mac_address.text().strip()
        new_use_ip = self.checkBox_use_ip.isChecked()
        new_username = self.lineEdit_username.text().strip()
        new_password = self.lineEdit_password.text().strip()

        # Проверяем корректность IP-адреса
        if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', new_ip):
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, введите корректный IP-адрес.')
            return

        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', new_mac_address):
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, введите корректный MAC-адрес.')
            return

        if not new_username or not new_password:  # Проверяем, что имя пользователя и пароль не пустые
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, заполните все поля.')
            return

        self.settings_changed('ip', new_ip)
        self.settings_changed('mac_address', new_mac_address)
        self.settings_changed('use_ip', new_use_ip)
        self.settings_changed('username', new_username)
        self.settings_changed('password', new_password)
        self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
