from flask import Flask, request, redirect, render_template, url_for, send_file, send_from_directory, Response, make_response, session
import documentHandler
import s3DocumentHandler
import os
import pprint
#from flask_oauth import OAuth
from RedisDatabase import RedisDatabase
import Paper
import User
from datetime import datetime, date
import base64
import json
import logging, logging.handlers

# to help with some weird encoding errors we were getting from python, related to copying and pasting
# abstracts with weird characters from pdf files.
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# png:
# import PDF_To_PNG_Converter

# if this is true, we use the testing S3 bucket, and the testing redis database, which is cleared out at the beginning of each run
# MODE = "Test" 
MODE = "Development" 
# MODE = "Production"


ALLOWED_EXTENSIONS = set(['pdf', 'txt'])
BIG_NUMBER = 99999

app = Flask(__name__)

# set printing to be to file
# SYSTEM_LOG_FILENAME = "server_log.txt"
# old_f = sys.stdout
# class F:
#     def write(self, x):
#         outfile = open(SYSTEM_LOG_FILENAME, "a")
#         # old_f.write("[" + str(datetime.now()) + "] " + x)
#         outfile.write(x)
#         outfile.close()
# sys.stdout = F()
# # sys.stdout = open("server_log.txt", "a")
# # set werkzeug logging to be to a file
# # sys.stdout = open(SYSTEM_LOG_FILENAME, "a")
# app.logger.setLevel(logging.INFO) # use native flask logger
# app.logger.disabled = False
# handler = logging.handlers.RotatingFileHandler(
#         SYSTEM_LOG_FILENAME,
#         "a",
#         maxBytes=1024 * 1024 * 100,
#         backupCount=0
#         )

# # formatter = logging.Formatter("%(message)s")
# # handler.setFormatter(formatter)

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.INFO)
# log.addHandler(handler)

# app.logger.addHandler(handler) # maybe not needed since we realy use werkzeug's logger

# png:
# png_converter = PDF_To_PNG_Converter.PDF_To_PNG()

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
    # import addDummyUsers
    db.putUser("Asher Morgan", "1162476383780112")
    db.putUser("Jonathan Jenkins", "986584014732857")
    db.putUser("Tyler Duffy", "10153554827465751")

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
    print('user ' + get_user_id() + ' requested the root page')
	# this is where we get to choose where to redirect people.  for now, 
    # redirect to the profile page.  later maybe the home page
    return redirect('/profile')

@app.route('/home', methods=['GET'])
def home_page():
    print('user ' + get_user_id() + ' is viewing the home page')
    return render_template('home.html')

