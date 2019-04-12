from django.contrib import admin
from .models import Announcement




class AnnAdmin(admin.ModelAdmin):

    list_display = ['title', 'author', 'created_at', 'modified_at']


admin.site.register(Announcement, AnnAdmin)