from flask import Flask, request, redirect, render_template, url_for, send_from_directory
import documentHandler

import pprint


ALLOWED_EXTENSIONS = set(['pdf', 'txt'])


app = Flask(__name__)
docStore = documentHandler.SimpleDocHandler() # our wrapper for whatever system stores the pdfs 
db = []


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
            # TODO: we might should check our database to see if the file already exists somehow
            uniqueID = docStore.storeDocument(file)
            # TODO: now we record the uniqueID in the database along with metadata as a dictionary
            data = {'filename':file.filename, 'uniqueID':uniqueID}
            db.append(data)

            #return redirect(url_for('uploaded_file', filename=filename))
    # else it is a GET request
    results = db
    return render_template('upload.html', results=results)

@app.route('/uploads/<uniqueID>')
def uploaded_file(uniqueID):
    file = docStore.retrieveDocument(uniqueID)
    return send_file(file)

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
        # query DB for certain entries.  for now we return everything
        results = db

        return render_template('search.html', results=results)
    else:
        return render_template('search.html')

if __name__ == '__main__':
	# REMOVE FOR PRODUCTION:
    app.debug = True
    app.run(host='0.0.0.0')