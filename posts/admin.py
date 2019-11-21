from django.contrib import admin
#from django.db import models

# Register your models here.
#from .models import Post
from .models import (
        Post,
        Checklist_A,
        Equipment,
        Category,
        Subcategory,
        State,
#        ContentImage,
        ContentFile,
        )


#class ContentImageInline(admin.TabularInline):
#    model = ContentImage
#    extra = 1

class ContentFileInline(admin.TabularInline):
    model = ContentFile
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [
#        ContentImageInline,
        ContentFileInline,
    ]    
#    list_display = ['catergory',]
#    list_display = ('id','equipment', 'catergory', 'subcatergory', 'subtitle', 'discoverydate', ) 

#admin.site.register(Post)

admin.site.register(Equipment)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(State)
admin.site.register(Checklist_A)
admin.site.register(Post,PostAdmin)