def parse_paper_post_data():
    title = request.form.get('title', default="")
    # TODO: add author names as a field here that could be ignored on the outside, since sometimes 'authors' is used as names and sometimes as ids
    authorIDs = [] if request.form.get('authors', default="") == "" else request.form.get('authors', default="").split(',')
    authorIDs = [authorID.strip() for authorID in authorIDs]

    tags = [] if request.form.get('tags', default="") == "" else request.form.get('tags', default="").split(',')
    tags = [tag.strip() for tag in tags]

    abstract = request.form.get('abstract', default="")

    datePublished = request.form.get('date', default="")
    datePublished = parse_date(datePublished)

    references = [] if request.form.get('references', default="") == "" else request.form['references'].split(",")
    references = [reference.strip() for reference in references]
    # if an ID is already assigned to this paper somehow, such as when filling a stub or updating an existing paper
    paperID = request.form.get('paperID', default="")

    print "parsed incoming paper post data:"
    print "title:", title, "authorIDs", authorIDs, "tags:", tags, "abstract:", abstract, "datePublished:", datePublished, "references:", references, "paperID:", paperID
    return title, authorIDs, tags, abstract, datePublished, references, paperID

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    print 'user ' + get_user_id() + ' is uploading'
    if request.method == 'POST':
        title, authorIDs, tags, abstract, datePublished, references, paperID = parse_paper_post_data()
        print 'title:',title,'authorIDs:',authorIDs,'tags:',tags,'abstract:', abstract,'submittedBy:',get_user_id(),'datePublished:',datePublished,'references:',references
        if get_user_id() == "":
            return "Sorry, you must be logged in to upload a paper"
        upload_file = request.files.get('file', default=None)
        if upload_file and allowed_file(upload_file.filename):

            try:
                # We will be replacing some file in S3, so it is either uploading a new paper or updating a paper/stub and replacing the upload file
                if paperID == "":
                    # this is a new paper
                    print "Putting paper"
                    paperID = db.putPaper(title, authorIDs, tags, abstract, get_user_id(), datePublished, None, True)
                    db.setReferences(paperID, references)
                else:
                    # this paper already exists
                    posted_by = db.getPaper(paperID).postedByUserID
                    if posted_by != "" and posted_by != str(get_user_id()):
                        # they are not allowed to update/overwrite it
                        print "posted by:", posted_by, "user id:", str(get_user_id())
                        print "Permission denied, your user id did not upload this paper so you cannot modify it"
                        return "Permission denied, your user id did not upload this paper so you cannot modify it"
                    print "Updating paper and pdf with id:", paperID
                    db.updatePaper(paperID, title, authorIDs, tags, abstract, get_user_id(), datePublished, None, True)
                    db.setReferences(paperID, references)
                # in either case, store the document
                if docStore.documentExists(paperID):
                    docStore.removeDocument(paperID)
            except Exception as e:
                print "ERROR:",e
            docStore.storeDocument(upload_file, paperID)

        else:
            # We are not uploading a physical paper, so either we are updating a paper's metadata without changing the pdf, or it is an invalid request
            posted_by = db.getPaper(paperID).postedByUserID
            if posted_by != str(get_user_id()):
                # they are not allowed to update/overwrite it
                return "Permission denied, your used id did not upload this paper so you cannot modify it"
            print "Updating paper with id:", paperID
            db.updatePaper(paperID, title, authorIDs, tags, abstract, get_user_id(), datePublished, None, True)
            db.setReferences(paperID, references)
            # png:
            # thumbnail = png_converter.convert(upload_file)
            # print "uploading thumbnail: ", thumbnail.make_blob(format='png')

            # png:
            # docStore.storeThumbnail(thumbnail, uniqueID)

        return "Upload successful!"
        # return render_template('upload.html')
    # else it is a GET request
    else:
        # TODO: what about prepopulating the file input?
        # how about add the following text to file input in this case: "(optional) replace uploaded file with new one"
        stubID = "stubID" if request.args.get("editPaperID") is None else request.args.get("editPaperID")
        title = "" if request.args.get("title") is None else request.args.get("title")
        authorNames = "" if request.args.get("authorNames") is None else request.args.get("authorNames")
        authorIDs = "" if request.args.get("authorIDs") is None else request.args.get("authorIDs")
        datePublished = "" if request.args.get("datePublished") is None else request.args.get("datePublished").split(" ")[0]
        abstract = "" if request.args.get("abstract") is None else request.args.get("abstract")
        tags = "" if request.args.get("tags") is None else request.args.get("tags")
        referenceNames = "" if request.args.get("referenceNames") is None else request.args.get("referenceNames")
        referenceIDs = "" if request.args.get("referenceIDs") is None else request.args.get("referenceIDs")
        print "stubID:", stubID, "title:", title, "authorNames:", authorNames, "authorIDs:", authorIDs, "datePublished:", datePublished, "abstract:", abstract, "tags:", tags, "referenceNames:", referenceNames, "referenceIDs:", referenceIDs
        return render_template('upload.html', stubID=stubID, title=title, tags=tags, authorNames=authorNames, authorIDs=authorIDs, datePublished=datePublished, abstract=abstract, referenceNames=referenceNames, referenceIDs=referenceIDs)


@app.route('/uploadFakePaper', methods=['POST'])
def upload_fake_paper_endpoint():
    # title, authorIDs, tags, abstract, datePublished, references, paperID
    title, authorNames, _, _, datePublished, _, _ = parse_paper_post_data()
    # what is posted to the uploadFakePaper endpoint is currently author names, not ids, so let's naively resolve them
    authorIDs = [get_id_for_author_name(authorName) for authorName in authorNames]
    # we put the empty string in instead of get_user_id().  hopefully it doesn't break stuff
    uniqueID = db.putPaper(title, authorIDs, [], "", "", datePublished, None, False)
    return uniqueID

