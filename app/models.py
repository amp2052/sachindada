from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    subject = models.CharField(max_length=200, default="General Inquiry")

    GRIEVANCE_CHOICES = [
        ("Infrastructure Issues", "Infrastructure Issues"),
        ("Healthcare Services", "Healthcare Services"),
        ("Education and Schools", "Education and Schools"),
        ("Water Supply", "Water Supply"),
        ("Electricity", "Electricity"),
        ("Sanitation", "Sanitation"),
        ("Public Transport", "Public Transport"),
        ("Law and Order", "Law and Order"),
        ("Land and Property", "Land and Property"),
        ("Social Welfare Schemes", "Social Welfare Schemes"),
        ("Other", "Other"),
    ]

    grievance_type = models.CharField(max_length=100, choices=GRIEVANCE_CHOICES, default="Other")

    message = models.TextField(default="Other")

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.grievance_type}"
    
class Volunteer(models.Model):
    INTEREST_CHOICES = [
        ("Education initiatives", "Education initiatives"),
        ("Infrastructure development", "Infrastructure development"),
        ("Women empowerment", "Women empowerment"),
        ("Agricultural support", "Agricultural support"),
        ("Healthcare programs", "Healthcare programs"),
        ("Environmental conservation", "Environmental conservation"),
        ("Youth development", "Youth development"),
        ("Social welfare", "Social welfare"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    interests = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=255)  
    mobile_no = models.CharField(max_length=15)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False) 

    def __str__(self):
        return self.name


# latest change
    
from django.db import models

# ================= GALLERY =================
class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ================= NEWS =================
class News(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='news/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
    
    
    
    
    
    
    
    
    
    from django.db import models

class IssueReport(models.Model):

    # Personal Info
    name = models.CharField(max_length=200)
    village = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15)

    # Survey Questions
    main_issue = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    priority = models.CharField(max_length=100)
    scheme = models.CharField(max_length=50)
    roads = models.CharField(max_length=50)
    water = models.CharField(max_length=50)
    jobs = models.CharField(max_length=50)

    suggestion = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.village}"