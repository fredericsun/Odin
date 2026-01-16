from app.services.alerting import EmailAlertSender


class FakeSMTP:
    def __init__(self):
        self.sent = False

    def sendmail(self, *_):
        self.sent = True


def test_send_email_alert():
    smtp = FakeSMTP()
    sender = EmailAlertSender(smtp_client=smtp, from_addr="a@b.com", to_addr="c@d.com")
    sender.send("Subject", "Body")
    assert smtp.sent is True
