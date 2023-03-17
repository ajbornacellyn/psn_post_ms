from flask import Flask, Response, Blueprint, request, jsonify
from pydantic import ValidationError
from models import *
from bson  import  ObjectId, json_util
from mongoengine.errors import DoesNotExist



posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/', methods=['POST'])
def add_post():
    try:
        post_data = request.get_json()
        if not post_data:
            return jsonify({'error': 'No data provided'}), 400
        
        post = Post(**post_data)
        post.save()
        
        return jsonify({'message': 'Post added successfully'}), 201

    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'message': str(e)}), 400

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500


@posts_bp.route('/', methods=['GET'])
def get_posts():
    try:
        posts = Post.objects().to_json()
        response = posts
        return Response(response, mimetype='application/json')

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500


@posts_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        response = post.to_json()
        return Response(response, 201, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'error': 'Post not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500


@posts_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        post.update(**request.json)
        return jsonify({'message': 'Post updated successfully'}),200
    
    except DoesNotExist:
        return jsonify({'error': 'Post not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500


@posts_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        post.delete()
        return jsonify({"message": "Post deleted"})

    except DoesNotExist:
        return jsonify({'error': 'Post not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500


@posts_bp.route('/orderByDate', methods=['GET'])
def get_posts_by_date():
    try:
        posts = Post.objects().order_by('created_at')
        response = posts.to_json()
        return Response(response, mimetype='application/json')

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500


