import sendgrid
import os
from sendgrid.helpers.mail import *
import datetime
from src.apis.serviceReminder.models import ServiceReminder
from src.apis.serviceReminder.api.serializers import ServiceReminderEmail

def service_reminder(self):
    now = datetime.datetime.now()
    reminder = ServiceReminder.objects.filter(reminderDate=now)
    serializer = ServiceReminderEmail(reminder, many=True)
    emails = [i['cusID']['cusemail'] for i in serializer.data]

    # emails = ["vaghasiya665@gmail.com", "shyam047.rejoice@gmail.com"] 

    for dta in emails:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("dev043.rejoice@gmail.com")
        to_email = Email(dta)
        subject = "For Your vehicles service reminder."
        content = Content("text/plain", "Dear Customer, your vehicles service date is today, Please contact your realated workshop.")
        mail = Mail(from_email, subject, to_email, content)

        
        response = sg.client.mail.send.post(request_body=mail.get())


service_reminder()











