from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from flask import jsonify

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('addReportToPost/<post_id>', methods=['POST'])
def add_report_to_post(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        report = Report(**request.json)
        post.report.append(report)
        post.save()
        return jsonify({'message': 'Report added successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@report_bp.route('addReportToComment/<comment_id>', methods=['POST'])
def add_report_to_comment(comment_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        report = Report(**request.json)
        comment.report.append(report)
        comment.save()
        return jsonify({'message': 'Report added successfully'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@report_bp.route('getReportPost/<post_id>', methods=['GET'])
def get_reports(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        reports = post.report
        response = [report.to_json() for report in reports]
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})
    

@report_bp.route('getReportComment/<comment_id>', methods=['GET'])
def get_reports_from_comment(comment_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        reports = comment.report
        response = [report.to_json() for report in reports]
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'error': str(e)})
    

@report_bp.route('deleteReportPost/<post_id>/<report_id>', methods=['DELETE'])
def delete_report_post(post_id, report_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        post.update(pull__report__id=Report(_id = ObjectId(report_id)))
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@report_bp.route('deleteReportComment/<comment_id>/<report_id>', methods=['DELETE'])
def delete_report_comment(comment_id, report_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        comment.update(pull__report__id=Report(_id = ObjectId(report_id)))
    
    except Exception as e:
        return jsonify({'error': str(e)})
    

