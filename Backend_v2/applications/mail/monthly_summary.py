from . import *
from jinja2 import Template
from datetime import  timedelta, date
from flask import render_template
from applications.models.userdb import User
from applications.models.blogdb import Blog
from applications.models.commentsdb import Comments

from applications.jobs import celery
from celery.schedules import crontab # crontab is a class

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from weasyprint import HTML
import uuid

# Genreating the report in pdf
def format_report(report, data={}):
    with open(report) as file_:
        template = Template(file_.read())
        return template.render(data = data)

def create_pdf_report(data):
    message = format_report("applications/mail/templates/report.html", data=data)
    html = HTML(string = message)
    file_name = str(uuid.uuid4()) + ".pdf"
    file_path = "applications/static/pdfReports/" + file_name
    print(file_path)
    html.write_pdf(target=file_path)
    return file_name


def format_message(template_file, user):
        with open (template_file) as file_:
            template = Template(file_.read())
            message = template.render(data=user)
            return message

    

def send_email(to_address, subject, message, content='text', attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    if content =="html":
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))
    
    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_file}",
        )
        msg.attach(part)

    s = smtplib.SMTP(host = SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True


@celery.task(name="monthly_mail")
def monthly_mail():
    # get all the users
    users = User.query.all()
    # new_users = []
    for user in users:
        blogs = Blog.query.filter_by(blogUserId=user.userId).all()

        user_data = {
            "name": user.userName,
            "number_of_follower":user.userNoFollowers,
            "number_of_followings":user.userNoFollowing,
            "blog_details": []
            }

        blogs_created_last_month = list(
                filter(lambda x: x.blogCreation.date() >= (date.today() - timedelta(days=30)),
                    blogs)
            )

        if blogs_created_last_month:
            blogs_created_last_month.reverse()

            email = user.userUsername + "@bloglite.com"
            name = user.userName
            user_ = {
                "name": name,
                "msg": "You have posted {} blog(s) in the previous month.".format(len(blogs_created_last_month))
                }

            for blog in blogs_created_last_month:
                comment_list = Comments.query.filter_by(commentBlogId=blog.blogId).all()

                if comment_list:
                    user_data["blog_details"].append({"blogTitle": blog.blogTitle,
                                                       "blogCreation": blog.blogCreation.strftime("%b %d %Y %H:%M:%S") ,"number_of_comments": len(comment_list),
                                                       "likes": blog.likes,
                                                       "dislikes": blog.dislikes})
                    # print(blog.likes, blog.dislikes)

                else:
                    user_data["blog_details"].append({"blogTitle": blog.blogTitle,
                                                      "blogCreation": blog.blogCreation.strftime("%b %d %Y %H:%M:%S"), "number_of_comments": 0,
                                                      "likes": blog.likes,
                                                      "dislikes": blog.dislikes})

            if(user.monthlyReport == 'pdf'):
                path = create_pdf_report(user_data)
                message = format_message("applications/mail/templates/monthly_report.html", user_)
                send_email(email,
                           subject="Monthly Blog Summary",
                           message=message,
                           content="html",
                           attachment_file= "applications/static/pdfReports/{}".format(path)
                        )
                
            else:
                message = format_message("applications/mail/templates/report.html", user_data)
                send_email(email,
                           subject="Monthly Blog Summary",
                           message=message,
                           content="plain"
                           )
            

        else:
            email = user.userUsername + "@bloglite.com"
            name = user.userName
            user_ = {"name": name, "msg": "You have not posted any blog in last month."}

            if (user.monthlyReport == 'pdf'):
                path = create_pdf_report(user_data)
                message = format_message("applications/mail/templates/monthly_report.html", user_)
                send_email(email,
                           subject="Monthly Blog Summary",
                           message=message,
                           content="html", 
                           attachment_file= "applications/static/pdfReports/{}".format(path)
                           )
            else:
                message = format_message("applications/mail/templates/report.html", user_data)
                send_email(email,
                           subject="Monthly Blog Summary",
                           message=message,
                           content="plain")

        
    return "ok"



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(day_of_month=1, hour=20, minute=0), monthly_mail.s(), name="monthly_mail")
    # test mail in every 10 seconds
    # sender.add_periodic_task(50.0, monthly_mail.s(), name="monthly_mail")  


# query the user and check if you have any new blog in last 24 hours
# if yes, send email to the user saying new blog in last 24 hours
# if no, send email to the user saying no new blog in last 24 hours