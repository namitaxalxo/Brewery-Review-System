from flask import Flask, render_template, request, redirect, url_for, session
import requests
from uuid import UUID

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Hardcoded users
users = {
    'Namita': 'namita1'
}

# Temporary in-memory storage for reviews
reviews = {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('search'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
        session['username'] = username
        return redirect(url_for('search'))
    return 'Invalid credentials!'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('home'))

    search_results = []
    if request.method == 'POST':
        query = request.form['query']
        search_by = request.form['search_by']
        if search_by == 'city':
            search_results = requests.get(f'https://api.openbrewerydb.org/breweries?by_city={query}').json()
        elif search_by == 'name':
            search_results = requests.get(f'https://api.openbrewerydb.org/breweries?by_name={query}').json()
        elif search_by == 'type':
            search_results = requests.get(f'https://api.openbrewerydb.org/breweries?by_type={query}').json()
        
    return render_template('search.html', results=search_results)

@app.route('/brewery/<uuid:id>')
def brewery(id):
    if 'username' not in session:
        return redirect(url_for('home'))

    brewery_info = requests.get(f'https://api.openbrewerydb.org/breweries/{id}').json()
    return render_template('brewery.html', brewery=brewery_info)

@app.route('/add_review/<uuid:id>', methods=['POST'])
def add_review(id):
    rating = request.form['rating']
    review = request.form['review']
    if id not in reviews:
        reviews[id] = []
    reviews[id].append({'rating': rating, 'review': review})
    return redirect(url_for('brewery', id=id))

if __name__ == '__main__':
    app.run(debug=True)
 
