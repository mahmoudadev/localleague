from django.contrib import admin
from .models import Field, Image



class InlineImage(admin.TabularInline):
    model =  Image
    extra = 1

class FieldAdmin(admin.ModelAdmin):
    inlines = [InlineImage]
    list_display = ['name', 'area', 'location', 'is_available']
    list_filter = ['location', 'area', 'is_available']
    list_search = ['location', 'area', 'is_available']

admin.site.register(Field, FieldAdmin)
admin.site.register(Image)