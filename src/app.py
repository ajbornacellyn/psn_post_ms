from flask import Flask
from controllers.posts_controller import posts_bp
from controllers.content_controller import contentElement_bp
from controllers.reaction_controller import reaction_bp
from controllers.report_controller import report_bp
from controllers.comment_controller import Comment_bp
from mongoengine import connect

app = Flask(__name__)

# connect to database
MONGO_URI = 'mongodb+srv://jrojasce:jkvUIs1rFxeB4NHR@psn-post-db.izodfgc.mongodb.net/test'
connect(host=MONGO_URI)

app.register_blueprint(posts_bp)
app.register_blueprint(contentElement_bp)
app.register_blueprint(reaction_bp)
app.register_blueprint(report_bp)
app.register_blueprint(Comment_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080 , debug=True)