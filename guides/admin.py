from django.contrib import admin
from .models import Guide, Category, Tag, Article

# Register your models here.

admin.site.register(Guide)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)