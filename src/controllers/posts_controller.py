from flask import Flask, Response, Blueprint, request, jsonify
from pydantic import ValidationError
from models import *
from bson  import  ObjectId, json_util


posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/', methods=['POST'])
def add_post():
    try:
        post_data = request.json
        post = Post(**post_data)

    except ValidationError as e:
        return e.json(), 400
    
    post.save()
    return Response(post.to_json(), 201, mimetype='application/json')

@posts_bp.route('/', methods=['GET'])
def get_posts():
    posts =   Post.objects().to_json()
    response = posts
    return Response(response, mimetype='application/json')

@posts_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        response = post.to_json()
        return Response(response, 201, mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)})
    
@posts_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        post.update(**request.json)
        return Response(post.to_json(), 201, mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)})
    
@posts_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        post.delete()
        return jsonify({"message": "Post deleted"})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@posts_bp.route('/orderByDate', methods=['GET'])
def get_posts_by_date():
    posts = Post.objects().order_by('created_at')
    response = posts.to_json()
    return Response(response, mimetype='application/json')




