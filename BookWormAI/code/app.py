from flask import *
import chat
import csv

app = Flask(__name__)

DISPLAYLIMIT = 100 # post display limit 

@app.route('/')
@app.route('/index.html')
def main():
    return render_template("index.html")

@app.route('/')
@app.route('/history.html')
def history():
    temp = returnhistory()
    print(temp)
    # get data to send back to the server
    # get array full of submissions. Can be a 2D array of submissions, all submission turned into strings 
    #ctx2 = {submissions:temp, len : len(temp)}
    
    return render_template("history.html", submissions=temp)

# unused right now 
def returnhistory():
    # importing csv module 
    # csv file name
    filename = "./data/reviews.csv"
    # initializing the titles and rows list
    fields = []
    rows = []
 
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        fields = next(csvreader)
    
        # extracting each data row one by one
        i = 0
        for row in csvreader:
            rows.append(row)
            i += 1
            if i > DISPLAYLIMIT:
                break
    
        # get total number of rows
        #print("Total no. of rows: %d"%(csvreader.line_num))
    
        # printing the field names
        #print('Field names are:' + ', '.join(field for field in fields))
        
        # printing first 5 rows
        #print('\nFirst 5 rows are:\n')
        #for row in rows[:5]:
            # parsing each column of a row
        #    for col in row:
        #       print("%10s"%col,end=" "),
        #    print('\n')
    return rows


@app.route('/login.html')
def login():
    return render_template("login.html")

allowed_extensions = {'txt', 'pdf'}


def allowed_file(name):
    return '.' in name and \
        name.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/submission.html', methods = ['POST', 'GET'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        if allowed_file(f.filename):
            print(chat.get_review(f, True))
            return render_template("submission.html", review="Your code has been reviewed and uploaded to the history tab")
    return render_template("submission.html", review="")


if __name__ == '__main__':
    app.run(debug=True)
