class EmailAlertSender:
    def __init__(self, smtp_client, from_addr: str, to_addr: str):
        self.smtp_client = smtp_client
        self.from_addr = from_addr
        self.to_addr = to_addr

    def send(self, subject: str, body: str) -> None:
        message = f"Subject: {subject}\n\n{body}"
        self.smtp_client.sendmail(self.from_addr, self.to_addr, message)
