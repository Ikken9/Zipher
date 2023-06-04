import os.path
import subprocess
import itertools as it

openstego = 'C:\\"Program Files (x86)"\\OpenStego\\openstego.bat'


PASSWORD_FILE = 'output.txt'
LOG_FILE = 'log.txt'

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
IMAGE = 'image.png'


def create_password_file(letters, output):
    combinations = list(it.product(letters, repeat=5))
    with open(output, 'w') as file:
        for combination in combinations:
            file.write(''.join(combination) + '2019' + '\n')

    print(f"File '{output}' created with combinations.")


def create_log_file(output):
    with open(output, 'w') as log_file:
        pass


def brute_force():
    with open(LOG_FILE, 'w') as log, open(PASSWORD_FILE) as passwords_file:
        for password in passwords_file:
            try:
                print(password)
                command = f'{openstego} extract -sf "{IMAGE}" -p {password} -xf "{LOG_FILE}"'
                # command = f'{openpuff} -extract -stegano "{IMAGE}" -p "{password}"'
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                log.write(output.decode('utf-8'))
            except subprocess.CalledProcessError as e:
                log.write(e.output.decode('utf-8'))


def main():
    create_log_file(LOG_FILE)

    if os.path.exists('output.txt'):
        pass
    else:
        create_password_file(LETTERS, output='output.txt')

    brute_force()


if __name__ == '__main__':
    main()
