import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import validation

UPLOAD_FOLDER = '/home/gosia/Downloads'
ALLOWED_EXTENSIONS = 'wav'

validator_app = Flask(__name__)
validator_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def is_file_allowed(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@validator_app.route('/', methods=['GET', 'POST'])
def upload_site():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)

		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and is_file_allowed(file.filename):
			sth = validation.valid_audio("%s/%s" % (UPLOAD_FOLDER, file.filename))
			print("sth: ", sth)
			print("type(sth): ", type(sth))
			filename = secure_filename(file.filename)
			file.save(os.path.join(validator_app.config['UPLOAD_FOLDER'], filename))
			sth_return = sth.split(" ")
			is_valid = sth_return[0]
			sample_number = " " if len(sth_return) == 1 else sth_return[1]
			print("sample_number: ", sample_number)

			return redirect(url_for('validation_site', filename=filename, is_valid=is_valid, sample_number=sample_number))
	return render_template('upload_site.html')


@validator_app.route('/validation/<filename>/<is_valid>/<sample_number>')
def validation_site(filename, is_valid, sample_number):
	return render_template('validation.html', filename=filename, is_valid=is_valid, sample_number=sample_number)


if __name__ == '__main__':
	validator_app.run(debug=True)
