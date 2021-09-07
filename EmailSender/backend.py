from flask import Flask
from flask import render_template , redirect
from flask import request
from flask import redirect 
import sys  
from emailSender import sendMail
from flask import send_file , url_for
sys.path.append('../')
sys.path.append('./')
from flask import Flask, redirect, url_for, request


app = Flask(__name__ ,static_url_path='/static')


from os import walk

f = []
for (dirpath, dirnames, filenames) in walk('\\Users\EBB\Desktop\EmailSender\Files'):
    f.extend(filenames)
    break


@app.route('/')
def index():
    return render_template("index.html")



@app.route("/sendMail",methods = ['POST', 'GET'])
def projects():
    if request.method =='POST':
        emailto = (request.form['email'])
        sendMail(emailto)
        return render_template("index.html")
    else:
        return render_template("sendMail.html")
    """
    if request.method == 'GET':
        return render_template("index.html")
    else:
        sendMail(emailto)
        return render_template("index.html")
    """



@app.route("/downloadList",methods = ['POST', 'GET'])
def downloadList():
    if request.method =='POST':
        return render_template("download.html" , fileNames = f)
    else:
        return render_template("download.html" , fileNames = f)
       
@app.route('/download/<variable>')
def download(variable):
    path = str(variable).split("\\")
    a = ".\Files\\"+ path[0]
    return send_file(a, as_attachment=True)
    

if __name__ == "__main__":
    app.run(debug=True)