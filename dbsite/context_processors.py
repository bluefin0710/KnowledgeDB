from django.db.models import Count, Q

from posts.models import Equipment, Category, Subcategory, State 


def common(request):
    context = {
        'equipments': Equipment.objects.annotate(
            num_posts=Count('post', filter=Q(post__is_public=True))),
        'categories': Category.objects.annotate(
            num_posts=Count('post', filter=Q(post__is_public=True))),
        'subcategories': Subcategory.objects.annotate(
            num_posts=Count('post', filter=Q(post__is_public=True))),
        'states': State.objects.annotate(
            num_posts=Count('post', filter=Q(post__is_public=True))),
    }
    return context
