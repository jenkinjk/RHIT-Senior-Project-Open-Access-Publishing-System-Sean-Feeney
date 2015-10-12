from flask import Flask, request, redirect, render_template, url_for, send_file, send_from_directory
import documentHandler
import s3DocumentHandler
import os
import pprint
#import cPickle
import redisDatabaseImpl
import Paper


ALLOWED_EXTENSIONS = set(['pdf', 'txt'])


app = Flask(__name__)
docStore = s3DocumentHandler.S3DocumentHandler() # our wrapper for whatever system stores the pdfs 

db = redisDatabaseImpl()


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

            title = request.form['title']
            authorNames = request.form['authorName'].split(',')
            for authorName in authorNames:
                authorName.strip()
            tags = request.form['tags'].split(',')
            for tag in tags:
                tag.strip()

            print title, authorNames, tags

            uniqueID = db.putPaper(title, authorNames, tags) # (string title, list of strings authors, list of strings tags)

            docStore.storeDocument(file, uniqueID)

        return redirect('/upload')
    # else it is a GET request
    else:
        results = []
        return render_template('upload.html', results=results)

@app.route('/uploads/<uniqueID>')
def uploaded_file(uniqueID):
    file = docStore.retrieveDocument(uniqueID)
    tempfile = open('tempfile.pdf', 'wb')
    tempfile.write(file['Body'].read())
    return send_from_directory('.', 'tempFile')
    #return send_file(file, mimetype='application/pdf')
    

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
        results = db.search('')
        print results

        return render_template('search.html', results=results)
    else:
        return render_template('search.html')

if __name__ == '__main__':
	# REMOVE FOR PRODUCTION:
    app.debug = True
    app.run(host='0.0.0.0')