from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import random

app = Flask(__name__, template_folder='client')

app.config["MONGO_URI"] = "mongodb://localhost:27017/reviews"
mongo = PyMongo(app)

ANIMAL_NAMES = [
    "Clever Fox", "Brave Bear", "Wise Owl", "Happy Otter", "Swift Deer",
    "Gentle Dove", "Bold Lion", "Quiet Mouse", "Silly Goose", "Calm Turtle"
]

@app.route('/')
def index():
    reviews = mongo.db.reviews.find()
    return render_template('index.html', reviews=reviews)

@app.route('/review/<reviews_id>', methods=['GET', 'POST'])
def reviews(reviews_id):
    reviews = mongo.db.reviews.find_one({"_id": ObjectId(reviews_id)})

    if not reviews:
        return "Review not found", 404

    if request.method == 'POST':
        username = random.choice(ANIMAL_NAMES)
        new_comment = {
            "username": username,
            "comment": request.form.get("comment"),
            "timestamp": datetime.utcnow().isoformat()
        }
        mongo.db.reviews.update_one(
            {"_id": ObjectId(reviews_id)},
            {"$push": {"comments": new_comment}}
        )
        return redirect(url_for('reviews', reviews_id=reviews_id))

    return render_template('review.html', reviews=reviews)

if __name__ == "__main__":
    app.run(debug=True)
