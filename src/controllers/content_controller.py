from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from flask import jsonify


contentElement_bp = Blueprint('contentElement', __name__, url_prefix='/contentElement')


@contentElement_bp.route('/<post_id>', methods=['POST'])
def add_contentElement(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        contentElement = ContentElement(**request.json)
        post.content.append(contentElement)
        post.save()
        return Response(contentElement.to_json(), 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@contentElement_bp.route('/<post_id>', methods=['GET'])
def get_contentElements(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        contentElements = post.content
        response = [contentElement.to_json() for contentElement in contentElements]
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})



    
    



