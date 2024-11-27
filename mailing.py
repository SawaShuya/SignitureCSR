import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import ssm_client

from_address = "no-reply@devdevnetwork.com"
charset = "UTF-8"
smtp_endpoint= "email-smtp.ap-northeast-1.amazonaws.com"

smtp_user = ssm_client.get_params('/lambda/SubmitCSRRequest/SMTP_USER')
smtp_user_password = ssm_client.get_params('/lambda/SubmitCSRRequest/SMTP_USER_PASSWORD')

def send(id, to_address, attachment_path):
    print(f"Send Mail to {to_address}")
    subject = "Certification was Created Sccessfully !"
    body = f"Your application was Completed ! ( ID : {id} ) \nPlease Check aattached file."
    smtpobj = smtplib.SMTP(smtp_endpoint, 587)
    smtpobj.ehlo() 
    smtpobj.starttls()
    smtpobj.login(smtp_user, smtp_user_password)
    
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = to_address

    with open(attachment_path, 'br') as attachment:
        part = MIMEBase('application', 'zip')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split("/")[-1]}')
        msg.attach(part)

    smtpobj.send_message(msg)

    smtpobj.quit()