from urllib.parse import urlencode

def generate_invitation_email(friend_name, group_name, description, start_date, invite_link):
    # Generate accept and decline links with URL parameters
    accept_link = f"{invite_link}?{urlencode({'status': 'Accept'})}"
    decline_link = f"{invite_link}?{urlencode({'status': 'Decline'})}"
    
    email_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f9f9f9;
                color: #333333;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #2563eb;
                color: #ffffff;
                text-align: center;
                padding: 20px;
                font-size: 24px;
            }}
            .content {{
                padding: 20px;
                text-align: center;
            }}
            .content p {{
                font-size: 16px;
                line-height: 1.5;
                margin-bottom: 20px;
            }}
            .cta-button {{
                display: inline-block;
                padding: 12px 24px;
                color: #ffffff;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
            }}
            .accept {{
                background-color: #4CAF50;
            }}
            .decline {{
                background-color: #f87171;
            }}
            .cta-button:hover {{
                opacity: 0.9;
            }}
            .footer {{
                background-color: #f1f1f1;
                padding: 10px;
                text-align: center;
                font-size: 12px;
                color: #666666;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                You've Been Invited to Join a Group!
            </div>
            <div class="content">
                <p>Hi there,</p>
                <p><strong>{friend_name}</strong> has invited you to join their group, <strong>{group_name}</strong>.</p>
                <p>This group is about <strong>{description}</strong>, and it starts on <strong>{start_date}</strong>.</p>
                <a href="{accept_link}" class="cta-button accept">Accept Invitation</a>
                <a href="{decline_link}" class="cta-button decline">Decline Invitation</a>
            </div>
            <div class="footer">
                If you have any questions, feel free to contact us at <a href="mailto:support@yourapp.com">support@yourapp.com</a>.
            </div>
        </div>
    </body>
    </html>
    """
    return email_template
