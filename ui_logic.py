from flask import Flask, render_template, request, redirect, url_for
import os
import requests
import json

app = Flask(__name__)

# Set the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

API_ENDPOINT='http://3.239.185.205:8000/image'


# Function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Route for the main upload form
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file is submitted
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']

        # If the user does not select a file
        if file.filename == '':
            return 'No selected file', 400

        # Check if the file has an allowed extension
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            api_response = ""
            with open(filepath, 'rb') as f:
                data = f.read()
                files = {'file': data}
                try:
                    api_response = requests.post(API_ENDPOINT, files=files, auth=(os.environ['IMAGE_API_USER'], os.environ['IMAGE_API_SECRET']))
                    data = json.loads(api_response.text)
                    rating = data.get('data').get('score')
                    rating_percentage = (rating) * 100
                    return render_template('rating_bar.html', rating=rating, rating_percentage=rating_percentage, image=f'uploads/{file.filename}')
                except Exception as e:
                    return {'Message': 'Error occurred processing Image. Try again', 'Exception': e.args, 'ApiRespStatus': api_response.status_code, 'ApiRespText': api_response.text}
        else:
            return 'Invalid file format. Only image files are allowed.', 400

    # Render the form to upload an image
    return render_template('upload.html')


if __name__ == '__main__':
    # Create the uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True, host='0.0.0.0', port=8001)
