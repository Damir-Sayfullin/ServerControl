import re
import json
import operations
from PyQt5 import QtWidgets, QtCore, QtGui


class Profile:
    def __init__(self, name, ip, mac_address, use_ip, username, password):
        self.name = name
        self.ip = ip
        self.mac_address = mac_address
        self.use_ip = use_ip
        self.username = username
        self.password = password

    def __str__(self):
        return self.name


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ServerControl')
        self.setFixedSize(420, 320)
        self.setWindowIcon(QtGui.QIcon('icons/icon.ico'))
        self.selected_profile = Profile('Default', '0.0.0.0', '00:00:00:00:00:00',
                                        True, 'admin', 'admin')
        self.profile_file = 'profiles.json'
        self.profiles = self.load_profiles()
        self.init_ui()
        self.check_profiles()
        self.show()

    def load_profiles(self):
        try:
            with open(self.profile_file, 'r') as f:
                data = f.read()
                if data.strip():
                    f.seek(0)
                    json_data = json.load(f)
                    validated_profiles = []
                    for profile_name, profile_data in json_data.items():
                        if self.validate_profile(profile_data) and profile_name.strip():
                            validated_profiles.append(Profile(profile_name, profile_data['ip'].strip(),
                                                              profile_data['mac_address'].strip(),
                                                              profile_data['use_ip'],
                                                              profile_data['username'].strip(),
                                                              profile_data['password'].strip()))
                        else:
                            return -1
                    return validated_profiles
                else:
                    return [self.selected_profile]
        except FileNotFoundError:
            return [self.selected_profile]
        except json.JSONDecodeError:
            return -1

    def validate_profile(self, profile_data):
        if (isinstance(profile_data, dict) and
                all(key in profile_data for key in ['ip', 'mac_address', 'use_ip', 'username', 'password'])):
            # Проверка на пустоту значений
            if (all(profile_data[key].strip() for key in ['ip', 'mac_address', 'username', 'password']) and
                    isinstance(profile_data['use_ip'], bool)):
                ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
                mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
                if re.match(ip_pattern, profile_data['ip']) and re.match(mac_pattern, profile_data['mac_address']):
                    return True
        else:
            return False

    def check_profiles(self):
        if self.profiles != -1:
            self.update_profiles()
        else:
            self.label_profile.setText('Профили недоступны:\n'
                                       'Укажите другой файл в настройках.')
            self.label_profile.setEnabled(False)
            self.list_profiles.setEnabled(False)
            self.button_save_profiles.setEnabled(False)

    def update_profiles(self):
        for profile in self.profiles:
            self.list_profiles.addItem(profile.name)

    def init_ui(self):
        self.main_vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.vbox1 = QtWidgets.QVBoxLayout()
        self.vbox2 = QtWidgets.QVBoxLayout()

        self.label_status = QtWidgets.QLabel('Статус: Неизвестно.', self)
        self.main_vbox.addWidget(self.label_status)

        self.label_ip = QtWidgets.QLabel(f'IP адрес компьютера: \n{self.selected_profile.ip}', self)
        self.vbox1.addWidget(self.label_ip)

        self.label_mac_address = QtWidgets.QLabel(f'MAC адрес компьютера: \n{self.selected_profile.mac_address}', self)
        self.vbox1.addWidget(self.label_mac_address)

        self.label_use_ip = QtWidgets.QLabel(
            f'Использовать IP адрес: \n{"Да" if self.selected_profile.use_ip else "Нет"}', self)
        self.vbox1.addWidget(self.label_use_ip)

        self.label_username = QtWidgets.QLabel(f'Имя пользователя: \n{self.selected_profile.username}', self)
        self.vbox1.addWidget(self.label_username)

        self.label_password = QtWidgets.QLabel(f'Пароль пользователя: \n{self.selected_profile.password}', self)
        self.vbox1.addWidget(self.label_password)

        self.label_profile = QtWidgets.QLabel(f'Профиль:', self)
        self.label_profile.setFixedSize(350, 35)
        self.vbox2.addWidget(self.label_profile)

        self.vbox2.addSpacing(10)

        self.list_profiles = QtWidgets.QComboBox(self)
        self.list_profiles.currentTextChanged.connect(self.list_profiles_changed)
        self.vbox2.addWidget(self.list_profiles)

        self.button_save_profiles = QtWidgets.QPushButton(QtGui.QIcon('icons/save.ico'), 'Сохранить профили', self)
        self.button_save_profiles.clicked.connect(self.button_save_profiles_clicked)
        self.vbox2.addWidget(self.button_save_profiles)

        self.vbox2.addSpacing(self.height())

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
        self.hbox.addSpacing(20)
        self.hbox.addLayout(self.vbox2)
        self.main_vbox.addLayout(self.hbox)
        self.setLayout(self.main_vbox)

    def button_wake_clicked(self):
        self.label_status.setText('Статус: Включение компьютера...')
        QtCore.QCoreApplication.processEvents()
        result = operations.wake_on_lan(self.selected_profile.mac_address, self.selected_profile.ip) \
            if self.selected_profile.use_ip else operations.wake_on_lan(self.selected_profile.mac_address)
        if result:
            self.label_status.setText('Ошибка: ' + result)
        else:
            self.label_status.setText('Статус: Компьютер включен.')

    def button_ssh_clicked(self):
        result = operations.connect_by_ssh(self.selected_profile.ip, self.selected_profile.username)
        if result:
            self.label_status.setText('Ошибка: ' + result)
        else:
            self.label_status.setText('Статус: Подключение по ssh выполнено.')

    def button_shutdown_clicked(self):
        result = operations.shutdown(self.selected_profile.ip, self.selected_profile.username,
                                     self.selected_profile.password)
        if result:
            self.label_status.setText('Ошибка: ' + result)
        else:
            self.label_status.setText('Статус: Компьютер выключен.')

    def button_save_profiles_clicked(self):
        with open('profiles.json', 'w') as f:
            data = {}
            for profile in self.profiles:
                data[profile.name] = {
                    'ip': profile.ip,
                    'mac_address': profile.mac_address,
                    'use_ip': profile.use_ip,
                    'username': profile.username,
                    'password': profile.password
                }
            json.dump(data, f, indent=4)

    def settings_changed(self):
        self.label_ip.setText(f'IP адрес компьютера: \n{self.selected_profile.ip}')
        self.label_mac_address.setText(f'MAC адрес компьютера: \n{self.selected_profile.mac_address}')
        self.label_use_ip.setText(f'Использовать IP адрес: \n{"Да" if self.selected_profile.use_ip else "Нет"}')
        self.label_username.setText(f'Имя пользователя: \n{self.selected_profile.username}')
        self.label_password.setText(f'Пароль пользователя: \n{self.selected_profile.password}')

    def list_profiles_changed(self):
        self.selected_profile = self.profiles[self.list_profiles.currentIndex()]
        self.settings_changed()

    def button_settings_clicked(self):
        self.settings = SettingsWindow(self.selected_profile, self.settings_changed)


