from flask import Flask, abort, jsonify, request
from test_template import TestMailTemplate
from utils import format_email_params, validated_response

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to Aviso Emial Testing API server</h1>" \
           "<p>This server is only meant for development purpose to check the output of your jinja template</p>"


@app.route('/testmail', methods=['POST'])
def testMail():
    requestData = request.json
    fieldList = ['html_file', 'payload', 'recipients', 'optional', 'subject']
    data, status, missing_params = format_email_params(requestData, fieldList)
    if not status:
        return validated_response(status, data, missing_params, 'missingParams')
    testObj = TestMailTemplate()
    sent_status, sent_response = testObj.send_mail(requestData['subject'], requestData['recipients'],
                                                   requestData['html_file'],
                                                   requestData['payload'], requestData['optional'])
    print sent_response
    response = validated_response(sent_status, data, sent_response, 'mailingError')
    return response


@app.route('/getparams', methods=['POST'])
def getParams():
    requestData = request.json
    data, status, missing_params = format_email_params(requestData, ['html_file'])
    if not status:
        return validated_response(status, data, missing_params, 'missingParams')
    testObj = TestMailTemplate()
    paramsList = testObj.get_template_params(data['html_file'])
    return jsonify({
            "success": True,
            "paramsList": paramsList,
            "data": data
        })


@app.route('/css-inline', methods=['POST'])
def getInlineCSS():
    requestData = request.json
    data, status, missing_params = format_email_params(requestData, ['html_file'])
    if not status:
        return validated_response(status, data, missing_params, 'missingParams')
    testObj = TestMailTemplate()
    html_data = testObj.premailer(data['html_file'])
    return jsonify({
            "success": True,
            "inline_css_html": html_data,
            "data": data
        })


if __name__ == '__main__':
    app.run(debug=True)
