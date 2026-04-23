from .models import ContactMessage

def unread_messages_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        count = ContactMessage.objects.filter(is_read=False).count()
    else:
        count = 0
    return {'unread_messages_count': count}