@app.route('/addNewAuthor', methods=['POST'])
def add_new_author_endpoint():
    
    authorName = request.form['authorName']
    uniqueID = db.putAuthor(authorName)

    return uniqueID


@app.route('/viewer/<uniqueID>')
def view_file(uniqueID):
    viewingPaper = db.getPaper(uniqueID)
    references = viewingPaper.references
    citedBys = viewingPaper.citedBys
    userID = get_user_id()
    favorited = db.hasFavoritePaper(userID, uniqueID)
    favoritedTags = []
    favoritedAuthors = []
    for authorID in viewingPaper.authorIDs:
        if db.hasFavoriteAuthor(userID, authorID):
            favoritedAuthors.append(True)
        else:
            favoritedAuthors.append(False)
    for tag in viewingPaper.tags:
        if db.hasFavoriteTag(userID, tag):
            favoritedTags.append(True)
        else:
            favoritedTags.append(False)
    references = [db.getPaper(reference) for reference in references]
    referenceTitles = [reference.title for reference in references]
    citedBys = [db.getPaper(citedBy) for citedBy in citedBys]
    return render_template('view_pdf.html', paper=viewingPaper, favorited=favorited, favoritedAuthors=favoritedAuthors, favoritedTags=favoritedTags, references=references, citedBys=citedBys, userID=userID, referenceTitles=referenceTitles)


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


@app.route('/thumbnails/<uniqueID>')
def get_thumbnail(uniqueID):
    print 'user ' + get_user_id() + ' is retrieving a thumbnail'
    print 'for file', uniqueID 
    return "no thumb"
    # png:
    # viewing_file = docStore.retrieveThumbnail(uniqueID)
    # print 'content length:', viewing_file['Body']._content_length

    # response = make_response(viewing_file['Body'].read())
    # response.headers['Content-Type'] = 'image/png'
    
    # uncomment this line to download as attachment instead of view
    #response.headers['Content-Disposition'] = 'attachment; filename=' + uniqueID + '.pdf'
    # return response
    

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
    if(user_id is ""):
        #   def __init__(id, username, followingIDs, followingNames, papers, authors, tags, followerCount, facebookID = None):
        user = User.User(0,"Anonymous User", [],[],[],[],[],0)
    else:
        user = db.getUserByID(user_id)
        # for favPaper in user.papers:
        #     attach_paper_thumbnail(favPaper)
        print user.username

    for paperGuy in user.papers:
        print paperGuy.title
    authorNames = []
    for authorObj in user.authors:
        authorNames.append(authorObj.name)
    return render_template('profile.html', user=user, authorGuys=authorNames, suggestions=db.getPaperRecsForUserID(user_id))

@app.route('/search', methods=['GET'])
def search_page():
    print 'user ' + get_user_id() + ' is searching'
    return render_template('advanced_search.html')


@app.route('/asyncPaperSearch', methods=['POST'])
def async_paper_search_endpoint():
    # an endpoint that performs searches.  returns results from start to end excluding end, 0 being the first result, 1 being the second, etc.
    title, authorNames, tags, _, datePublished, _, _ = parse_paper_post_data()
    start = int(request.form.get('start', default='0'))
    end = int(request.form.get('end', default='5'))

    results = db.getPapersAdvancedSearchRealOnly([title], tags, authorNames) # date)
    return render_template('paperSearch.html', results=results[start:end])


@app.route('/asyncReferenceSearch', methods=['POST'])
def async_reference_search_endpoint():
    # an endpoint that performs searches.  returns results from start to end excluding end, 0 being the first result, 1 being the second, etc.
    # title, authorIDs, tags, abstract, datePublished, references, paperID
    title, authorNames, tags, _, datePublished, _, _ = parse_paper_post_data()
    start = int(request.form.get('start', default='0'))
    end = int(request.form.get('end', default='5'))

    results = db.getPapersAdvancedSearch([title], tags, authorNames) # date)
    return render_template('referenceSearch.html', results=results[start:end])

