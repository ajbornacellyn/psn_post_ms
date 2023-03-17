from flask import Flask, Response, Blueprint, request, jsonify
from pydantic import ValidationError
from models import *
from bson  import  ObjectId, json_util
from mongoengine.errors import DoesNotExist


Comment_bp = Blueprint('Comment', __name__, url_prefix='/comment')

@Comment_bp.route('/', methods=['POST'])
def add_comment():
    try:
        comment_data = request.get_json()

        # Verificar que el objeto JSON tenga los campos requeridos
        if 'postId' not in comment_data or 'description' not in comment_data:
            return jsonify({'error': 'Required fields are missing'}), 400

        # Verificar que el post exista
        post = Post.objects(id=ObjectId(comment_data['postId'])).first()
        if not post:
            return jsonify({'error': 'Post not found'}), 404

        # Crear y guardar el comentario
        comment = Comment(**comment_data)
        comment.save()

        return jsonify({'message': 'Comment added successfully'}), 201

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500
    
@Comment_bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        response = comment.to_json()
        return Response(response, 201, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'error': 'Comment not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
    
@Comment_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    try:
        comment = Comment.objects(id=ObjectId(comment_id))
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        comment.update(**request.json)
        return jsonify({'message': 'Comment updated successfully'}),200
    
    except DoesNotExist:
        return jsonify({'error': 'Comment not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
    
@Comment_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        comment = Comment.objects(id=ObjectId(comment_id))
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        comment.delete()
        return jsonify({'message': 'Comment deleted successfully'}), 200
    
    except DoesNotExist:
        return jsonify({'error': 'Comment not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
    

@Comment_bp.route('/allComments/<post_id>', methods=['get'])
def get_all_comments(post_id):
    try:
        comments = Comment.objects(postId=ObjectId(post_id)).to_json()
        response = comments
        return Response(response, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'error': 'Comment not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500


    


