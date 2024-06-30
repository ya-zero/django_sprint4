from django.utils import timezone

from blog.models import Post


def get_base_request():
    current_date = timezone.now()
    return (
        Post.objects.select_related("category", "author", "location")
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=current_date
        )
        .order_by("-pub_date")
    )
