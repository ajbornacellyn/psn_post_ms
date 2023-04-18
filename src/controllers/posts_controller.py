from flask import Flask, Response, Blueprint, request, jsonify
from models import *
from bson  import  ObjectId, json_util
from mongoengine.errors import DoesNotExist, ValidationError
from controllers.pipelines import *

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/', methods=['POST'])
def add_post():
    try:
        post_data = request.get_json()
        if 'idOriginalPost' in post_data:
            post_id = post_data['idOriginalPost']
            postOriginal = Post.objects.get(_id=post_id)
            post = Post(**post_data)
            post.save()
            response = post.to_json()
            return Response(response, mimetype='application/json')
        else:    
            post = Post(**post_data)
            post.save()
            response = post.to_json()
            return Response(response, mimetype='application/json')

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': str(e)}), 400
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': 'post not found'}), 404

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
        
# get all posts only information about post
@posts_bp.route('/', methods=['GET'])
def get_all_posts():
    try:
        pipeline = getPostPipeline()
        result = Post.objects.aggregate(*pipeline)
        response = json_util.dumps(result)
        return Response(response, mimetype='application/json')
    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500

# get post by id, wiht all information
@posts_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    try:
        pipeline = getPostPipeline(post_id)
        post = Post.objects.aggregate(*pipeline)
        response = json_util.dumps(post)
        return Response(response, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'statusCode': 400,'message': 'post not found'}), 400
    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500

# get all posts by owner, with all information about post order by date
@posts_bp.route('/findPostsByOwner/<owner_id>', methods=['GET'])
def get_posts_by_owner(owner_id):
    try:
        pipeline = getPostsByOwner(owner_id)
        posts = Post.objects.aggregate(*pipeline)
        print(posts)
        response = json_util.dumps(posts)
        return Response(response, mimetype='application/json')
    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500

# get all posts with #comments, #reactions and content element 
@posts_bp.route('/postInfo', methods=['GET'])
def get_posts_Info():
    try:
        pipeline = getPostcontentElementPipeline()
        response = Post.objects.aggregate(*pipeline)
        response = json_util.dumps(response)
        return Response(response, mimetype='application/json')
    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500


@posts_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        post = Post.objects.get(_id=post_id)
        post.update(**request.json)
        post.save()
        post.reload()
        response = post.to_json()
        return Response(response,status=200,  mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': 'post not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500


@posts_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        post = Post.objects.get(_id=post_id)
        post.delete()
        return jsonify({"message": "Post deleted"})

    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': 'post not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500



