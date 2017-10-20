from django.contrib import admin

# Register your models here.
from .models import Tag, UserImage

admin.site.register(Tag)
admin.site.register(UserImage)
