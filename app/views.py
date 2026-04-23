from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

from .models import News

def news(request):
    return render(request, 'app/news.html')

def stock(request):
    return render(request, 'app/stock.html')
def press(request):
    return render(request, 'app/press.html')
def faq(request):
    return render(request, 'app/faq.html')
# def join(request):
#     return render(request, 'app/join.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import VolunteerForm


def join(request):

    if request.method == "POST":
        form = VolunteerForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "✅ Thank you for registering as a volunteer!")
            return redirect("join")

    else:
        form = VolunteerForm()

    return render(request, "app/join.html", {"form": form})
def services(request):
    return render(request, 'app/services.html')
def stock(request):
    return render(request, 'app/stock.html')

def schemes(request):
    return render(request, 'app/schemes.html')

def privacy_policy(request):
    return render(request, 'app/privacy_policy.html')

def disclaimer(request):
    return render(request, 'app/disclaimer.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# def contact(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         message = request.POST.get("message")

#         subject = f"New Contact Form Submission from {name}"
#         full_message = f"Sender: {name}\nEmail: {email}\n\nMessage:\n{message}"

#         send_mail(
#             subject,
#             full_message,
#             "amp2052@gmail.com",        # sender
#             ["amp2052@gmail.com"],      # recipient(s) -> must be a list
#         )

#         messages.success(request, "Your message has been sent successfully!")
#         return redirect('contact')

#     return render(request, "app/contact.html")
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import ContactMessage

def contact(request):
    if request.method == "POST":

        # Get data manually
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        grievance_type = request.POST.get("grievance_type")
        message = request.POST.get("message")

        # Save to DB
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            grievance_type=grievance_type,
            message=message
        )

        # Email content
        full_message = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Subject: {subject}\n"
            f"Grievance: {grievance_type}\n\n"
            f"Message:\n{message}"
        )

        # Send email
        send_mail(
            f"New Contact: {subject}",
            full_message,
            "amp2052@gmail.com",
            ["amp2052@gmail.com"],
            fail_silently=False,
        )

        messages.success(request, "✅ Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "app/contact.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import ContactForm
from .models import ContactMessage
def admin_login(request):
    next_url = request.GET.get('next') or 'contact_submissions'
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "✅ Logged in successfully!")
            return redirect(next_url)
        else:
            messages.error(request, "❌ Invalid credentials or not authorized.")
    return render(request, "app/admin_login.html")

# Admin Logout
def admin_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("admin_login")

# Admin-only Contact Submissions Page
@login_required
@user_passes_test(lambda u: u.is_staff)
def contact_submissions(request):
    # Contact Messages
    messages_list = ContactMessage.objects.all().order_by("-created_at")
    total_count = messages_list.count()
    unread_count = messages_list.filter(is_read=False).count()

    # Team Members
    team_members = TeamMember.objects.all().order_by("-created_at")
    team_total_count = team_members.count()

    return render(
        request,
        "app/contact_submissions.html",
        {
            "messages": messages_list,
            "total_count": total_count,
            "unread_count": unread_count,
            "team_members": team_members,
            "team_total_count": team_total_count
        }
    )

