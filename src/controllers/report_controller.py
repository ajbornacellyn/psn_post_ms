from flask import Response, Blueprint, request
from models import *
from bson  import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError
from flask import jsonify

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('/addReportToPost', methods=['POST'])
def add_report_to_post():
    try:
        report_data = request.get_json()
        report = Report(**report_data)
        report.validate()
        post = Post.objects.get(_id=report_data['postId'])
        report.save()
        response = report.to_json()
        return Response(response, 201, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' post not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
@report_bp.route('/addReportToComment', methods=['POST'])
def add_report_to_comment():
    try:
        report_data = request.get_json()
        report = Report(**request.json)
        report.validate()
        comment = Comment.objects.get(_id=report_data['commentId'])
        report.save()
        response = report.to_json()
        return Response(response, 201, mimetype='application/json')

    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' comment not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
@report_bp.route('/getReportPost/<post_id>', methods=['GET'])
def get_reports(post_id):
    try:
        post = Post.objects.get(_id=post_id)
        reports = Report.objects(postId=post_id)
        response = reports.to_json()
        return Response(response, 200, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' post not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    

@report_bp.route('/getReportComment/<comment_id>', methods=['GET'])
def get_reports_from_comment(comment_id):
    try:
        comment = Comment.objects.get(_id=comment_id)
        reports = Report.objects(commentId=comment_id)
        return Response(response, 201, mimetype='application/json')
    
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' comment not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
    
    

@report_bp.route('/<report_id>', methods=['DELETE'])
def delete_report(report_id):
    try:
        report = Report.objects.get(_id=report_id)
        report.delete()
        return jsonify({'message': 'Report deleted successfully'})

    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' report not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500
    
    


# update pendiente
@report_bp.route('/<report_id>', methods=['PUT'])
def update_report(report_id):
    try:
        report = Report.objects.get(id=report_id)
        report.update(**request.json)
        response = report.to_json()
        return Response(response, 200, mimetype='application/json')
        
    except DoesNotExist:
        return jsonify({'statusCode': 404,'message': ' report not found'}), 404

    except ValidationError as e:
        return jsonify({'statusCode': 400,'message': 'Bad request'}), 400

    except Exception as e:
        return jsonify({'statusCode': 500,'message': str(e)}), 500   


