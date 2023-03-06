from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from flask import jsonify

reaction_bp = Blueprint('reaction', __name__, url_prefix='/reaction')

@reaction_bp.route('/<post_id>', methods=['POST'])
def add_reaction(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        reaction = Reaction(**request.json)
        post.reaction.append(reaction)
        post.save()
        return Response(reaction.to_json(), 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@reaction_bp.route('/<post_id>', methods=['GET'])
def get_reactions(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        reactions = post.reaction
        response = [reaction.to_json() for reaction in reactions]
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})