class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, selected_profile, settings_changed):
        super().__init__()
        self.setWindowTitle('Настройки')
        self.setFixedSize(300, 300)
        self.setWindowIcon(QtGui.QIcon('icons/settings.ico'))
        self.selected_profile = selected_profile
        self.settings_changed = settings_changed
        self.init_ui()
        self.show()

    def init_ui(self):
        self.vbox = QtWidgets.QVBoxLayout()

        self.label_ip = QtWidgets.QLabel('IP-адрес компьютера:')
        self.vbox.addWidget(self.label_ip)

        self.lineEdit_ip = QtWidgets.QLineEdit()
        self.lineEdit_ip.setInputMask('000.000.000.000')
        self.lineEdit_ip.setText(self.selected_profile.ip)
        self.vbox.addWidget(self.lineEdit_ip)

        self.label_mac_address = QtWidgets.QLabel('MAC-адрес компьютера:')
        self.vbox.addWidget(self.label_mac_address)

        self.lineEdit_mac_address = QtWidgets.QLineEdit()
        self.lineEdit_mac_address.setText(self.selected_profile.mac_address)
        self.lineEdit_mac_address.setInputMask('HH:HH:HH:HH:HH:HH')
        self.vbox.addWidget(self.lineEdit_mac_address)

        self.label_username = QtWidgets.QLabel('Имя пользователя:')
        self.vbox.addWidget(self.label_username)

        self.lineEdit_username = QtWidgets.QLineEdit()
        self.lineEdit_username.setText(self.selected_profile.username)
        self.vbox.addWidget(self.lineEdit_username)

        self.label_password = QtWidgets.QLabel('Пароль пользователя:')
        self.vbox.addWidget(self.label_password)

        self.lineEdit_password = QtWidgets.QLineEdit()
        self.lineEdit_password.setText(self.selected_profile.password)
        self.vbox.addWidget(self.lineEdit_password)

        self.checkBox_use_ip = QtWidgets.QCheckBox('[Wake-on-LAN] Использовать IP-адрес')
        self.checkBox_use_ip.setChecked(self.selected_profile.use_ip)
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

        self.selected_profile.ip = new_ip
        self.selected_profile.mac_address = new_mac_address
        self.selected_profile.use_ip = new_use_ip
        self.selected_profile.username = new_username
        self.selected_profile.password = new_password
        self.settings_changed()
        self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
