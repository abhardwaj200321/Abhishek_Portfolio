from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact

def home(request):
    success = False
    error = None

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # 🔍 VALIDATION
        if not name or not email or not subject or not message:
            error = "All fields are required!"

        elif "@" not in email:
            error = "Enter a valid email address!"

        elif len(message) < 10:
            error = "Message must be at least 10 characters!"

        else:
            # ✅ Save to DB
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # ✅ Create formatted email message
            full_message = f"""
            New Contact Form Submission:

            Name: {name}
            Email: {email}
            Subject: {subject}

            Message:
            {message}
            """

            # ✅ Send Email
            try:
                send_mail(
                    subject,
                    full_message,  # 👈 use this instead of 'message'
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                success = True
            except Exception as e:
                error = "Email failed to send"

    return render(request, "index.html", {
        "success": success,
        "error": error
    })