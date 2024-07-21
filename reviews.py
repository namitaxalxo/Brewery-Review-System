from flask import request, redirect, url_for

# Temporary in-memory storage for reviews
reviews = {}

@app.route('/add_review/<int:id>', methods=['POST'])
def add_review(id):
    rating = request.form['rating']
    review = request.form['review']
    if id not in reviews:
        reviews[id] = []
    reviews[id].append({'rating': rating, 'review': review})
    return redirect(url_for('brewery', id=id))
