
from .models import Category
from django.contrib.auth import get_user_model


def categories_processor(request):
    user_model = get_user_model()
    registered_users = user_model.objects.all().select_related('profile').order_by('username')

    return {
        'categories': Category.objects.all(),
        'registered_users': registered_users,
    }