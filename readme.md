#Email template testing for Jinja-Gmail
This is a testing app endpoint for testing templates with jinja formatting and check the mail sending to your mail

##Email protocol:
Email protocol used is SMTP
Server used: gmail smtp

##Setup guidelines:

1. Place the folder `template-test` inside python-sdk repo directory in your local
2. activate the virtual environment
    `source {your_virtual_env}/bin/activate`
3. Navigate to `template-test` folder
4. Run pip install -r dev_requirements.txt
5. Run the server:
    `python server`
6. place your html file and assets inside `templates` folder

##API endpoints:(Use Postman or curl request)
1. Home Page to check server status-[GET]
    url=localhost:5000/
2. Test your Email:[POST]
    url=localhost:5000/testmail
    content-type='application/json'
    post-data=
    {
        "html_file": "name_of_your_html_template.html", (String)
        "payload": JSON object for jinja template payload, (JSON Object)
        "recipients": Array with list of strings of recipient email addresses (Array)
        "optional": Optional fields list in your jinja template (Array)
    }

    Sample request and response:
    URL='http://127.0.0.1:5000/testmail'

    Request JSON-
    {
	"html_file": "Welcome to Aviso!.html",
	"payload": {
            "external_user": "Nishant",
            "host_full_name": "Nishant Patel",
            "deal_name": "Deal",
            "room_url": "https://www.google.com",
            "tenant_name": "SPLUNK"
        },
    "optional": ["opens_tracker"],
    "recipients": ["nishant.patel@aviso.com", "test123@aviso.com"]
    }

    Response JSON-
    {
  "data": {
    "html_file": "Welcome to Aviso!.html",
    "optional": [
      "opens_tracker"
    ],
    "payload": {
      "deal_name": "Deal",
      "external_user": "Nishant",
      "host_full_name": "Nishant Patel",
      "room_url": "https://www.google.com",
      "tenant_name": "SPLUNK"
    },
    "recipients": [
      "nishant.patel@aviso.com",
      "test123@aviso.com"
    ]
  },
  "message": "Mail sent successfully!",
  "success": true
}


