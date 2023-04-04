from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId, json_util
from flask import jsonify
from mongoengine.errors import DoesNotExist, ValidationError
from controllers.pipelines import getReactionPipeline

reaction_bp = Blueprint('reaction', __name__, url_prefix='/reaction')

@reaction_bp.route('reactToPost', methods=['POST'])
def add_reaction_to_post():
    try:
        reaction = Reaction(**request.json)
        reaction.validate()
        postId = request.json['postId']
        post = Post.objects.get(_id=postId)
        reaction.save()
        response = reaction.to_json()
        return Response(response, 201, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' post not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
@reaction_bp.route('reactToComment', methods=['POST'])
def add_reaction_to_comment():
    try:
        reaction = Reaction(**request.json)
        reaction.validate()
        commentId = request.json['commentId']
        post = Comment.objects.get(_id=commentId)
        reaction.save()
        response = reaction.to_json()
        return Response(response, 201, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': 'Comment not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
@reaction_bp.route('/', methods=['GET'])
def get_reactions():
    try:
        reactions = Reaction.objects()
        response = reactions.to_json()
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
     
    
@reaction_bp.route('/<reaction_id>', methods=['DELETE'])
def delete_reaction(reaction_id):
    try:
        reaction = Reaction.objects.get(_id=reaction_id)
        reaction.delete()
      
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' reaction not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500

@reaction_bp.route('/<reaction_id>', methods=['PUT'])
def update_reaction(reaction_id):
    try:
        reaction = Reaction.objects.get(_id=reaction_id)
        reaction.update(**request.json)
        response = reaction.to_json()
        return Response(response, 201, mimetype='application/json')
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' reaction not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500

