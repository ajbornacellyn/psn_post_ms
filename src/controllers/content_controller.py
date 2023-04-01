from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from flask import jsonify
from mongoengine.errors import DoesNotExist, ValidationError

contentElement_bp = Blueprint('contentElement', __name__, url_prefix='/contentElement')


@contentElement_bp.route('/addContentToPost', methods=['POST'])
def add_contentElement():
    try:
        content_data = request.json
        content = ContentElement(**content_data)
        content.validate()
        post = Post.objects.get(_id=content_data['postId'])
        content.save()
        return Response(content.to_json(), 201, mimetype='application/json')

    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' post  not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500


@contentElement_bp.route('/addContentToComment', methods=['POST'])
def add_contentElement_to_comment():
    try:
        content_data = request.json
        content = ContentElement(**content_data)
        content.validate()
        comment = Comment.objects.get(_id=content_data['commentId'])
        content.save()
        return Response(content.to_json(), 201, mimetype='application/json')
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' comment  not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    

@contentElement_bp.route('getContentPost/<post_id>', methods=['GET'])
def get_contentElements_from_post(post_id):
    try:
        post = Post.objects.get(_id=post_id)
        contents = ContentElement.objects(postId=post_id)
        response = contents.to_json()
        return Response(response, 201, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' post not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    

@contentElement_bp.route('getContentComment/<comment_id>', methods=['GET'])
def get_contentElements_from_comment(comment_id):
    try:
        comment = Comment.objects.get(_id=comment_id)
        contentElements = ContentElement.objects(commentId=comment_id)
        return Response(response, 201, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' comment not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500



@contentElement_bp.route('deleteContentElement/<contentElement_id>', methods=['DELETE'])
def delete_contentElementt(contentElement_id):
    try:
        contentElement = ContentElement.objects.get(_id=contentElement_id)
        contentElement.delete()
        return jsonify({'message': 'ContentElement deleted successfully'}), 200
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' content element not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500




@contentElement_bp.route('/<contentElement_id>', methods=['PUT'])
def update_contentElement(contentElement_id):
    try:
        contentElement = ContentElement.objects.get(_id=contentElement_id)
        contentElement.update(**request.json)
        return jsonify({'message': 'ContentElement updated successfully'}), 200
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' content element not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    


    
    



