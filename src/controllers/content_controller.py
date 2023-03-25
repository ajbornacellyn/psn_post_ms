from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from flask import jsonify


contentElement_bp = Blueprint('contentElement', __name__, url_prefix='/contentElement')


@contentElement_bp.route('/', methods=['POST'])
def add_contentElement():
    try:
        content_data = request.json
        if 'postId' in content_data:
            post = Post.objects(id=ObjectId(content_data['postId'])).first()
            if not post:
                return jsonify({'message': 'post not found'})
            else:
                content = ContentElement(**request.json)
                content.save()
                return jsonify({'message': 'ContentElement added successfully'})
        elif 'commentId' in content_data:
            comment = Comment.objects(id=ObjectId(content_data['commentId'])).first()
            if not comment:
                return jsonify({'message': 'comment not found'})
            else:
                content = ContentElement(**request.json)
                content.save()
                return jsonify({'message': 'ContentElement added successfully'})
        else:
            return jsonify({'message': 'please provide a post or comment id'})

    except Exception as e:
        return jsonify({'error': str(e)})
    
@contentElement_bp.route('getContentPost/<post_id>', methods=['GET'])
def get_contentElements(post_id):
    try:
        contents = ContentElement.objects.get(id=ObjectId(post_id))
        response = contents.to_json()
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@contentElement_bp.route('getContentComment/<comment_id>', methods=['GET'])
def get_contentElements_from_comment(comment_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        contentElements = comment.contentElement
        response = [contentElement.to_json() for contentElement in contentElements]
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})



@contentElement_bp.route('deleteContentPost/<post_id>/<contentElement_id>', methods=['DELETE'])
def delete_contentElementt_post(post_id, contentElement_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        post.update(pull__contentElement__=ContentElement(_id = ObjectId(contentElement_id)))
        return jsonify({'message': 'ContentElement deleted successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})


@contentElement_bp.route('deleteContentComment/<comment_id>/<contentElement_id>', methods=['DELETE'])
def delete_contentElement_comment(comment_id, contentElement_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        comment.update(pull__contentElement__=ContentElement(_id = ObjectId(contentElement_id)))
        return jsonify({'message': 'ContentElement deleted successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})
    


@contentElement_bp.route('/<post_id>/<contentElement_id>', methods=['PUT'])
def update_contentElement_post(post_id, contentElement_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        contentElement = ContentElement.objects.get(id=ObjectId(contentElement_id))
        contentElement.update(**request.json)
        return jsonify({'message': 'ContentElement updated successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@contentElement_bp.route('/<comment_id>/<contentElement_id>', methods=['PUT'])
def update_contentElement_comment(comment_id, contentElement_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        contentElement = ContentElement.objects.get(id=ObjectId(contentElement_id))
        contentElement.update(**request.json)
        return jsonify({'message': 'ContentElement updated successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})

    
    



