from django.conf import settings
from django.core.mail import EmailMessage
import random
import hashlib
from django.core.cache import cache


# Helper function to generate the base email template
def get_base_email_template(body_content):
    """
    Returns the full HTML structure for the email.
    It includes a <style> block where Bootstrap-like CSS is defined.
    This CSS will be inlined by css_inline.
    """
    template = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Email Notification</title>
        <style>
          /*
          These are the core CSS rules that mimic Bootstrap 5's default styling
          for the classes used in the email body.
          css_inline will take these rules and apply them directly to the HTML tags.
          */
          body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            background-color: #f8f9fa; /* bg-light */
            margin: 0;
            padding: 0;
            line-height: 1.5;
            color: #212529; /* text-dark */
          }}
          .container {{
            max-width: 600px;
            margin: 30px auto; /* mx-auto my-3 */
            padding: 1.5rem; /* p-4 */
            background-color: #ffffff; /* bg-white */
            border: 1px solid #dee2e6; /* border */
            border-radius: .375rem; /* rounded */
            box-shadow: 0 .125rem .25rem rgba(0,0,0,.075); /* shadow-sm */
            text-align: center; /* text-center */
          }}
          h2.h5 {{
            font-size: 1.5rem; /* h5 */
            font-weight: 500;
            margin-bottom: 1rem; /* mb-3 */
            color: #343a40; /* text-dark */
          }}
          p.lead {{
            font-size: 1.25rem; /* lead */
            margin-bottom: 1rem;
            color: #495057; /* text-secondary */
          }}
          p.text-body {{
            font-size: 1rem;
            margin-bottom: 1rem;
            color: #212529; /* text-body */
          }}
          div.code {{
            display: inline-block; /* d-inline-block */
            padding: .75rem 1.5rem; /* p-3 */
            margin-top: 1rem;
            margin-bottom: 1rem; /* my-4 */
            border-radius: .375rem; /* rounded */
            font-family: monospace; /* font-monospace */
            font-weight: 700; /* fw-bold */
            color: #007bff; /* text-primary */
            background-color: #eaf6ff; /* bg-info-subtle */
            border: 1px solid #0dcaf0; /* border border-info */
            border-style: dashed; /* border-dashed */
            font-size: large;
          }}
          p.small {{
            font-size: .875em; /* small */
            margin-top: 1rem; /* mt-3 */
          }}
          p.text-danger {{
            color: #dc3545; /* text-danger */
          }}
          p.fw-bold {{
            font-weight: 700;
          }}
          div.footer {{
            margin-top: 1.5rem; /* mt-4 */
            padding-top: 1rem; /* pt-3 */
            border-top: 1px solid #e9ecef; /* border-top */
            color: #6c757d; /* text-muted */
            font-size: .875em; /* small */
          }}
          p.mb-0 {{
            margin-bottom: 0;
          }}
          .invoice-container {{
            max-width: 600px;
            margin: 40px auto;
            background-color: #ffffff;
            padding: 30px;
            border: 1px solid #e5e5e5;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
          }}
          h2 {{
            color: #333333;
            margin-bottom: 20px;
          }}
          table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
          }}
          th, td {{
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #e5e5e5;
          }}
          th {{
            background-color: #f2f2f2;
            color: #555;
          }}
          .footer {{
            margin-top: 30px;
            font-size: 14px;
            color: #888888;
            text-align: center;
          }}
        </style>
      </head>
      <body>
        {body_content}
      </body>
    </html>
    """
    return template

# Helper Functions
def sent_email_to_user(recipient_email, subject,  message):
    email = EmailMessage(
        subject=subject,
        body=get_base_email_template(message),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )
    email.content_subtype = "html"
    email.send()



# Helper Functions
def sent_otp(email, purpose, subject="Your OTP Code for Verification"):
    code = f"{random.randint(1000, 9999)}"
    code_hash = hashlib.sha256(code.encode()).hexdigest()
    cache.set(f"email_verify_{email}", code_hash, timeout=600)  # 10 minutes
    verification_url = f"{settings.FRONTEND_HOSTNAME}/user/{purpose}/verify?email={email}&code={code}"
    body = f"""
        <div style="max-width: 480px; margin: auto; font-family: Arial, sans-serif; background: #ffffff; border: 1px solid #e5e5e5; border-radius: 8px; padding: 24px; text-align: center;">
          
          <!-- Title -->
          <h2 style="color: #333333; font-size: 20px; margin-bottom: 16px;">Verify Your Email</h2>
          
          <!-- Verification Code -->
          <p style="color: #555555; font-size: 15px; margin-bottom: 8px;">Use the code below to verify your email:</p>
          <div style="font-size: 24px; font-weight: bold; color: #2d6cdf; letter-spacing: 4px; margin: 16px 0;">
            {code}
          </div>
        
          <!-- Direct Link -->
          <p style="color: #555555; font-size: 15px; margin: 16px 0;">Or verify directly using this link:</p>
          <a href="{verification_url}" target="_blank" style="display: inline-block; padding: 12px 20px; background: #2d6cdf; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 15px; font-weight: 600;">
            Verify Email
          </a>
        
          <!-- Footer Note -->
          <p style="color: #999999; font-size: 13px; margin-top: 24px;">This code will expire in 10 minutes.</p>
          <p style="color: #cc0000; font-size: 13px; font-weight: bold; margin-top: 8px;">Do not share this code with anyone.</p>
          
          <hr style="margin: 24px 0; border: none; border-top: 1px solid #eee;">
          <p style="color: #888888; font-size: 13px; margin: 0;">Thank you for using our service.</p>
        </div>

    """.strip()

    # Send email with the code
    sent_email_to_user(
        recipient_email=email,
        subject=subject,
        message=body,
    )



def verify_otp(email, code):
    # Retrieve the hashed code from cache
    code_hash = cache.get(f"email_verify_{email}")
    if not code_hash:
        return False

    # Hash the input code and compare
    input_code_hash = hashlib.sha256(code.encode()).hexdigest()
    if input_code_hash != code_hash:
        return False

    # If valid, delete the cache entry
    cache.delete(f"email_verify_{email}")
    return True