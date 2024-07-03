import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

def send_email_with_sendinblue(subject, sender_name, sender_email, recipients, html_content):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    send_email = sib_api_v3_sdk.SendSmtpEmail(
        sender={"name": sender_name, "email": sender_email},
        to=recipients,
        subject=subject,
        html_content=html_content,
    )

    try:
        api_response = api_instance.send_transac_email(send_email)
        return api_response
    except ApiException as e:
        print(f"Exception when calling TransactionalEmailsApi->send_transac_email: {e}")
        return False
