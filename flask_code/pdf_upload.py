import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['pdf', 'txt'])

app = Flask("PDF Upload")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# check if given file name is allowed as an upload
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# convert (if necessary) given filename into safe one
def get_secure_filename(filename):
	return secure_filename(filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = get_secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], "pdfs", filename))
			#return redirect(url_for('uploaded_file', filename=filename))
	# else it is a GET request
	return render_template('uploadPdf.html', pdfNames=os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], "pdfs")))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], "pdfs"), filename)
			
if __name__=="__main__":
	app.debug = True
	app.run(host='0.0.0.0')
