import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class Mail:
    def __init__(
        self,
        serverAddress: str,
        portNumber: int,
        userName: str,
        userPassword: str,
        senderEmail: str,
        receiverEmails: list,
    ):
        self.serverAddress = serverAddress
        self.portNumber = portNumber
        self.userName = userName
        self.userPassword = userPassword
        self.senderEmail = senderEmail
        self.receiverEmails = receiverEmails

    def getHtmlTemplate(self, messageContent: str, logLevel: str = "INFO") -> str:
        currentTimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tamga Logger Alert</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                    border-bottom: 1px solid #eee;
                }}
                .header h1 {{
                    font-size: 24px;
                    color: #333;
                }}
                .content {{
                    padding: 20px 0;
                }}
                .log-level {{
                    display: inline-block;
                    padding: 5px 10px;
                    background-color: #e0e0e0;
                    border-radius: 4px;
                    font-size: 14px;
                    color: #555;
                    margin-bottom: 20px;
                }}
                .message {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #333;
                    margin-bottom: 20px;
                }}
                .timestamp {{
                    font-size: 12px;
                    color: #999;
                }}
                .footer {{
                    text-align: center;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    font-size: 12px;
                    color: #999;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Tamga Logger</h1>
                </div>
                <div class="content">
                    <div class="log-level">{logLevel}</div>
                    <div class="message">{messageContent}</div>
                    <div class="timestamp">{currentTimestamp}</div>
                </div>
                <div class="footer">
                    <p>This is an automated message from Tamga Logger</p>
                </div>
            </div>
        </body>
        </html>
        """

    def sendMail(
        self,
        emailSubject: str,
        messageContent: str,
        logLevel: str = "INFO",
        enableHtml: bool = True,
    ):
        try:
            emailMessage = MIMEMultipart("alternative")
            emailMessage["Subject"] = emailSubject
            emailMessage["From"] = self.senderEmail
            emailMessage["To"] = ", ".join(self.receiverEmails)

            textContent = MIMEText(messageContent, "plain")
            htmlContent = MIMEText(
                self.getHtmlTemplate(messageContent, logLevel), "html"
            )

            emailMessage.attach(textContent)
            if enableHtml:
                emailMessage.attach(htmlContent)

            mailServer = smtplib.SMTP(self.serverAddress, self.portNumber)
            mailServer.starttls()
            mailServer.login(self.userName, self.userPassword)
            mailServer.send_message(emailMessage)
            mailServer.quit()
            return True

        except Exception as errorDetails:
            print(f"Error: {errorDetails}")
            return False