# Delete Contact Message
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_contact_message(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    messages.success(request, "✅ Contact message deleted successfully!")
    return redirect("contact_submissions")
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import ContactMessage

@login_required
@user_passes_test(lambda u: u.is_staff)
def mark_as_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True
    msg.save()
    messages.success(request, f"✅ Message from {msg.name} marked as read!")
    return redirect("contact_submissions")
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def admin_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("admin_login")
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .models import ContactMessage

@login_required
@user_passes_test(lambda u: u.is_staff)
def download_contact_pdf(request):
    # Create the HttpResponse object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contact_submissions.pdf"'

    # Create PDF
    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=3*cm, bottomMargin=2*cm)
    elements = []

    styles = getSampleStyleSheet()
    styleH = styles['Heading1']
    styleN = styles['Normal']

    # Header
    elements.append(Paragraph("📩 Contact Submissions", styleH))
    elements.append(Spacer(1, 12))

    # Fetch all messages
    messages_list = ContactMessage.objects.all().order_by('-created_at')

    # Prepare data for table
    data = [['#', 'Name', 'Email', 'Mobile', 'Address', 'Message', 'Date']]
    for idx, msg in enumerate(messages_list, start=1):
        data.append([
            idx,
            msg.name,
            msg.email,
            msg.mobile_no,
            msg.address,
            msg.message,
            msg.created_at.strftime("%d-%b-%Y %H:%M")
        ])

    # Create Table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    elements.append(table)

    # Footer: Page numbers
    def add_page_number(canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(A4[0] - 2*cm, 1*cm, text)

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import TeamMember  # your model

def join(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        message_text = request.POST.get("message")

        if name and email and mobile:
            # Save to database
            team_member = TeamMember.objects.create(
                name=name,
                email=email,
                address=address,
                mobile_no=mobile,
                message=message_text
            )

            # Prepare email content
            subject = "Thank You for Joining Team Sanjay Rathod"
            full_message = (
                f"Hello {name},\n\n"
                "Thank you for joining Team Sanjay Rathod.\n"
                "We will contact you soon.\n\n"
                "Your Details:\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Mobile: {mobile}\n"
                f"Address: {address}\n"
                f"Message: {message_text}\n\n"
                "Best Regards,\nTeam Sanjay Rathod"
            )

            # Send confirmation email to user
            send_mail(
                subject,
                full_message,
                "amp2052@gmail.com",  # sender
                [email,"amp2052@gmail.com"],              # recipient
                fail_silently=False,
            )

            alert = "✅ Thank you for joining! A confirmation email has been sent to you."
            return render(request, "app/join.html", {"alert": alert})
        else:
            alert = "❌ Please fill in all required fields."

    return render(request, "app/join.html")

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import TeamMember

# View all Team Members
@login_required
@user_passes_test(lambda u: u.is_staff)
def team_members_list(request):
    members = TeamMember.objects.all().order_by('-created_at')
    total_count = members.count()
    return render(request, "app/team_members_list.html", {
        "members": members,
        "total_count": total_count,
    })

# Delete Team Member
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.delete()
    messages.success(request, "✅ Team member deleted successfully!")
    return redirect("contact_submissions")

@login_required
@user_passes_test(lambda u: u.is_staff)
def mark_team_member_reviewed(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.is_reviewed = True
    member.save()
    messages.success(request, f"✅ Team member {member.name} marked as reviewed!")
    return redirect("contact_submissions")

@login_required
@user_passes_test(lambda u: u.is_staff)
def mark_team_member_unreviewed(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.is_reviewed = False
    member.save()
    messages.success(request, f"⚠️ Team member {member.name} marked as unreviewed!")
    return redirect("contact_submissions")

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import TeamMember

@login_required
@user_passes_test(lambda u: u.is_staff)
def download_team_members_pdf(request):
    # Create the HttpResponse object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="team_members.pdf"'

    # Create PDF document
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=2*cm
    )

    elements = []
    styles = getSampleStyleSheet()
    styleH = styles['Heading1']
    styleN = styles['Normal']

    # Header
    elements.append(Paragraph("👥 Team Members List", styleH))
    elements.append(Spacer(1, 12))

    # Fetch all team members
    members = TeamMember.objects.all().order_by('-created_at')

    # Prepare table data
    data = [['#', 'Name', 'Email', 'Mobile', 'Address', 'Message', 'Date Joined', 'Status']]
    for idx, member in enumerate(members, start=1):
        status = "Reviewed" if member.is_reviewed else "Pending"
        data.append([
            idx,
            member.name,
            member.email,
            member.mobile_no,
            member.address,
            member.message,
            member.created_at.strftime("%d-%b-%Y %H:%M"),
            status
        ])

    # Create Table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))

    elements.append(table)

    # Footer: Page numbers
    def add_page_number(canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(A4[0] - 2*cm, 1*cm, text)

    # Build PDF
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return response

from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings

def chat_with_ai(request):
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"response": "⚠️ Invalid request format"}, status=400)

        user_message = data.get("message")
        headers = {"Authorization": f"Bearer {settings.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}"}

        try:
            response = requests.post(
                "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                headers=headers,
                json={"inputs": user_message},
                timeout=30
            )

            # If HuggingFace returns HTML (not JSON), catch it
            try:
                result = response.json()
            except Exception:
                return JsonResponse({"response": "⚠️ API returned invalid data"}, status=500)

            # Handle HuggingFace response format
            if isinstance(result, list) and "generated_text" in result[0]:
                bot_message = result[0]["generated_text"]
            elif "error" in result:
                bot_message = f"⚠️ API Error: {result['error']}"
            else:
                bot_message = "⚠️ Unexpected API response"

        except requests.exceptions.RequestException as e:
            bot_message = f"⚠️ Request failed: {e}"

        return JsonResponse({"response": bot_message})


# # changes
# from django.shortcuts import render, get_object_or_404
# from .models import News


# def news_list(request):

#     news = News.objects.all().order_by("-date")

#     featured_news = News.objects.filter(featured=True).first()

#     context = {
#         "news": news,
#         "featured_news": featured_news
#     }

#     return render(request, "app/news.html", context)



# def news_detail(request, slug):

#     article = get_object_or_404(News, slug=slug)

#     return render(request, "app/news_detail.html", {"article": article})
from .models import Gallery, News

def gallery_view(request):
    images = Gallery.objects.all().order_by('-created_at')
    return render(request, 'app/gallery.html', {'images': images})








from django.shortcuts import render, redirect
from .models import IssueReport

def public_issues(request):

    if request.method == 'POST':
        try:
            IssueReport.objects.create(
                name=request.POST.get('name'),
                village=request.POST.get('village'),
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),

                main_issue=request.POST.get('main_issue'),
                severity=request.POST.get('severity'),
                duration=request.POST.get('duration'),
                priority=request.POST.get('priority'),
                scheme=request.POST.get('scheme'),
                roads=request.POST.get('roads'),
                water=request.POST.get('water'),
                jobs=request.POST.get('jobs'),

                suggestion=request.POST.get('suggestion'),
            )

            # SUCCESS MESSAGE
            return render(request, 'app/public_issues.html', {
                'success': True
            })

        except Exception as e:
            print("ERROR:", e)
            return render(request, 'app/public_issues.html', {
                'error': "Something went wrong. Please try again."
            })

    return render(request, 'app/public_issues.html')


from django.shortcuts import render
from django.core.paginator import Paginator

def services(request):

    schemes = [

    # ================= HEALTH =================
    {
        "name": "Ayushman Bharat (PM-JAY)",
        "category": "health",
        "benefits": "₹5 lakh free treatment per family",
        "eligibility": "SECC database eligible families",
        "link": "https://pmjay.gov.in"
    },
    {
        "name": "Mahatma Jyotiba Phule Jan Arogya Yojana",
        "category": "health",
        "benefits": "Cashless treatment in Maharashtra hospitals",
        "eligibility": "Residents of Maharashtra",
        "link": "https://www.jeevandayee.gov.in"
    },
    {
        "name": "Pradhan Mantri Suraksha Bima Yojana",
        "category": "health",
        "benefits": "₹2 lakh accident insurance",
        "eligibility": "Age 18–70 with bank account",
        "link": "https://jansuraksha.gov.in"
    },
    {
        "name": "Pradhan Mantri Jeevan Jyoti Bima Yojana",
        "category": "health",
        "benefits": "₹2 lakh life insurance",
        "eligibility": "Age 18–50",
        "link": "https://jansuraksha.gov.in"
    },

    # ================= EDUCATION =================
    {
        "name": "Post Matric Scholarship",
        "category": "education",
        "benefits": "Tuition + maintenance allowance",
        "eligibility": "SC/ST/OBC students",
        "link": "https://mahadbt.maharashtra.gov.in"
    },
    {
        "name": "Rajarshi Shahu Maharaj Scholarship",
        "category": "education",
        "benefits": "₹600/month support",
        "eligibility": "Economically weaker students",
        "link": "https://mahadbt.maharashtra.gov.in"
    },
    {
        "name": "EBC Scholarship",
        "category": "education",
        "benefits": "Fee reimbursement",
        "eligibility": "Income below ₹8 lakh",
        "link": "https://mahadbt.maharashtra.gov.in"
    },
    {
        "name": "Savitribai Phule Scholarship",
        "category": "education",
        "benefits": "Support for girl students",
        "eligibility": "Girls in govt schools",
        "link": "https://mahadbt.maharashtra.gov.in"
    },

    # ================= EMPLOYMENT =================
    {
        "name": "MGNREGA",
        "category": "employment",
        "benefits": "100 days guaranteed work",
        "eligibility": "Rural households",
        "link": "https://nrega.nic.in"
    },
    {
        "name": "PM Kaushal Vikas Yojana",
        "category": "employment",
        "benefits": "Free skill training",
        "eligibility": "Youth 18+",
        "link": "https://pmkvyofficial.org"
    },
    {
        "name": "Chief Minister Employment Generation Programme",
        "category": "employment",
        "benefits": "Loan subsidy",
        "eligibility": "Entrepreneurs",
        "link": "https://mahaonline.gov.in"
    },
    {
        "name": "Stand-Up India",
        "category": "employment",
        "benefits": "Loan for SC/ST/Women",
        "eligibility": "Entrepreneurs",
        "link": "https://standupmitra.in"
    },

    # ================= HOUSING =================
    {
        "name": "PM Awas Yojana (Urban)",
        "category": "housing",
        "benefits": "Home subsidy",
        "eligibility": "Urban poor",
        "link": "https://pmaymis.gov.in"
    },
    {
        "name": "PM Awas Yojana (Gramin)",
        "category": "housing",
        "benefits": "Rural housing support",
        "eligibility": "Rural families",
        "link": "https://pmayg.nic.in"
    },
    {
        "name": "Mhada Housing Scheme",
        "category": "housing",
        "benefits": "Affordable housing",
        "eligibility": "Maharashtra residents",
        "link": "https://mhada.gov.in"
    },

    # ================= AGRICULTURE =================
    {
        "name": "PM Kisan",
        "category": "agriculture",
        "benefits": "₹6000/year",
        "eligibility": "Farmers",
        "link": "https://pmkisan.gov.in"
    },
    {
        "name": "PM Fasal Bima Yojana",
        "category": "agriculture",
        "benefits": "Crop insurance",
        "eligibility": "Farmers",
        "link": "https://pmfby.gov.in"
    },
    {
        "name": "Kisan Credit Card",
        "category": "agriculture",
        "benefits": "Low-interest loans",
        "eligibility": "Farmers",
        "link": "https://pmkisan.gov.in"
    },

    # ================= WOMEN =================
    {
        "name": "Beti Bachao Beti Padhao",
        "category": "women",
        "benefits": "Girl child support",
        "eligibility": "All families",
        "link": "https://wcd.nic.in"
    },
    {
        "name": "Sukanya Samriddhi Yojana",
        "category": "women",
        "benefits": "Savings for girl child",
        "eligibility": "Girl <10 years",
        "link": "https://nsiindia.gov.in"
    },
    {
        "name": "Mahila Shakti Kendra",
        "category": "women",
        "benefits": "Empowerment support",
        "eligibility": "Women",
        "link": "https://wcd.nic.in"
    },

    # ================= SENIOR =================
    {
        "name": "Indira Gandhi Pension",
        "category": "senior",
        "benefits": "Monthly pension",
        "eligibility": "60+ age",
        "link": "https://nsap.nic.in"
    },
    {
        "name": "Senior Citizen Saving Scheme",
        "category": "senior",
        "benefits": "High interest savings",
        "eligibility": "60+",
        "link": "https://nsiindia.gov.in"
    },

    # ================= CERTIFICATES =================
    {
        "name": "Income Certificate",
        "category": "other",
        "benefits": "Required for schemes",
        "eligibility": "All citizens",
        "link": "https://aaplesarkar.mahaonline.gov.in"
    },
    {
        "name": "Domicile Certificate",
        "category": "other",
        "benefits": "Proof of residence",
        "eligibility": "Maharashtra residents",
        "link": "https://aaplesarkar.mahaonline.gov.in"
    },
    {
        "name": "Caste Certificate",
        "category": "other",
        "benefits": "Reservation benefits",
        "eligibility": "SC/ST/OBC",
        "link": "https://aaplesarkar.mahaonline.gov.in"
    },
    {
        "name": "Caste Validity Certificate",
        "category": "other",
        "benefits": "Verification for reservation",
        "eligibility": "SC/ST/OBC",
        "link": "https://aaplesarkar.mahaonline.gov.in"
    },

    ]

    # SEARCH
    query = request.GET.get('q')
    if query:
        schemes = [s for s in schemes if query.lower() in s['name'].lower()]

    # PAGINATION
    paginator = Paginator(schemes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "app/services.html", {
        "page_obj": page_obj
    })
    
