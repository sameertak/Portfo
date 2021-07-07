from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_txt(data):
    email = data['email']
    subject = data['text']
    message = data['message']
    with open('database.txt', 'a') as mf:
        mf.write('\n---------------------------------------------------------------')
        mf.write(f'\nEmail ID:\t{email} \nSubject:\t{subject} \nMessage:\t{message}')
        mf.write('---------------------------------------------------------------')


def write_to_csv(data):
    email = data['email']
    subject = data['text']
    message = data['message']
    with open('database.csv',newline='', mode='a') as mf2:
        csv_writer = csv.writer(mf2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('./thank_you.html')
    else:
        return 'Something went wrong. Try again later'
