from flask import Flask, render_template, url_for, request, redirect
import datetime, csv 
import scrape

app = Flask(__name__)
# print(__name__)

@app.route("/")
def my_home():
    return render_template('index.html')

@app.route('/hackernews.html')
def test_page():   
    my_dict = scrape.page_from_scraped_data()
    my_dictJ = scrape.jobs_from_scraped_data()
    return render_template('hackernews.html',my_dict=my_dict,my_dictJ=my_dictJ)

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:    
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thank-you.html')  
        except:
            return 'Did not save to database'
    else:
        return 'something went wrong, try again!'   

# def write_to_file(data):
#     with open('./database.txt', mode='a') as db:
#         email = data['email'] # here I use the name added into html tag
#         subject = data['subject']
#         message = data['message']
#         file = db.write(f'\n {email}, {subject}, {message}, {datetime.datetime.now()} ')


def write_to_csv(data):
    with open('./database.csv', newline='', mode='a') as db2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(db2, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([datetime.datetime.now(),email,subject, message])