from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
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
        Causediv,
        Discoverydiv,
        Severity,
        MarketSpillover,
        Factordiv,
        User,
        )


#class ContentImageInline(admin.TabularInline):
#    model = ContentImage
#    extra = 1

class ContentFileInline(admin.TabularInline):
    model = ContentFile
    extra = 1

class MarketSpilloverInline(admin.TabularInline):
    model = MarketSpillover
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [
#        ContentImageInline,
        ContentFileInline,
        MarketSpilloverInline,
    ]    
#    list_display = ['catergory',]
#    list_display = ('id','equipment', 'catergory', 'subcatergory', 'subtitle', 'discoverydate', ) 

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

#admin.site.register(Post)
admin.site.register(Equipment)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(State)
admin.site.register(Checklist_A)
admin.site.register(Causediv)
admin.site.register(Discoverydiv)
admin.site.register(Severity)
admin.site.register(Post,PostAdmin)
admin.site.register(Factordiv)
admin.site.register(MarketSpillover)
admin.site.register(User, MyUserAdmin)
