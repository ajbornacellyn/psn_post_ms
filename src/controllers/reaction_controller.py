from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from flask import jsonify

reaction_bp = Blueprint('reaction', __name__, url_prefix='/reaction')

@reaction_bp.route('addReactionToPost/<post_id>', methods=['POST'])
def add_reaction_to_post(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        reaction = Reaction(**request.json)
        post.reaction.append(reaction)
        post.save()
        return jsonify({'message': 'Reaction added successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@reaction_bp.route('addReactionToComment/<comment_id>', methods=['POST'])
def add_reaction_to_comment(comment_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        reaction = Reaction(**request.json)
        comment.reaction.append(reaction)
        comment.save()
        return jsonify({'message': 'Reaction added successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@reaction_bp.route('getReactionPost/<post_id>', methods=['GET'])
def get_reactions(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        reactions = post.reaction
        response = [reaction.to_json() for reaction in reactions]
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@reaction_bp.route('getReactionComment/<comment_id>', methods=['GET'])
def get_reactions_from_comment(comment_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        reactions = comment.reaction
        response = [reaction.to_json() for reaction in reactions]
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})
    




@reaction_bp.route('deleteReactionPost/<post_id>/<reaction_id>', methods=['DELETE'])
def delete_reaction_post(post_id, reaction_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        post.update(pull__reaction__=Reaction(_id = ObjectId(reaction_id)))
        post.save()

        return jsonify({'message': 'Reaction deleted successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@reaction_bp.route('deleteReactionComment/<comment_id>/<reaction_id>', methods=['DELETE'])
def delete_reaction_comment(comment_id, reaction_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        comment.update(pull__reaction__=Reaction(_id = ObjectId(reaction_id)))
        comment.save()

        return jsonify({'message': 'Reaction deleted successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})


@reaction_bp.route('updateReactionComment/<comment_id>/<reaction_id>', methods=['PUT'])
def update_reaction_comment(comment_id, reaction_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        comment.update(pull__reaction__=Reaction(_id = ObjectId(reaction_id)))
        comment.save()
        return jsonify({'message': 'Reaction updated successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})

@reaction_bp.route('updateReactionPost/<post_id>/<reaction_id>', methods=['PUT'])
def update_reaction_post(post_id, reaction_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        post.update(pull__reaction__=Reaction(_id = ObjectId(reaction_id)))
        post.save()
        return jsonify({'message': 'Reaction updated successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})