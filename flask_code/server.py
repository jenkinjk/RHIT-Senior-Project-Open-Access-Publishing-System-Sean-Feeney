from flask import Flask, request, redirect, render_template, url_for, send_file, send_from_directory, Response, make_response, session
import documentHandler
import s3DocumentHandler
import os
import pprint
#from flask_oauth import OAuth
from RedisDatabase import RedisDatabase
import Paper
import User
from datetime import datetime
import base64
import json

# if this is true, we use the testing S3 bucket, and the testing redis database, which is cleared out at the beginning of each run
# MODE = "Test" 
MODE = "Development" 
# MODE = "Production"


ALLOWED_EXTENSIONS = set(['pdf', 'txt'])
BIG_NUMBER = 99999

app = Flask(__name__)

# get the facebook credentials
credential_file = open('facebookCredentials.txt', 'r')
credential_file.readline()
credentials = credential_file.readline().split(',')
FACEBOOK_APP_ID = credentials[0]
FACEBOOK_API_VERSION = credentials[1]
FACEBOOK_APP_SECRET = credentials[2]

if MODE == "Test":
    print "Running in", MODE, "mode with self-clearing Test DB and test bucket of S3DocumentHandler"
    db = RedisDatabase(MODE)
    docStore = s3DocumentHandler.S3DocumentHandler(mode=MODE)
    # to save on S3 queries while testing, we could use this:
    # print "Running in", MODE, "mode with self-clearing Test DB and SimpleDocHandler.  Note: Must have local filesystem write permissions (sudo?)"
    # docStore = documentHandler.SimpleDocHandler()
    import addDummyUsers

elif MODE == "Development":
    print "Running in", MODE, "mode with regular DB and dev bucket of S3DocumentHandler"
    db = RedisDatabase(MODE)
    docStore = s3DocumentHandler.S3DocumentHandler(mode=MODE)

elif MODE == "Production":
    print "Running in", MODE, "mode with production DB and real bucket of S3DocumentHandler.  Realistic data only please."
    db = RedisDatabase(MODE)
    docStore = s3DocumentHandler.S3DocumentHandler(mode=MODE)


@app.route('/', methods=['GET'])
def welcome_page():
    print 'user ' + get_user_id() + ' requested the root page'
	# this is where we get to choose where to redirect people.  for now, 
    # redirect to the profile page.  later maybe the home page
    return redirect('/profile')

@app.route('/home', methods=['GET'])
def home_page():
    print 'user ' + get_user_id() + ' is viewing the home page'
    return render_template('home.html')
	



#########################################
# TODO: this version of upload is just for demo purposes.  for the real thing we wanna do javascript and ajax

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    print 'user ' + get_user_id() + ' is uploading'
    if request.method == 'POST':
        upload_file = request.files['file']
        if upload_file and allowed_file(upload_file.filename):
            # TODO: we might should check our database to see if the file already exists 
            
            # Parse out the entered information
            title = request.form['title']
            authorIDs = []
            authorNames = request.form['authorName'].split(',')
            for authorName in authorNames:
                authorName.strip()
                # TODO: Do this right, this is just a workaround.  we should be prompting users which author exactly they mean
                # to resolve same-name conflicts, then passing in the correct authorID
                authorIDs.append(db.putAuthor(authorName))
            tags = request.form['tags'].split(',')
            for tag in tags:
                tag.strip()


            # putPaper(title, authorIDs, tagNames, abstract, userID, datePublished, publisherID, citedBys, references)
            uniqueID = db.putPaper(title, authorIDs, tags, None, None, datetime(2015,10,21), None, [], []) 
            print 'title:',title
            print 'authornames:',authorNames
            print 'tags:',tags

            docStore.storeDocument(upload_file, uniqueID)

        results = []
        return render_template('upload.html', results=results)
    # else it is a GET request
    else:
        results = []
        return render_template('upload.html', results=results)



@app.route('/viewer/<uniqueID>')
def view_file(uniqueID):

    return render_template('view_pdf.html', uniqueID=uniqueID)


