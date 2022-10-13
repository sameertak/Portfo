from flask import Flask, render_template, request, redirect
import csv
import hashlib
import requests

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as db2:
        email = data['email']
        subject = data['text']
        message = data['message']
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('./thank_you.html')
    else:
        return 'Something went wrong. Try again later'


@app.route('/password_checker', methods=['POST', 'GET'])
def password_checker():
    if request.method == "POST":
        password = request.form.to_dict()
        counted = main_pswd(password['password'])
        return render_template('/password_checker.html', counted=counted)
    else:
        return 'Something went wrong. Try again later'


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(f'Error while fetching the data. Error:{res.status_code}')
    return res


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return leak_counts(response, tail)


def leak_counts(hashes, check_hash):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == check_hash:
            return count
    return 0


def main_pswd(pswd):
    counted = pwned_api_check(pswd)
    return counted
