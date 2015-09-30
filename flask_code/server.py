from flask import Flask, request, redirect, render_template, url_for, send_from_directory
import os
from werkzeug import secure_filename

UPLOAD_FOLDER = './pdfs'
ALLOWED_EXTENSIONS = set(['pdf', 'txt'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def welcome_page():
	# this is where we get to choose where to redirect people.  for now, 
    # redirect to the login page.  later maybe the home page
    return redirect('/login')

@app.route('/home', methods=['GET'])
def home_page():
    return render_template('home.html')
	



#########################################
# TODO: this version of upload is just for demo purposes.  for the real thing we wanna do javascript and ajax

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file', filename=filename))
    # else it is a GET request
    return render_template('upload.html', pdfNames=os.listdir(app.config['UPLOAD_FOLDER']))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	
########################################




@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if(request.method == 'POST'):
        # we are getting a request to login
        # verify credentials, etc. for now we let everything through
        return redirect('/profile')
    else:
        return render_template('login.html')
	
@app.route('/profile', methods=['GET'])
def profile_page():
    return render_template('profile.html')

@app.route('/search', methods=['GET', 'POST'])
def search_page():
    if(request.method == 'POST'):
        pass
    else:
        return render_template('search.html')

if __name__ == '__main__':
	# remove for production:
    app.debug = True
    app.run(host='0.0.0.0')