@app.route('/asyncStubSearch', methods=['POST'])
def async_stub_search_endpoint():
    # an endpoint that performs searches.  returns results from start to end excluding end, 0 being the first result, 1 being the second, etc.
    # title, authorIDs, tags, abstract, datePublished, references, paperID
    title, authorNames, _, _, datePublished, _, _ = parse_paper_post_data()
    start = int(request.form.get('start', default='0'))
    end = int(request.form.get('end', default='5'))

    results = db.getPapersAdvancedSearchFakeOnly([title], [], authorNames) # date)
    return render_template('stubSearch.html', results=results[start:end])


@app.route('/asyncAuthorSearch', methods=['POST'])
def async_author_search_endpoint():
    # an endpoint that performs searches.  returns results from start to end excluding end, 0 being the first result, 1 being the second, etc.
    print 'user ' + get_user_id() + ' posted to asynchronous search'
    
    name = request.form.get('name', default="")

    start = int(request.form.get('start', default='0'))
    end = int(request.form.get('end', default='5'))

    results = db.getAuthorsMatchingAuthorNames([name])

    return render_template('authorSearch.html', results=results[start:end])


@app.route('/addFavorite', methods=['POST'])
def addFavorite():
    db.putFavoritePaper(get_user_id(), request.values['paperID'], 1)
    print(request.values['paperID'])
    return "Added! :)"

@app.route('/removeFavorite', methods=['POST'])
def rmFavorite():
    db.removeFavoritePaper(get_user_id(), request.values['paperID'])
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

@app.route('/removeFavoriteTag', methods=['POST'])
def rmFavoriteTag():
    db.removeFavoriteTag(get_user_id(), request.values['tag'])
    print(request.values['tag'])
    return "Added! :)"

@app.route('/removeFavoriteAuthor', methods=['POST'])
def rmFavoriteAuthor():
    db.removeFavoriteAuthor(get_user_id(), request.values['author'])
    print(request.values['author'])
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
    db.putUser("Asher Morgan", "1162476383780112")
    db.putUser("Jonathan Jenkins", "986584014732857")
    db.putUser("Tyler Duffy", "10153554827465751")
    return 'reinitilizing database'
        
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def get_id_for_author_name(author_name):
    # get a list of author objects similar to the given author name
    possibleAuthors = db.getAuthorsMatchingAuthorNames([author_name])

    print "matching author:", author_name
    for possibleAuthor in possibleAuthors:
        print "possible author match:", possibleAuthor.name
    # for each one (starting with the first which should be the closest match), see if it is an exact match
        if possibleAuthor.name == author_name:
            print "found author in database:", possibleAuthor.name
            # if so, return this ID 
            return possibleAuthor.id
    # if you get all the way through the possibles without getting a perfect match, this guy isn't in our database.  time to add him
    print "didn't find author in database, adding", author_name
    return db.putAuthor(author_name)

def attach_paper_thumbnail(paper):
    paper.thumbnail = docStore.retrieveThumbnail(paper.id)
    print "attaching thumbnail:", paper.thumbnail.make_blob(format='png')

def get_user_id():
    # In reality we should check the signature to make sure it is from who we think it is
    # currently we are not worried about security
    # we also should query facebook to make sure the person is legit
    if ('fbsr_' + FACEBOOK_APP_ID) in request.cookies:
        auth_cookie = request.cookies['fbsr_' + FACEBOOK_APP_ID].split('.')
        # print "cookie0:", auth_cookie[0]
        cookie_dict = json.loads(base64.urlsafe_b64decode(str(auth_cookie[1]) + ((4 - len(auth_cookie[1]) % 4) * '=')))
        # print "cookie dict:", str(cookie_dict)
        facebookID = str(cookie_dict['user_id'])
        regularID = db.facebookToRegularID(facebookID)
        return regularID
    else:
        return ""

def parse_date(datestring):
    # TODO: beef this up
    print "parsing datestring:", datestring
    if len(datestring) >= 10:
        return date(int(datestring[0:4]), int(datestring[5:7]), int(datestring[8:10]))
    else:
        return ""

if __name__ == '__main__':
	# REMOVE FOR PRODUCTION, and get a real WSGI server instead of the flask server (so turn threaded=True off):
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)
