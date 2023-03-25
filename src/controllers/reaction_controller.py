from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId, json_util
from flask import jsonify
from controllers.pipelines import getReactionPipeline

reaction_bp = Blueprint('reaction', __name__, url_prefix='/reaction')

@reaction_bp.route('reactToPost', methods=['POST'])
def add_reaction_to_post():
    try:
        post_id = request.json['postId']
        post = Post.objects.get(id=ObjectId(post_id))
        if not post:
            return jsonify({'message': 'post not found'})
        reaction = Reaction(**request.json)
        reaction.save()
        return jsonify({'message': 'Reaction added successfully'}), 201
    
    except Exception as e:
        return jsonify({'message': str(e)})
    
@reaction_bp.route('reactToComment', methods=['POST'])
def add_reaction_to_comment():
    try:
        comment_id = request.json['commentId']
        comment = Comment.objects.get(id=ObjectId(comment_id))
        if not comment:
            return jsonify({'message': 'comment not found'})
        reaction = Reaction(**request.json)
        reaction.save()
        return jsonify({'message': 'Reaction added successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@reaction_bp.route('/', methods=['GET'])
def get_reactions():
    try:
        pipeline = getReactionPipeline()
        reactions = Reaction.objects.aggregate(pipeline)
        response = json_util.dumps(reactions)
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})
     
    
@reaction_bp.route('/<reaction_id>', methods=['DELETE'])
def delete_reaction(reaction_id):
    try:
        reaction = Reaction.objects.get(id=ObjectId(reaction_id))
        print(reaction)
        if reaction:
            reaction.delete()
            return jsonify({'message': 'Reaction deleted successfully'})
        else:
            return jsonify({'message': 'Reaction not found'})
    except Exception as e:
        return jsonify({'error': str(e)})


@reaction_bp.route('/<reaction_id>', methods=['PUT'])
def update_reaction(reaction_id):
    try:
        reaction = Reaction.objects.get(id=ObjectId(reaction_id))
        if reaction:
            reaction.update(**request.json)
            return jsonify({'message': 'Reaction updated successfully'})
        else:
            return jsonify({'message': 'Reaction not found successfully'})
    
    except Exception as e:
        return jsonify({'message': str(e)})