@app.route('/uploads/<uniqueID>')
def uploaded_file(uniqueID):
    print 'user ' + get_user_id() + ' is viewing a file'
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
    print 'user ' + get_user_id() + ' is logging in'
    if(request.method == 'POST'):
        # we are getting a request to login
        # verify credentials, etc. for now we let everything through
        return redirect('/profile')
    else:
        return render_template('login.html')
	
@app.route('/profile', methods=['GET'])
def profile_page():
    print 'user ' + get_user_id() + ' is on the profile page'
    # print 'request:', request
    # print 'cookies:', request.cookies
    # print 'session:', session
    # if ('fbsr_' + FACEBOOK_APP_ID) in request.cookies:
    #     # print request.cookies['fbsr_' + FACEBOOK_APP_ID]
    #     auth_cookie = request.cookies['fbsr_' + FACEBOOK_APP_ID].split('.')
    #     signature = base64.urlsafe_b64decode(str(auth_cookie[0]) + ((4 - len(auth_cookie[0]) % 4) * '='))
    #     payload = json.loads(base64.urlsafe_b64decode(str(auth_cookie[1]) + ((4 - len(auth_cookie[1]) % 4) * '=')))
    #     # print 'signature:', signature
    #     # print 'payload:', payload
    #     # # we should probably check with facebook to make sure this is legit, and check the signature and all that.  but really what we care about for now is the user_ID
    #     # print 'user_ID:', payload['user_id']
    # else:
    #     print 'user unknown (no facebook authentication cookie is set)'


    # User(username, followingIDs, followingNames, papers, authors, tags, followerCount):
    user_id = get_user_id()
    if(user_id is "Anonymous"):
        user = User.User("Anonymous User", [],[],[],[],[],0)
    else:
        user = db.getUser(user_id)
        print user.username

    return render_template('profile.html', user=user)

@app.route('/search', methods=['GET'])
def search_page():
    print 'user ' + get_user_id() + ' is searching'
    return render_template('search.html')

@app.route('/search-<byWhat>', methods=['GET', 'POST'])
def search_endpoint(byWhat):
    print 'user ' + get_user_id() + ' is searching'
    results = []
    
    print 'request form:', request.form

    if(byWhat == 'byTitle'):
        # TODO: remove this for production, or expand to allow regular expressions.  this is just for testing purposes
        if(request.form['title'] == '*'):
            results = db.getTopPapers(BIG_NUMBER)
        else:
            results = db.getPapersMatchingTitle(request.form['title'])
    elif(byWhat == 'byAuthors'):
        results = db.getPapersMatchingAuthorNames([request.form['authors']])
    elif(byWhat == 'byTags'):
        results = db.getPapersMatchingTags([request.form['tags']])



    return render_template('search.html', results=results)
        
# REMOVE FOR PRODUCTION
@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

# REMOVE FOR PRODUCTION
@app.route('/cleanoutS3', methods=['GET', 'POST'])
def cleanoutS3():
    docStore.removeAllNonMatching(db.getTopPapers(BIG_NUMBER))
    return 'deleting entries from S3 that are not reflected in database'

# REMOVE FOR PRODUCTION
@app.route('/cleanoutDB', methods=['GET', 'POST'])
def cleanoutDB():
    db.clearDatabase()
    return 'reinitilizing database'
        
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def get_user_id():
    # In reality we should check the signature to make sure it is from who we think it is
    # currently we are not worried about security
    # we also should query facebook to make sure the person is legit
    if ('fbsr_' + FACEBOOK_APP_ID) in request.cookies:
        auth_cookie = request.cookies['fbsr_' + FACEBOOK_APP_ID].split('.')
        return str(json.loads(base64.urlsafe_b64decode(str(auth_cookie[1]) + ((4 - len(auth_cookie[1]) % 4) * '=')))['user_id'])
    else:
        return "Anonymous"

if __name__ == '__main__':
	# REMOVE FOR PRODUCTION, and get a real WSGI server instead of the flask server (so turn threaded=True off):
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)
