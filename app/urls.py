from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # path('news/', views.news, name='news'),
    path('stock/', views.stock, name='stock'),
        path('faq/', views.faq, name='faq'),

    path('schemes/', views.schemes, name='schemes'),
path('services/', views.services, name='services'),
    path('press/', views.press, name='press'),
    path('join/', views.join, name='join'),
    path('stock/', views.stock, name='stock'),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("contact-submissions/", views.contact_submissions, name="contact_submissions"),
    path("contact-submissions/delete/<int:pk>/", views.delete_contact_message, name="delete_contact_message"),
path("contact-submissions/mark-read/<int:pk>/", views.mark_as_read, name="mark_as_read"),
    path("contact-submissions/download-pdf/", views.download_contact_pdf, name="download_contact_pdf"),
    path('team-member/delete/<int:pk>/', views.delete_team_member, name='delete_team_member'),
    path('admin/team-members/download/', views.download_team_members_pdf, name='download_team_members_pdf'),
    path('team-member/<int:pk>/reviewed/', views.mark_team_member_reviewed, name='mark_team_member_reviewed'),
    path('team-member/<int:pk>/unreviewed/', views.mark_team_member_unreviewed, name='mark_team_member_unreviewed'),

path('team-member/pdf/', views.download_team_members_pdf, name='download_team_members_pdf'),



path('chatbot/', views.chat_with_ai, name='chatbot'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),



    
    
    path('public-issues/', views.public_issues, name='public_issues'),
    path('gallery/', views.gallery_view, name='gallery'),
path('news/', views.news, name='news'),]
