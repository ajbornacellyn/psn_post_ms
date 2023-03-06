from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from flask import jsonify

report_bp = Blueprint('reaction', __name__, url_prefix='/reaction')

@report_bp.route('/<post_id>', methods=['POST'])
def add_report(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        report = Report(**request.json)
        post.report.append(report)
        post.save()
        return Response(report.to_json(), 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})

@report_bp.route('/<post_id>', methods=['GET'])
def get_reports(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        reports = post.report
        response = [report.to_json() for report in reports]
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})

@report_bp.route('/<post_id>/<report_id>', methods=['PUT'])
def update_report(post_id, report_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        report = post.report.get(id=ObjectId(report_id))
        report.update(**request.json)
        post.save()
        return Response(report.to_json(), 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})
