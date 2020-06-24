import os
import webbrowser
import codecs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pypremailer import Premailer
import traceback
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
        self.optional = []
        self.payload = {}

    def jinga_magic(self, file_path, payload={}, premailer=False):
        templateLoader = FileSystemLoader(searchpath="./templates/")
        templateEnv = Environment(loader=templateLoader, autoescape=select_autoescape(['html']))
        # validate the jinja template params
        if not premailer:
            self.validate_template_params(templateEnv, file_path)

        # load template with payload
        template = templateEnv.get_template(file_path)
        jinjaOutput = ""
        jinjaOutput += template.render(**payload)
        return jinjaOutput

    def validate_template_params(self, templateEnv, file_path):
        variables = set(self.get_template_params(file_path))
        diff = variables.difference(set(self.payload.keys()))
        diff = diff.difference(set(self.optional))
        if diff:
            raise MissingParams(list(diff))

    def premailer(self, file):
        html_data = self.jinga_magic(file, premailer=True)
        result = Premailer(html_data)
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

    def get_template_params(self, file):
        templateLoader = FileSystemLoader(searchpath="./templates/")
        templateEnv = Environment(loader=templateLoader, autoescape=select_autoescape(['html']))
        template_source = templateEnv.loader.get_source(templateEnv, file)[0]
        parsed_content = templateEnv.parse(template_source)
        return list(meta.find_undeclared_variables(parsed_content))

    def send_mail(self, subject, receivers, html_file, payload, optional):
        # specify the sender's and receive's email addresses
        try:
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
            return True, {}
        except Exception as err:
            return False, {'error': traceback.format_exc()}


    def main(self, html_file, payload={}, optional=[]):
        self.payload = payload
        self.optional = optional
        result = self.jinga_magic(html_file, payload)
        return result
        # chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        # webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path), 1)
        # write_html(result)
        # controller = webbrowser.get('chrome')
        # controller.open_new_tab('file://' + os.path.realpath('./templates/tmp.html'))
