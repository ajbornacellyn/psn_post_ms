from flask import Flask, Response, Blueprint, request, jsonify
from models import *
from bson  import  ObjectId, json_util
from mongoengine.errors import *
from controllers.pipelines import *


Comment_bp = Blueprint('Comment', __name__, url_prefix='/comment')


@Comment_bp.route('/', methods=['POST'])
def add_comment():
    try:
        comment_data = request.get_json()
        comment = Comment(**comment_data)
        comment.validate()
        post = Post.objects.get(_id=comment_data['postId'])
        comment.save()
        response = comment.to_json()
        return Response(response, mimetype='application/json')

    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' post not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except FieldDoesNotExist as e:
        return jsonify({'statusCode': 400,'message': str(e)}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500

@Comment_bp.route('/commentToComment', methods=['POST'])
def comment_to_comment():
        try:
            comment_data = request.get_json()
            comment = Comment(**comment_data)
            comment.validate()
            parentComment = Comment.objects.get(_id=comment_data['parentCommentId'])
            comment.save()
            response = comment.to_json()
            return Response(response, mimetype='application/json')
    
        except DoesNotExist:
            return jsonify({'statusCode': 404,'message': ' comment not found'}), 404
    
        except ValidationError as e:
            return jsonify({'statusCode': 400,'message': 'Bad request'}), 400
    
        except FieldDoesNotExist as e:
            return jsonify({'statusCode': 400,'message': str(e)}), 400
    
        except Exception as e:
            return jsonify({'statusCode': 500,'message': str(e)}), 500   

@Comment_bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    try:
        comment = Comment.objects(_id=comment_id).first()
        if not comment:
            return jsonify({'error': 'Comment not found'})
        
        response = comment.to_json()
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@Comment_bp.route('/commentsThread/<postId>', methods=['GET'])
def get_comments_thread(postId):
    try:
        pipeline = getCommentsThreadPipeline(postId)
        comments = Comment.objects.aggregate(*pipeline)
        response = json_util.dumps(comments)
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

    
@Comment_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    try:
        comment = Comment.objects.get(_id=comment_id)
        comment.update(**request.json)
        comment.save()
        comment.reload()
        response = comment.to_json()
        return Response(response, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'error': 'Comment not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
    
@Comment_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        comment = Comment.objects.get(_id=comment_id)
        comment.delete()
        return jsonify({'message': 'Comment deleted successfully'}), 200
    
    except DoesNotExist:
        return jsonify({'error': 'Comment not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
    

@Comment_bp.route('/allComments/<post_id>', methods=['get'])
def get_all_comments(post_id):
    try:
        pipeline = getCommentsPostPipeline(post_id)
        comments = Comment.objects(postId=post_id).aggregate(*pipeline)
        response = json_util.dumps(comments)
        return Response(response, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'error': 'Comment not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500


    


