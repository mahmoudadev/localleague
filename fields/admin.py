from django.contrib import admin
from .models import Field, Image



class InlineImage(admin.TabularInline):
    model =  Image
    extra = 1

class FieldAdmin(admin.ModelAdmin):
    inlines = [InlineImage]

admin.site.register(Field, FieldAdmin)
admin.site.register(Image)