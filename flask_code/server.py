from flask import Flask, request, redirect, render_template
app = Flask(__name__)



@app.route('/', methods=['GET'])
def welcome_page():
	# in the future, there may be info about the site here, or we may store cookies
	# and redirect to the login or account page automatically.  for now we redirect
	# to the login page
    return redirect('/login')
	
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if(request.method == 'POST'):
        #return render_template('uploadPdf.html')
        pass
    else:
        return render_template('uploadPdf.html')
	
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
    return render_template('search.html')

if __name__ == '__main__':
	# remove for production:
    app.debug = True
    app.run(host='0.0.0.0')