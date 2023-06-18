import os.path
import subprocess
import itertools as it
import threading

openstego = 'C:\\"Program Files (x86)"\\OpenStego\\openstego.bat'

THREADS_NUMBER = 3

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


def brute_force(thread):
    with open(LOG_FILE, 'w') as log_file, open(PASSWORD_FILE) as passwords_file:
        passwords = passwords_file.readlines()
        size = len(passwords)
        print(threading.get_ident())
        if thread == 0:
            start_idx = 0
            end_idx = size // THREADS_NUMBER
            print("t1")
        elif thread == 1:
            start_idx = (size // THREADS_NUMBER) + 1
            end_idx = 2*(size // THREADS_NUMBER)
            print("t2")
        elif thread == 2:
            start_idx = 2*(size // THREADS_NUMBER) + 1
            end_idx = size
            print("t3")

        for i in range(start_idx, end_idx):
            try:
                password = passwords[i].rstrip("\n")
                command = f'{openstego} extract -sf "{IMAGE}" -p "{password}" -xf "{LOG_FILE}"'
                subprocess.run(command, shell=True)
                print(password)
            except subprocess.CalledProcessError as e:
                print(e.stderr)


def start_threads():
    threads = []
    for i in range(THREADS_NUMBER):
        thread = threading.Thread(target=brute_force(i))
        threads.append(thread)
        print(f"thread number + {i} ")
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def main():
    create_log_file(LOG_FILE)

    if os.path.exists('output.txt'):
        pass
    else:
        create_password_file(LETTERS, output='output.txt')

    start_threads()


if __name__ == '__main__':
    main()
