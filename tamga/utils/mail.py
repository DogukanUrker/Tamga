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
                * {{
                    margin: 0;
                    padding: 0;
                    boxSizing: border-box;
                }}

                body {{
                    fontFamily: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    lineHeight: 1.6;
                    color: #1a1a1a;
                    backgroundColor: #f5f5f5;
                    padding: 20px;
                }}

                .emailContainer {{
                    maxWidth: 600px;
                    margin: 0 auto;
                    backgroundColor: #ffffff;
                    borderRadius: 16px;
                    boxShadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                    overflow: hidden;
                }}

                .headerSection {{
                    padding: 32px;
                    textAlign: center;
                    backgroundColor: #ffffff;
                    borderBottom: 1px solid #eef0f3;
                }}

                .headerSection h1 {{
                    fontSize: 28px;
                    fontWeight: 700;
                    color: #1a1a1a;
                    margin: 0;
                    letterSpacing: -0.5px;
                }}

                .contentSection {{
                    padding: 32px;
                    backgroundColor: #ffffff;
                }}

                .logLevelBadge {{
                    display: inline-block;
                    padding: 6px 12px;
                    backgroundColor: #f3f4f6;
                    borderRadius: 8px;
                    fontSize: 14px;
                    fontWeight: 500;
                    color: #4b5563;
                    marginBottom: 24px;
                }}

                .messageBox {{
                    padding: 24px;
                    backgroundColor: #f9fafb;
                    borderRadius: 12px;
                    fontSize: 16px;
                    lineHeight: 1.6;
                    color: #1f2937;
                    marginBottom: 24px;
                }}

                .timestampSection {{
                    fontSize: 14px;
                    color: #6b7280;
                    display: flex;
                    alignItems: center;
                    gap: 8px;
                }}

                .timestampSection::before {{
                    content: "";
                    display: inline-block;
                    width: 6px;
                    height: 6px;
                    backgroundColor: #d1d5db;
                    borderRadius: 50%;
                }}

                .footerSection {{
                    padding: 24px 32px;
                    borderTop: 1px solid #eef0f3;
                    textAlign: center;
                }}

                .footerSection p {{
                    fontSize: 14px;
                    color: #6b7280;
                    margin: 0;
                }}

                @media (max-width: 640px) {{
                    body {{
                        padding: 16px;
                    }}

                    .headerSection,
                    .contentSection,
                    .footerSection {{
                        padding: 24px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="emailContainer">
                <div class="headerSection">
                    <h1>Tamga Logger</h1>
                </div>
                <div class="contentSection">
                    <div class="logLevelBadge">
                        {logLevel}
                    </div>
                    <div class="messageBox">
                        {messageContent}
                    </div>
                    <div class="timestampSection">
                        {currentTimestamp}
                    </div>
                </div>
                <div class="footerSection">
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
