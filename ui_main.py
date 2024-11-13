from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    rating = .5 # Example rating value
    rating_percentage = (rating) * 100
    return render_template('rating_bar.html', rating=rating, rating_percentage=rating_percentage)

if __name__ == '__main__':
    app.run(debug=True)