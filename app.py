from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import logging
from schedule_of_notices_of_leases_parser import schedule_of_notices_of_leases_parser

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'user_pdfs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level=logging.INFO)

@app.route('/api/schedule_of_notices_of_leases_parser', methods=['POST'])
def receive_user_pdf():
    logging.info("Helloooo")
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        logging.info(f"Received file: {filename}")
        
        schedule_of_notices_of_leases_parser(filename)
        return send_file('schedule_of_notices_of_leases.json', as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)