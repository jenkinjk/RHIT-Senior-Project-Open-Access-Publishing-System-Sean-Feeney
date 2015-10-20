from flask import Flask, request, redirect, render_template, url_for, send_file, send_from_directory, Response, make_response
import documentHandler
import s3DocumentHandler
import os
import pprint
#import cPickle
from RedisDatabaseImpl import RedisDatabase
import Paper
from datetime import datetime


ALLOWED_EXTENSIONS = set(['pdf', 'txt'])


app = Flask(__name__)
docStore = s3DocumentHandler.S3DocumentHandler() # our wrapper for whatever system stores the pdfs 

db = RedisDatabase("Anything besides the string 'Test', which wipes the database each time for testing purposes") # our wrapper for the database


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
        upload_file = request.files['file']
        if upload_file and allowed_file(upload_file.filename):
            # TODO: we might should check our database to see if the file already exists 
            
            # Parse out the entered information
            title = request.form['title']
            authorNames = request.form['authorName'].split(',')
            for authorName in authorNames:
                authorName.strip()
            tags = request.form['tags'].split(',')
            print 'tags:', tags
            for tag in tags:
                tag.strip()

            # putPaper(title, authors, tags, abstract, userID, datePublished, publisherID, citedBys, references)
            uniqueID = db.putPaper(title, authorNames, tags, None, None, datetime.now(), None, [], []) 

            docStore.storeDocument(upload_file, uniqueID)

        return redirect('/upload')
    # else it is a GET request
    else:
        results = []
        return render_template('upload.html', results=results)

@app.route('/uploads/<uniqueID>')
def uploaded_file(uniqueID):
    print 'viewing file', uniqueID 
    viewing_file = docStore.retrieveDocument(uniqueID)
    print 'content length:', viewing_file['Body']._content_length


    response = make_response(viewing_file['Body'].read())
    response.headers['Content-Type'] = 'application/pdf'
    # uncomment this line to download as attachment instead of view
    #response.headers['Content-Disposition'] = 'attachment; filename=' + uniqueID + '.pdf'
    return response


    # this part worked fine, but it is simpler to use the make_reponse function.  We may need to do things this way for streaming large files, however, so let's keep it around
    #def generate_file():
        #yield viewing_file['Body'].read()
        ######### TODO: this was experimental, more like actual streaming instead of giving it all in one glob, but had some issues with it.  should revisit at some point
        #amt_read = 0
        
        #while(amt_read < viewing_file['Body']._content_length):
        #    yield viewing_file['Body'].read(10)
        #    amt_read = amt_read + 10
        #########
    #return Response(generate_file(), mimetype='application/pdf')
    

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
        results = []
        print request.form
        # query DB for certain entries.  everything technically contains the empty string, and many things contain a space, so probably not good to return all those results if they ask
        if(request.form['search'] == '*'):
            results = db.getPapersMatchingTitle('')
        elif(request.form['search'] not in ['', ' ']):
            results = db.getPapersMatchingTitle(request.form['search'])
            print results
        

        return render_template('search.html', results=results)
    else:
        return render_template('search.html')
        
        
# Obviously, REMOVE FOR PRODUCTION        
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
        
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
	# REMOVE FOR PRODUCTION, and get a real WSGI server instead of the flask server (so turn threaded=True off):
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)
