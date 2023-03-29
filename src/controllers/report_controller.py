from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError
from flask import jsonify

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('/addReportToPost', methods=['POST'])
def add_report_to_post():
    try:
        post_id = request.json['postId']
        post = Post.objects.get(id=ObjectId(post_id))

        report = Report(**request.json)
        report.save()
        return jsonify({'message': 'Report added successfully'})
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' post not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
@report_bp.route('/addReportToComment', methods=['POST'])
def add_report_to_comment():
    try:
        comment_id = request.json['commentId']
        comment = Comment.objects.get(id=ObjectId(comment_id))

        report = Report(**request.json)
        report.save()
        return jsonify({'message': 'Report added successfully'})
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' comment not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
@report_bp.route('/getReportPost/<post_id>', methods=['GET'])
def get_reports(post_id):
    try:
        post = Post.objects.get(id=ObjectId(post_id))
        reports = post.report
        response = [report.to_json() for report in reports]
        return Response(response, 200, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    

@report_bp.route('/getReportComment/<comment_id>', methods=['GET'])
def get_reports_from_comment(comment_id):
    try:
        comment = Comment.objects.get(id=ObjectId(comment_id))
        reports = comment.report
        response = [report.to_json() for report in reports]
        return Response(response, 201, mimetype='application/json')
    
    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
    

@report_bp.route('/<report_id>', methods=['DELETE'])
def delete_report(report_id):
    try:
        report = Report.objects.get(id=ObjectId(report_id))
        report.delete()
        return jsonify({'message': 'Report deleted successfully'})

    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' report not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
    


# update pendiente
@report_bp.route('/updateReportPost/<post_id>/<report_id>', methods=['PUT'])
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
            
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' post not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500   


@report_bp.route('/updateReportComment/<comment_id>/<report_id>', methods=['PUT'])
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
            
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' comment not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
