import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..constants import COLOR_PALLETTE, LOG_LEVELS


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

        colorName = LOG_LEVELS.get(logLevel.upper(), "blue")
        rgb = COLOR_PALLETTE.get(colorName, (0, 0, 0))
        logColor = f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tamga Logger Alert</title>
            <style>
                :root {{
                    --card-bg: #111827;
                    --surface-bg: #1F2937;
                    --text-primary: #F9FAFB;
                    --text-secondary: #D1D5DB;
                    --border-color: rgba(255, 255, 255, 0.1);
                }}

                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}

                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: var(--text-primary);
                }}

                .wrapper {{
                    width: 100%;
                    max-width: 650px;
                    background: var(--card-bg);
                    border-radius: 16px;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
                    overflow: hidden;
                    border: 1px solid var(--border-color);
                }}

                .header {{
                    padding: 32px;
                    position: relative;
                    background: var(--surface-bg);
                    border-bottom: 1px solid var(--border-color);
                }}

                .header h1 {{
                    text-align: center;
                    font-size: 24px;
                    font-weight: 600;
                    letter-spacing: -0.5px;
                    background: linear-gradient(to right, var(--text-primary), var(--text-secondary));
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }}

                .content {{
                    padding: 32px;
                }}

                .status-container {{
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    margin-bottom: 24px;
                }}

                .log-level {{
                    display: inline-flex;
                    align-items: center;
                    padding: 6px 12px;
                    background-color: {logColor}22;
                    color: {logColor};
                    border: 1px solid {logColor}44;
                    border-radius: 8px;
                    font-size: 13px;
                    font-weight: 500;
                    letter-spacing: 0.3px;
                    text-transform: uppercase;
                }}

                .log-level::before {{
                    content: '';
                    display: inline-block;
                    width: 8px;
                    height: 8px;
                    background-color: {logColor};
                    border-radius: 50%;
                    margin-right: 8px;
                }}

                .message {{
                    background: var(--surface-bg);
                    padding: 24px;
                    border-radius: 12px;
                    font-size: 15px;
                    line-height: 1.6;
                    color: var(--text-secondary);
                    border: 1px solid var(--border-color);
                }}

                .message pre {{
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}

                .footer {{
                    padding: 20px 32px;
                    background: var(--surface-bg);
                    border-top: 1px solid var(--border-color);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }}

                .timestamp {{
                    font-size: 13px;
                    color: var(--text-secondary);
                    display: flex;
                    align-items: center;
                    gap: 6px;
                }}

                .timestamp svg {{
                    width: 14px;
                    height: 14px;
                    opacity: 0.7;
                }}

                @media (max-width: 600px) {{
                    body {{
                        padding: 16px;
                    }}

                    .wrapper {{
                        border-radius: 12px;
                    }}

                    .header, .content {{
                        padding: 24px;
                    }}

                    .message {{
                        padding: 20px;
                        font-size: 14px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="wrapper">
                <div class="header">
                    <h1>Tamga Logger Alert</h1>
                </div>
                <div class="content">
                    <div class="status-container">
                        <div class="log-level">{logLevel.upper()}</div>
                    </div>
                    <div class="message">
                        <pre>{messageContent}</pre>
                    </div>
                </div>
                <div class="footer">
                    <div class="timestamp">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M12 6v6l4 2"/>
                        </svg>
                        <span>{currentTimestamp}</span>
                    </div>
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
