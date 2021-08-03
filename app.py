from flask import Flask, render_template, url_for, request, send_file
import flask
from flask_bootstrap import Bootstrap 
import pandas as pd 
import numpy as np
from RF_forecast_azure import predictOnCSV, uploadFileToBlob
from flask_uploads import UploadSet, configure_uploads, ALL, DATA
import os
from werkzeug import secure_filename

app = flask.Flask(__name__)
Bootstrap(app)

#configuration
files = UploadSet('files', ALL)
app.config['UPLOADED_FILES_DEST']='static/uploadstorage'
configure_uploads(app, files)

class DataStore():
	predictFileName = None

data = DataStore()


@app.route('/')
def index():
	return flask.render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
	result = predictOnCSV(data.predictFileName)
	return flask.render_template('results.html', prediction = result)

@app.route('/datauploads', methods=['GET','POST'])
def datauploads():
	if request.method == 'POST' and 'csv_data' in request.files:
		file = request.files['csv_data']
		filename = secure_filename(file.filename)
		data.predictFileName = filename
		file.save(os.path.join('./static/upload', filename))
		# uploadFileToBlob(data.predictFileName)
		print("upload file :"+filename+" to blob")
	return render_template('details.html', filename=filename)

@app.route('/download')
def download_file():
	p = './static/output'+data.predictFileName+'_result.csv'
	return send_file(p, as_attachment=True)



if __name__ == '__main__':
	app.run(host="0.0.0.0", port= 5000, debug=True, use_reloader= True)