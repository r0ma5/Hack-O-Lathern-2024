from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Set the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


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
            rating = .5 # Example rating value
            rating_percentage = (rating) * 100
            return render_template('rating_bar.html', rating=rating, rating_percentage=rating_percentage)
        else:
            return 'Invalid file format. Only image files are allowed.', 400

    # Render the form to upload an image
    return render_template('upload.html')


if __name__ == '__main__':
    # Create the uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
