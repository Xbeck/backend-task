import smtplib
from pydantic import EmailStr

from src.tasks.celery_ import celery_app
from src.config import settings
from src.tasks.email_templates import verification_password_template




###################################### 88 probels ######################################
########################################################################################

@celery_app.task
def send_verification_password(generate_pass: str, email_to: EmailStr):
    """
    Send verification password to User email

    :param generate_pass: Verification password
    :param email_to: User email
    """
    msg_content = verification_password_template(generate_pass=generate_pass,
                                   email_to=email_to)
    # send message
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
    return True


# @celery_app.task
# def send_verification_link(verification_link: str, email_to: EmailStr):
#     """Send verification link to User email"""
#     msg_content = verification_link_template(verification_link=verification_link,
#                                    email_to=email_to)
#     # send message
#     with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
#         server.login(settings.SMTP_USER, settings.SMTP_PASS)
#         server.send_message(msg_content)
#     return True

