import sys
import requests
import argparse
import os.path

parser = argparse.ArgumentParser(description='pastebinCli tool')
parser.add_argument('operation', type=str, help='which handler to use get or paste')
parser.add_argument('file', type=str, help="file name to read/write")
parser.add_argument('--rawurl', type=str, help="full url from pastebin to grab data to file")
args = parser.parse_args()

if os.path.isfile(args.file) is False and args.operation.lower() == "paste":
    print("file: " + args.file + " not found")
    sys.exit(1)

login = {
    'api_dev_key': 'sNzySbu7EGd2st1LHTayZ--V-o0QAbp1',
    'api_user_name': 'raz-ohayon',
    'api_user_password': 'G3w#8udJnHMp9kc'
}


def get_token(login_data):
    pblogin = requests.post("https://pastebin.com/api/api_login.php", data=login_data)
    if pblogin.status_code != 200:
        return exit(1)
    else:
        return pblogin.text


def paste_text(token, text, api_dev_key, title):
    data = {
        'api_dev_key': api_dev_key,
        'api_option': "paste",
        'api_user_key': token,
        'api_paste_code': text,
        'api_paste_name': title
    }
    paste = requests.post("https://pastebin.com/api/api_post.php", data=data)
    print(paste.text)
    return paste.text


def get_text(filename, url):
    raw_text = requests.get(url)
    if raw_text.status_code != 200:
        print("failed to fetch data from url: " + url)
        sys.exit(3)


    file = open(filename, "w")
    file.write(raw_text.text)
    file.close()


if args.operation.lower() == "paste":
    token = get_token(login_data=login)
    file_content = open(args.file, "r").read()
    paste_text(token=token, text=file_content, api_dev_key=login['api_dev_key'], title=args.file)
elif args.operation.lower() == "get":
    if args.rawurl == "notset":
        print("rawurl is required with get operation")
        sys.exit(2)
    get_text(url=args.rawurl, filename=args.file)
else:
    print("operation not supported")

