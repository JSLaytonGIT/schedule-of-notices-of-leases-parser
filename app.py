from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import logging
from schedule_of_notices_of_leases_parser import schedule_of_notices_of_leases_parser

app = Flask(__name__)
CORS(app) # I use cors to allow cross origin calls from the localhost port:3000

UPLOAD_FOLDER = 'user_pdfs' # sets the folder where users pdfs will be stored
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level=logging.INFO)

@app.route('/api/schedule_of_notices_of_leases_parser', methods=['POST']) # creates the endpoint in which my frontend can call  
def receive_user_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) # create the full filename string
        file.save(filename)
        
        logging.info(f"Received file: {filename}")
        
        schedule_of_notices_of_leases_parser(filename) # runs the parser
        return send_file('schedule_of_notices_of_leases.json', as_attachment=True) # send the file back to the frontend in the response

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) # creates the folder for the users pdfs
    app.run(debug=True)