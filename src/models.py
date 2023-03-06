from datetime import datetime
from flask_mongoengine import MongoEngine
from mongoengine import fields

db = MongoEngine()

class Report(db.EmbeddedDocument):
    _id = fields.ObjectIdField(primary_key=True, default = fields.ObjectId)
    owner_id = db.IntField()
    created_at = db.DateTimeField(default=datetime.now)
    updated_at = db.DateTimeField(default=datetime.now)
    infraction = db.StringField()
    description = db.StringField()

class ContentElement(db.EmbeddedDocument):
    _id = fields.ObjectIdField(primary_key=True, default = fields.ObjectId)
    description = db.StringField()
    type = db.StringField()
    locator = db.StringField()

class postShare(db.EmbeddedDocument):
    _id = fields.ObjectIdField(primary_key=True, default = fields.ObjectId)
    owner_id = db.IntField()
    id = db.IntField()
    name = db.StringField()
    description = db.StringField()
    content = db.ListField(db.EmbeddedDocumentField(ContentElement))

class Reaction(db.EmbeddedDocument):
    _id = fields.ObjectIdField(primary_key=True, default = fields.ObjectId)
    owner_id = db.IntField()
    type = db.StringField()
    created_at = db.DateTimeField(default=datetime.now)
    updated_at = db.DateTimeField(default=datetime.now)


class Post(db.Document):
    created_at = db.DateTimeField(default=datetime.now)
    updated_at = db.DateTimeField(default=datetime.now)
    owner_id = db.IntField()
    title = db.StringField()
    location = db.StringField()
    description = db.StringField()
    content = db.ListField(db.EmbeddedDocumentField(ContentElement))
    share = db.ListField(db.EmbeddedDocumentField(postShare))
    reaction = db.ListField(db.EmbeddedDocumentField(Reaction))
    report = db.ListField(db.EmbeddedDocumentField(Report))




