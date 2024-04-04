import subprocess
import paramiko
from wakeonlan import send_magic_packet


def shutdown(ip, username, password):
    try:
        # Устанавливаем соединение SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        # Выполняем команду sudo shutdown now
        stdin, stdout, stderr = ssh.exec_command('sudo shutdown now', get_pty=True)
        # Передаем пароль на ввод
        stdin.write(password + '\n')
        stdin.flush()
        # Получаем результат выполнения команды
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        # Закрываем соединение
        ssh.close()
        # Печатаем результат
        # print(output)
        if error:
            return str(error)
    except paramiko.AuthenticationException as e:
        return 'неверный имя пользователя или пароль.'
    except Exception as e:
        return str(e)


def wake_on_lan(mac, ip='192.168.0.255', port=9):
    send_magic_packet(mac, ip_address=ip, port=port)


def connect_by_ssh(ip, username):
    ssh_command = f'ssh {username}@{ip}'
    subprocess.run(['start', 'cmd', '/c', ssh_command], shell=True)


if __name__ == '__main__':
    ip = '192.168.0.103'
    mac_address = '08:97:98:83:34:56'
    username = 'damir'
    password = '123'

    print('0 - выключить',
          '1 - включить',
          '2 - подключиться по ssh', sep='\n')
    user_input = input('Введите номер операции:')
    try:
        user_input = int(user_input)
    except ValueError:
        print('Неверный ввод: номер операции должен быть целым числом')
        exit(1)
    if user_input == 0:
        print(shutdown(ip, username, password))
    elif user_input == 1:
        print(wake_on_lan(mac_address))
    elif user_input == 2:
        print(connect_by_ssh(ip, username))
    else:
        print('Неверный ввод: нет такой операции')
        exit(1)
