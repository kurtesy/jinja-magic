import json
from flask import jsonify

ERROR_MAP = {
    'missingParams': lambda z: "Mail sending failed due to missing params: {}".format(z),
    'mailingError': lambda z: "Mail sending failed mail server error: {}".format(z),
}

def format_email_params(requestData, fields):
    result = {}
    missing_params = []
    status = True
    for field in fields:
        if field in requestData:
            result[field] = requestData[field]
        else:
            result[field] = None
            missing_params.append(field)
            status = False
    return result, status, missing_params


def validated_response(status, data, error, type):

    if status:
        response = jsonify({
            "success": True,
            "message": "Mail sent successfully!",
            "data": data
        })
    else:
        response = jsonify({
            "success": False,
            "message": ERROR_MAP[type],
            "data": data,
            "error-code": type
        })
    return response
