import json


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