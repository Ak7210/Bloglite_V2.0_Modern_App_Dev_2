from applications.jobs import celery
from . import *
# from flask_mail import Message
from celery.schedules import crontab # crontab is a class
from applications.models.userdb import User
from applications.models.blogdb import Blog
from datetime import datetime, timedelta
# from flask import render_template
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# @celery.task(name="mail.daily_reminder")

def format_message(template_file, user):
        with open (template_file) as file_:
            template = Template(file_.read())
            message = template.render(data=user)
            return message

    

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, 'html'))

    s = smtplib.SMTP(host = SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

# @app.route('/')
@celery.task(name="send_mail")
def mail():
    # get all the users
    users = User.query.all()
    # new_users = []
    for user in users:
        # get all the blogs for the user
        blogs = Blog.query.filter_by(blogUserId=user.userId).all()
        # check if any blog is created in last 24 hours
        # filter the blogs created in today
        blogs_created_today = list(filter(lambda x: x.blogCreation.date() == datetime.now().date(), blogs))
        if blogs_created_today:
            
            
            email = user.userUsername + "@bloglite.com"
            # count = len(blogs_created_today)
            name = user.userName
            user = {"name": name, "msg": "You have posted blog(s) today."}
            message = format_message("applications/mail/templates/mail_daily.html", user)
            send_email(email, subject="Today's Blog Summary", message=message)

        else:
            email = user.userUsername + "@bloglite.com"
            name = user.userName
            user = {"name": name, "msg": "You have not posted any blog today."}
            message = format_message("applications/mail/templates/mail_daily.html", user)
            # email = user.userUsername + "@bloglite.com"
            send_email(email, subject="Today's Blog Summary", message=message)

        
    return "ok"



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(
        hour=20, minute=0, day_of_week="*"), mail.s(), name="send_mail")
#     # test mail in every 10 seconds
    # sender.add_periodic_task(60.0, mail.s(), name="send_mail")  


# query the user and check if you have any new blog in last 24 hours
# if yes, send email to the user saying new blog in last 24 hours
# if no, send email to the user saying no new blog in last 24 hours
