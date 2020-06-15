from flask import Flask, abort, jsonify, request

from utils import format_email_params

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to Aviso Emial Testing API server</h1>" \
           "<p>This server is only meant for development purpose to check the output of your jinja template</p>"


@app.route('/testmail', methods=['POST'])
def testmail():
    requestData = request.json
    fieldList = ['html_file', 'payload', 'recipients', 'optional']
    data, status, missing_params = format_email_params(requestData, fieldList)
    payload = {}
    if status:
        response = jsonify({
            "success": True,
            "message": "Mail sent successfully!",
            "data": data
            })
    else:
        response = jsonify({
            "success": False,
            "message": "Mail sending failed due to missing params: {}".format(missing_params),
            "data": data
        })

    return response

@app.route('/getParams', methods=['POST'])
def getParams():
    requestData = request.json
    data = format_email_params(requestData, ['html_file'])


if __name__ == '__main__':
    app.run(debug=True)