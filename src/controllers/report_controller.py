from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from flask import jsonify

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('addReportToPost/', methods=['POST'])
def add_report_to_post():
    try:
        post_id = request.json['postId']
        post = Post.objects.get(id=ObjectId(post_id))
        if not post:
            return jsonify({'message': 'post not found'})
        report = Report(**request.json)
        report.save()
        return jsonify({'message': 'Report added successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
@report_bp.route('addReportToComment/', methods=['POST'])
def add_report_to_comment():
    try:
        comment_id = request.json['commentId']
        comment = Comment.objects.get(id=ObjectId(comment_id))
        if not comment:
            return jsonify({'message': 'comment not found'})
        report = Report(**request.json)
        report.save()
        return jsonify({'message': 'Report added successfully'})
    
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
    

@report_bp.route('<report_id>/', methods=['DELETE'])
def delete_report(report_id):
    try:
        report = Report.objects.get(id=ObjectId(report_id))
        if not report:
            return jsonify({'message': 'report not found'})
        report.delete()
        return jsonify({'message': 'Report deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    


# update pendiente
@report_bp.route('updateReportPost/<post_id>/<report_id>', methods=['PUT'])
def update_report_post(post_id, report_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        postReportList = post.report
        for report in postReportList:
            if report._id == ObjectId(report_id):
                report.owner_id = request.json['owner_id']
                report.infraction = request.json['infraction']
                report.description = request.json['description']
                #report.updateDate = db.DateTimeField(default=datetime.now) revisar por qué no deja cambiar la fecha
                post.save()
                return jsonify({'message': 'Report updated successfully'}), 201
            
        return jsonify({'message': 'Report not found'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})    

@report_bp.route('updateReportComment/<comment_id>/<report_id>', methods=['PUT'])
def update_report_comment(comment_id, report_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        commentReportList = comment.report
        for report in commentReportList:
            if report._id == ObjectId(report_id):
                report.owner_id = request.json['owner_id']
                report.infraction = request.json['infraction']
                report.description = request.json['description']
                #report.updateDate = db.DateTimeField(default=datetime.now)
                comment.save()
                return jsonify({'message': 'Report updated successfully'}), 201
            
        return jsonify({'message': 'Report not found'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)})
