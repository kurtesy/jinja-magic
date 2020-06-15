import os
import webbrowser
import codecs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pypremailer import Premailer
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template, meta

from config.config_dev import mail_server
from custom_exception import MissingParams

class TestMailTemplate:
    def __init__(self):
        port = mail_server['port']
        smtp_server = mail_server['server']
        login = mail_server['user']
        password = mail_server['pwd']
        print('Connecting...')
        self.server = smtplib.SMTP(smtp_server, port)
        self.server.starttls()
        self.server.login(login, password)
        print('Connected to smtp mailtrap server')
        self.html = ""

    def jinga_magic(self, file_path, payload={}):
        templateLoader = FileSystemLoader(searchpath="./template-test/templates/")
        templateEnv = Environment(loader=templateLoader, autoescape=select_autoescape(['html']))

        # validate the jinja template params
        self.validate_template_params(templateEnv, file_path)

        # load template with payload
        template = templateEnv.get_template(file_path)
        jinjaOutput = ""
        jinjaOutput += template.render(**payload)
        return jinjaOutput

    def validate_template_params(self, templateEnv, file_path):
        template_source = templateEnv.loader.get_source(templateEnv, file_path)[0]
        parsed_content = templateEnv.parse(template_source)
        variables = meta.find_undeclared_variables(parsed_content)

        diff = variables.difference(set(self.payload.keys()))
        diff = diff.difference(set(self.optional))
        if diff:
            raise MissingParams(list(diff))

    def premailer(self, html_data):
        result = Premailer(html_data)
        print result.premail()
        return result.premail()


    def load_template(self, html_file):
        html_data = ''
        with open(html_file, 'r') as f:
            html_data = f.read()
        template = Template(html_data)
        return template

    def write_html(self, data):
        # data = data.decode('utf-8')
        with codecs.open('./templates/tmp.html', 'w', encoding="utf-8") as f:
            f.writelines(data)
        return True

    def send_mail(self, subject, receivers, html_file, payload, optional):
        # specify the sender's and receive's email addresses
        sender = "admin@aviso.com"
        message = MIMEMultipart("alternative")

        # convert both parts to MIMEText objects and add them to the MIMEMultipart message
        html = self.main(html_file, payload, optional)
        html = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
        message.attach(html)

        for receiver in receivers:
            message["Subject"] = subject
            message["From"] = sender
            message["To"] = receiver

            # send your email
            self.server.sendmail(
                sender, receiver, message.as_string()
            )
        print('Sent')

    def main(self, html_file, payload={}, optional=[]):
        self.payload = payload
        self.optional = optional
        result = self.jinga_magic(html_file, payload)
        premailer_result = self.premailer(result)
        return result
        # chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        # webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path), 1)
        # write_html(result)
        # controller = webbrowser.get('chrome')
        # controller.open_new_tab('file://' + os.path.realpath('./templates/tmp.html'))


t = TestMailTemplate()
html_file = 'Welcome to Aviso!.html'
payload = {
            "external_user": "Nishant",
            "host_full_name": "Nishant Patel",
            "deal_name": "Deal",
            "room_url": "https://www.google.com",
            "tenant_name": "SPLUNK"
        }
optional = ['opens_tracker']
t.send_mail(html_file, ['nishant.patel@aviso.com'], html_file, payload, optional)