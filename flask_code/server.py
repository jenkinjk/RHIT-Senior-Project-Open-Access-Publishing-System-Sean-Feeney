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
# png:
# import PDF_To_PNG_Converter

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

            authorNames = request.form['authorName'].split(',')
            authorNames = [authorName.strip() for authorName in authorNames]
            # TODO: Do this right, this is just a workaround.  we should be prompting users which author exactly they mean
            # to resolve same-name conflicts, then passing in the correct authorID
            authorIDs = [db.putAuthor(authorName) for authorName in authorNames]

            tags = request.form['tags'].split(',')
            tags = [tag.strip() for tag in tags]

            abstract = request.form['abstract']

            datePublished = request.form['datePublished']
            datePublished = datetime.strptime(datePublished, '%Y-%m-%d')

            references = request.form['references']

            print 'title:',title
            print 'authornames:',authorNames
            print 'authorIDs:',authorIDs
            print 'tags:',tags
            print 'abstract:',abstract
            print 'submittedBy:',get_user_id()
            print 'datePublished:',datePublished
            print 'references:',references

            # putPaper(title, authorIDs, tagNames, abstract, userID, datePublished, publisherID, citedBys, references)
            uniqueID = db.putPaper(title, authorIDs, tags, abstract, get_user_id(), datePublished, None, [], references) 
            # png:
            # thumbnail = PDF_To_PNG_Converter.convert(upload_file)

            docStore.storeDocument(upload_file, uniqueID)
            # png:
            # docStore.storeThumbnail(thumbnail, uniqueID)

        return render_template('upload.html')
    # else it is a GET request
    else:
        return render_template('upload.html')



@app.route('/viewer/<uniqueID>')
def view_file(uniqueID):
    return render_template('view_pdf.html', uniqueID=uniqueID, paper=db.getPaper(uniqueID))


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
        user = db.getUserByID(user_id)
        print user.username

    for paperGuy in user.papers:
        print paperGuy.title
    return render_template('profile.html', user=user, suggestions=db.getPaperRecsForUserID(user_id))

@app.route('/search', methods=['GET'])
def search_page():
    print 'user ' + get_user_id() + ' is searching'
    return render_template('search.html')

@app.route('/search-<byWhat>', methods=['GET', 'POST'])
def search_endpoint(byWhat):
    print 'user ' + get_user_id() + ' is searching'
    results = []
    
    # print 'request form:', request.form['tags']
    # print request.form['authors']
    # print request.form['tags']    

    if(byWhat == 'byTitle'):
        # TODO: remove this for production, or expand to allow regular expressions.  this is just for testing purposes
        if(request.form['title'] == '*'):
            print "hey"
            results = db.getTopPapers(BIG_NUMBER)
            print results
        else:
            results = db.getPapersMatchingTitle(request.form['title'])
    elif(byWhat == 'byAuthors'):
        authorNames = request.form['authors'].split(',')
        authorNames = [authorName.strip() for authorName in authorNames]
        results = db.getPapersMatchingAuthorNames(authorNames)
    elif(byWhat == 'byTags'):
        tags = request.form['tags'].split(',')
        tags = [tag.strip() for tag in tags]
        results = db.getPapersMatchingTags(tags)
    return render_template('search.html', results=results)


@app.route('/advancedSearch', methods=['GET', 'POST'])
def advanced_search_page():
    print 'user ' + get_user_id() + ' is searching'
    if(request.method == 'GET'):
        results = []
    else:
        results = []

        title = request.form['title']
        authorNames = request.form['authors'].split(',')
        authorNames = [authorName.strip() for authorName in authorNames]
        tags = request.form['tags'].split(',')
        tags = [tag.strip() for tag in tags]

        print "Title:", title
        print "AuthorNames:", authorNames
        print "Tags:", tags

        # TODO: grab the advanced search results from the back end


    return render_template('advanced_search.html', results=results)


@app.route('/addFavorite', methods=['POST'])
def addFavorite():
    # putFavoritePaper(self, userID, paperID, favoriteLevel)
    db.putFavoritePaper(get_user_id(), request.values['paperID'], 1)
    print(request.values['paperID'])
    return "Added! :)"

@app.route('/addFavoriteTag', methods=['POST'])
def addFavoriteTag():
    db.putFavoriteTag(get_user_id(), request.values['tag'], 1)
    print(request.values['tag'])
    return "Added! :)"

@app.route('/addFavoriteAuthor', methods=['POST'])
def addFavoriteAuthor():
    db.putFavoriteAuthor(get_user_id(), request.values['author'], 1)
    print(request.values['author'])
    return "Added! :)"

@app.route('/resolveAuthorName', methods=['POST'])
def resolveAuthorName():
    

    print(request.values['paperID'])
    return "Added! :)"
        
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
