from django.contrib import admin
from django.utils.text import Truncator

from blog.constant import LEN_ADMIN_POST, MESSAGE_TEXT_RU
from blog.models import Category, Location, Post


admin.site.empty_value_display = 'Не задано'


class PostAdminInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text_view',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',

    )
    list_editable = (
        'pub_date',
    )
    search_fields = ('title', 'text', 'location', 'author',)
    list_filter = ('is_published', 'category')
    list_display_links = ('title',)

    def text_view(self, obj):
        if len(obj.text) > LEN_ADMIN_POST:
            return Truncator(obj.text).words(LEN_ADMIN_POST,
                                             truncate=f' [{MESSAGE_TEXT_RU}]')
        return obj.text


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostAdminInline,
    )
    list_display = (
        'title',
        'description',
        'slug',
        'is_published'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    list_filter = ('is_published',)
    list_display_links = ('name',)
