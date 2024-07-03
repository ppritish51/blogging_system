# email_utils.py
from django.template.loader import render_to_string
from .providers.sendinblue import send_email_with_sendinblue

def render_email_template(template_name, context):
    return render_to_string(f'{template_name}.html', context)

def send_forgot_password_email(name, email, reset_password_link):
    subject = "SlowestCheetah: Reset Password Link"
    sender_name = "Slowest Cheetah"
    sender_email = "help@slowestcheetah.com"
    recipients = [{"email": email, "name": name}]
    context = {"name": name, "reset_password_link": reset_password_link}
    html_content = render_email_template('forgot_password', context)

    return send_email_with_sendinblue(subject, sender_name, sender_email, recipients, html_content)
