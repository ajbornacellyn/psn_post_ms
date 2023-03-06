from flask import Flask
from models import *
from controllers.posts_controller import posts_bp
from controllers.content_controller import contentElement_bp
from controllers.reaction_controller import reaction_bp
from mongoengine import connect

app = Flask(__name__)

# connect to database
MONGO_URI = 'mongodb://localhost:27017/psn_post_bd'
connect(host=MONGO_URI)

app.register_blueprint(posts_bp)
app.register_blueprint(contentElement_bp)
app.register_blueprint(reaction_bp)

if __name__ == '__main__':
    app.run(debug=True)