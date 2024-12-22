from email.message import EmailMessage
from pydantic import EmailStr

from src.config import settings



###################################### 88 probels ######################################
########################################################################################

# def verification_link_template(verification_link: str, email_to: EmailStr,):
#     email = EmailMessage()
#     email["Subject"] = "Emailni tasdiqlash"
#     email["From"] = settings.SMTP_USER
#     email["To"] = email_to

#     email.set_content(
#         html = f"""
#                     <html>
#                     <body>
#                         <p>Assalomu aleykum,<br>
#                         Elektron pochtangizni tasdiqlash uchun quyidagi havolani bosing:<br>
#                         <a href="{verification_link}">Elektron pochtani tasdiqlang.</a>
#                         Havolaning yaroqlilik muddati 5 daqiqa.
#                         </p>
#                     </body>
#                     </html>
#                 """,
#                 subtype="html"
#     )
#     return email


def verification_password_template(generate_pass: str, email_to: EmailStr):
    """
    Create verification password email
    
    :param generate_pass: Verification password
    :param email_to: User email
    :return: EmailMessage
    """
    email = EmailMessage()
    # Настройка письма
    email["Subject"] = "Sizning vaqtinchalik tasdiqlash parolingiz"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    # HTML-сообщение
    email.set_content(
        f"""
            <html>
                <body>
                    <p>Assalomu aleykum,<br><br>
                    Sizning vaqtinchalik login parolingiz:<br>
                    <strong>{generate_pass}</strong><br><br>
                    Parolning yaroqlilik muddati 5 daqiqa.
                    </p>
                </body>
            </html>
        """,
        subtype="html"
    )
    return email

