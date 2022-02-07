import hashlib
import sys

import requests
from secret import password_list

# Function to fetch the API
def get_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fetching: {res.status_code}, check url & try again!')
    return res


def get_leaks(hashes, check_hash):
    hashes = (x.split(':') for x in hashes.text.splitlines())
    for k, v in hashes:
        if k == check_hash:
            return v
    return 0


def check_password(password):
    encypted_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Get the first five chars of the hashed pass
    first_five = encypted_password[:5]
    tail = encypted_password[5:]
    response = get_api_data(first_five)
    return get_leaks(response, tail)


def main(args):
    for password in args:
        count = check_password(password)
        if count:
            print(f'{password} was found {count} times...😲🚨')
        else:
            print(f'{password} was not found you rock!🔥')
    return 'finished'


if __name__ == '__main__':
    main(password_list)
