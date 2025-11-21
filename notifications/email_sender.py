# =============================================================================
# notifications/email_sender.py - Email notification system
# =============================================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from datetime import datetime
from config.settings import EMAIL_CONFIG
import logging

class EmailSender:
    """Handle email notifications."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = EMAIL_CONFIG
    
    def send_daily_report(self, data: pd.DataFrame):
        """Send daily report email with filtered data."""
        try:
            # Create email content
            subject = self.config['subject_template'].format(
                date=datetime.now().strftime('%H:%M - %d/%m/%Y')
            )
            
            # Generate HTML table from DataFrame
            html_table = data.to_html(index=False, escape=False, classes='table table-striped')
            
            body = f"""
            <html>
            <head>
                <style>
                    .table {{ border-collapse: collapse; width: 100%; }}
                    .table th, .table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    .table th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h2>Reporte Actualizado Contrataciones Menores</h2>
                <p>{len(data)} contrataciones menores relevantes encontradas el {datetime.now().strftime('%d-%m-%Y')} a las {datetime.now().strftime('%H:%M')}:</p>
                {html_table}
            </body>
            </html>
            """
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config['sender_email']
            msg['To'] = self.config['recipient_email']
            
            # Attach HTML content
            html_message = MIMEText(body, 'html')
            msg.attach(html_message)
            
            # Send email
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['sender_email'], self.config['sender_password'])
                server.send_message(msg)
            
            self.logger.info(f"Daily report sent successfully to {self.config['recipient_email']}")
            
        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
            raise