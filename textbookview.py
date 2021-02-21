"""
sproul.club Backend Assignment
Textbook View API Views

Author: Nicholas Cho
"""
# Imports
import json
from flask import Flask, request, jsonify, url_for
from flask_mongoengine import MongoEngine, Document

# Initializing app and database connection
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db' : 'sproulclub-backend-takehome',
    'host' : 'localhost',
    'port' : 27017
}

db = MongoEngine()
db.init_app(app)

# Model classes (meta fields route to corresponding collections in database)
class User(db.Document):
    meta = {
        'collection': 'User'
    }
    full_name = db.StringField()
    email = db.StringField()
    password = db.StringField()
    textbooks = db.ListField()

# I changed the textbook id field to "bid" as to avoid conflict with the object id
class Textbook(db.Document):
    meta = {
        'collection': 'Textbook'
    }
    bid = db.StringField()
    name = db.StringField()
    author = db.StringField()

class QRCode(db.Document):
    meta = {
        'collection': 'QRCode'
    }
    image_path = db.StringField()
    link = db.StringField()

"""
I did not include any redirects. All responses instead return JSON. In place of user authentication, I am using the full 
name of the user as a URL variable to validate any queries that I make. For removing/adding textbooks I am assuming that the entry 
that is selected by the user for removal is being passed in as the request data.
"""

# Views

# List all textbooks
@app.route('/', methods=['GET'])
def list_all_books():
    all_textbooks = Textbook.objects().all()
    return jsonify(all_textbooks)

# Lists user's textbooks
@app.route('/<fullname>/mybooks/', methods=['GET'])
def list_textbooks(fullname):
    # Check that user exists, error otherwise 
    user = User.objects(full_name=fullname).first()
    if user:
        # Retrieve textbook documents based on user textbook list
        textbook_ids = user.textbooks
        textbook_objs = [Textbook.objects(bid=int(bid)).first() for bid in textbook_ids]
        return jsonify(textbook_objs)
    else:
        return jsonify('Not a valid user!')

# Adds textbook that is clicked by user textbook list 
@app.route('/<fullname>/add/', methods=['POST'])
def add_textbook(fullname):
    # Check that user exists, error otherwise
    user = User.objects(full_name=fullname).first()
    if user:
        data = json.loads(request.data)
        # Update textbook list with new textbook
        new_list = user.textbooks + [data['bid']]
        user.update(textbooks=new_list)
        return jsonify('Successfully added!')
    
    return jsonify('Not a valid user!')

# Deletes textbook that is clicked by user from textbook list
@app.route('/<fullname>/remove/', methods=['DELETE'])
def delete_textbook(fullname):
    # Check that user exists, error otherwise
    user = User.objects(full_name=fullname).first()
    if user:
        data = json.loads(request.data)
        textbook = Textbook.objects(bid=data['bid'],
                                    name=data['name'],
                                    author=data['author']).first()
        textbook.delete()
        return jsonify('Successfully deleted!')
    
    return jsonify('Not a valid user!')

# Page with user's textbook titles (to be shared through the QR code)
@app.route('/<fullname>/booktitles/', methods=['GET'])
def list_titles(fullname):
    # Check that user exists, error otherwise 
    user = User.objects(full_name=fullname).first()
    if user:
        # Retrieve textbook names based on user textbook list
        textbook_ids = user.textbooks
        textbook_objs = [Textbook.objects(bid=int(bid)).first().name for bid in textbook_ids]
        return jsonify(textbook_objs)
    else:
        return jsonify('Not a valid user!')

"""
Generates QR code. 'qrcode.jpg' is used as a placeholder for the QR code image which would be
displayed in the template.
"""
@app.route('/<fullname>/qrcode/', methods=['GET'])
def generate_qr(fullname):
    # Check that user exists, error otherwise
    user = User.objects(full_name=fullname).first()
    if user:
        # Create QR code instance and generate link to user's textbook titles
        code = QRCode(image_path = 'qrcode.jpg',
                      link = url_for('list_titles', fullname=user.full_name)).save()
        return jsonify(code)
    else:
        return jsonify('Not a valid user!')

if __name__ == '__main__':
    app.run(debug=True)