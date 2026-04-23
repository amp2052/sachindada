from django import forms
from .models import ContactMessage,Volunteer

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "grievance_type", "message"]
        
    
    
class VolunteerForm(forms.ModelForm):

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

    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'interests', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Why do you want to volunteer?',
                'rows': 3
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.interests = ", ".join(self.cleaned_data['interests'])
        if commit:
            instance.save()
        return instance