from datetime import datetime
from tkinter import CASCADE
from flask_mongoengine import MongoEngine
from mongoengine import fields

db = MongoEngine()

class Report(db.EmbeddedDocument):
    _id = fields.ObjectIdField(primary_key=True, default = fields.ObjectId)
    owner_id = db.IntField()
    cretedDate = db.DateTimeField(default=datetime.now)
    updateDate = db.DateTimeField(default=datetime.now)
    infraction = db.StringField()
    description = db.StringField()

class ContentElement(db.EmbeddedDocument):
    _id = fields.ObjectIdField(primary_key=True, default = fields.ObjectId)
    description = db.StringField()
    mediaLocator = db.StringField()
    mediaType = db.StringField()


class Reaction(db.EmbeddedDocument):
    _id = fields.ObjectIdField(primary_key=True, default = fields.ObjectId)
    owner_id = db.IntField()
    type = db.StringField()
    createdDate = db.DateTimeField(default=datetime.now)
    updatedDate = db.DateTimeField(default=datetime.now)


    
class Post(db.Document):
    idOriginalPost = fields.ObjectIdField( default= None)
    createdDate = db.DateTimeField(default=datetime.now)
    updatedDate= db.DateTimeField(default=datetime.now)
    ownerId = db.IntField(required=True)
    location = db.StringField(default=None)
    description = db.StringField(required=True)
    contentElement = db.ListField(db.EmbeddedDocumentField(ContentElement))
    reaction = db.ListField(db.EmbeddedDocumentField(Reaction))
    report = db.ListField(db.EmbeddedDocumentField(Report))
    comment = db.ListField(fields.ReferenceField('Comment'), default=None, reverse_delete_rule=CASCADE)

class Comment(db.Document):
    postId = fields.ReferenceField('Post', reverse_delete_rule=CASCADE, required=True)
    ownerId = db.IntField()
    createdDate = db.DateTimeField(default=datetime.now)
    updatedDate= db.DateTimeField(default=datetime.now)
    description = db.StringField()
    reaction = db.ListField(db.EmbeddedDocumentField(Reaction))
    report = db.ListField(db.EmbeddedDocumentField(Report))
    contentElement = db.ListField(db.EmbeddedDocumentField(ContentElement))








