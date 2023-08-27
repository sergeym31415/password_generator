from random import choice
from string import ascii_letters, digits
from datetime import datetime
import argparse
from pathlib import Path


class SmallLengthException(Exception):
    pass


class TooManySpecialSymbols(Exception):
    pass


class TooLittleNumPasswords(Exception):
    pass


def save_to_file(obj):
    """
    :param obj: str or list
    :return: None
    """
    Path('passwords').mkdir(parents=True, exist_ok=True)
    now_time = datetime.now()
    ending = now_time.strftime('%H-%M-%S')
    filename = f'passwords/passwords_{ending}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        if type(obj) == str:
            f.write(obj)
        elif type(obj) == tuple:
            f.writelines('\n'.join(obj))
    print(f'Passwords saved to /passwords/{filename}')


def generate_password(num_passwords: int = 1, length_password: int = 12, num_special_symbols=1) -> (str, tuple[str]):
    if num_passwords < 1:
        raise TooLittleNumPasswords('Number of passwords is less than 1')
    if length_password < 5:
        raise SmallLengthException('Too small (less 5) length of password')
    if num_special_symbols + 3 > length_password:
        raise TooManySpecialSymbols('Too many special symbols for this length of password')
    special_symbols = '!@#$%^&*-_=+;:"<>/?'

    def generate_one_password(length):
        while True:
            password = ''
            flag_upper = flag_lower = flag_digit = flag_special = False
            for _ in range(length):
                if flag_special or num_special_symbols <= 0:
                    new_symbol = choice(ascii_letters + digits)
                else:
                    new_symbol = choice(ascii_letters + digits + special_symbols)
                password += new_symbol
                if new_symbol.isdigit():
                    flag_digit = True
                elif new_symbol.isupper():
                    flag_upper = True
                elif new_symbol.islower():
                    flag_lower = True
                if sum([symbol in special_symbols for symbol in password]) >= num_special_symbols:
                    flag_special = True
            if all([flag_lower, flag_upper, flag_digit, flag_special]):
                break
        return password

    if num_passwords == 1:
        return generate_one_password(length_password)
    else:
        passwords = tuple(generate_one_password(length_password) for _ in range(num_passwords))
        return passwords


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Password Generator', description='This program generate passwords',
                                     epilog='(c) Meshkov Sergey')
    parser.add_argument('--number', default=1, help='set the number of passwords you need')
    parser.add_argument('--length', default=12, help='set the length of password')
    parser.add_argument('--spec', default=1, help='set the number of special symbols in password')
    parser.add_argument('-file', action='store_const', const=True, help='set, if you need to save password to file')
    args = parser.parse_args()
    try:
        number = int(args.number)
        length = int(args.length)
        spec = int(args.spec)
    except ValueError as e:
        raise ValueError('Type of argument is not int')
    if args.file:
        save_to_file(generate_password(num_passwords=number, length_password=length, num_special_symbols=spec))
    else:
        print(generate_password(num_passwords=number, length_password=length, num_special_symbols=spec))
