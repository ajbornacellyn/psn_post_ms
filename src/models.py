from datetime import datetime
from tkinter import CASCADE
from flask_mongoengine import MongoEngine
from mongoengine import fields
import json
import bson
from bson import ObjectId
from mongoengine import *


db = MongoEngine()

class Post(db.Document):
    _id = db.StringField(primary_key=True, default=lambda: str(ObjectId()))
    idOriginalPost = db.StringField(default=None)
    createdDate = db.DateTimeField(default=datetime.now)
    updatedDate= db.DateTimeField(default=datetime.now)
    ownerId = db.IntField(required=True)
    location = db.StringField(default=None)
    description = db.StringField(required=True)
    comment = db.ListField(fields.ReferenceField('Comment'), default=None, reverse_delete_rule=CASCADE)
    reaction = db.ListField(fields.ReferenceField('Reaction'), default=None, reverse_delete_rule=CASCADE)
    report = db.ListField(fields.ReferenceField('Report'), default=None, reverse_delete_rule=CASCADE)
    contentElement = db.ListField(fields.ReferenceField('ContentElement'), default=None, reverse_delete_rule=CASCADE)
    

class Comment(db.Document):
    _id = db.StringField(primary_key=True, default=lambda: str(ObjectId()))
    parentCommentId = db.ReferenceField('self', reverse_delete_rule=CASCADE, required=False, min_length=1)
    postId = fields.ReferenceField('Post', reverse_delete_rule=CASCADE, required=False, min_length=1)
    ownerId = db.IntField()
    createdDate = db.DateTimeField(default=datetime.now)
    updatedDate= db.DateTimeField(default=datetime.now)
    description = db.StringField()
    reaction = db.ListField(fields.ReferenceField('Reaction'), default=None, reverse_delete_rule=CASCADE)
    report = db.ListField(fields.ReferenceField('Report'), default=None, reverse_delete_rule=CASCADE)
    contentElement = db.ListField(fields.ReferenceField('ContentElement'), default=None, reverse_delete_rule=CASCADE)

    def clean(self):
        if not self.postId and not self.parentCommentId:
            raise ValidationError('Al menos uno de los dos campos es requerido.')

class Report(db.Document):
    _id = db.StringField(primary_key=True, default=lambda: str(ObjectId()))
    postId = fields.ReferenceField('Post', reverse_delete_rule=CASCADE, required=False)
    commentId = fields.ReferenceField('Comment', reverse_delete_rule=CASCADE, required=False)
    ownerId = db.IntField(required=True)
    cretedDate = db.DateTimeField(default=datetime.now, required=True)
    updatedDate = db.DateTimeField(default=datetime.now, required=True)
    infraction = db.StringField()
    description = db.StringField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.id_str = str(self.id)
        super().save(*args, **kwargs)


class ContentElement(db.Document):
    _id = db.StringField(primary_key=True, default=lambda: str(ObjectId()))
    postId = fields.ReferenceField('Post', reverse_delete_rule=CASCADE, required=False, min_length=1)
    commentId = fields.ReferenceField('Comment', reverse_delete_rule=CASCADE, required=False, min_length=1)
    description = db.StringField()
    mediaLocator = db.StringField()
    mediaType = db.StringField()
    def clean(self):
        if not self.postId and not self.commentId:
            raise ValidationError('Al menos uno de los dos campos es requerido.')



class Reaction(db.Document):
    _id = db.StringField(primary_key=True, default=lambda: str(ObjectId()))
    postId = fields.ReferenceField('Post', reverse_delete_rule=CASCADE, required=False)
    commentId = fields.ReferenceField('Comment', reverse_delete_rule=CASCADE, required=False)
    ownerId = db.IntField()
    type = db.StringField()
    createdDate = db.DateTimeField(default=datetime.now)
    updatedDate = db.DateTimeField(default=datetime.now)



