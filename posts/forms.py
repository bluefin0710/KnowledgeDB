# -*- coding: utf-8 -*-
from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import Post
from .models import (
            Equipment,
#            Category,
            Subcategory,
#            State,
#            Checklist_A,
#            ContentImage,
            ContentFile,
            )

from .models import (
#            CATEGORY_CHOICES,
#            STATE_CHOICES,
            DISCOVERYDIV_CHOICES,
            SEVERITY_CHOICES,
            CAUSEDIV_CHOICES,
            )


#from .models import Image_File

#from .models import PostForm


#class ModelFormWithFormSetMixin:
#
#    def __init__(self, *args, **kwargs):
#        super(ModelFormWithFormSetMixin, self).__init__(*args, **kwargs)
#        self.formset = self.formset_class(
#            instance=self.instance,
#            data=self.data if self.is_bound else None,
#        )
#
#    def is_valid(self):
#        return super(ModelFormWithFormSetMixin, self).is_valid() and self.formset.is_valid()
#
#    def save(self, commit=True):
#        saved_instance = super(ModelFormWithFormSetMixin, self).save(commit)
#        self.formset.save(commit)
#        return saved_instance
#
#class ContentFileForm(ModelForm):
#
#    class Meta:
#        model = ContentFile
#        fields = ('content_file',)


#CATEGORY_CHOICES = [('', '------')] + CATEGORY_CHOICES

#STATE_CHOICES = [('', '------')] + STATE_CHOICES

DISCOVERYDIV_CHOICES = [('', '------')] + DISCOVERYDIV_CHOICES

SEVERITY_CHOICES = [('', '------')] + SEVERITY_CHOICES

CAUSEDIV_CHOICES = [('', '------')] + CAUSEDIV_CHOICES


class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ('name',
                  )
    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)   
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        

class SubcategoryForm(ModelForm):
    class Meta:
        model = Subcategory
        fields = ('name',
                  )
    def __init__(self, *args, **kwargs):
        super(SubcategoryForm, self).__init__(*args, **kwargs)   
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PostForm(ModelForm):
#    checklist = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),required=True)
#   formset_class = FileFormset

    class Meta:
        model = Post
        fields = (
                'equipment',
                'category',
                'subcategory',
                'state',
                'discoverydate',
                'discoverydiv',
                'severity',
                'overview',
                'content',
                'causediv',
                'cause',
                'counterplan',
                'checklist',
                'evidence',
                'completiondate',
#                'url_link',               
                'file_link',
                )
        widgets = {
#            'subtitle': forms.TextInput(attrs={'size': 40}),
#            'subcategory': forms.CheckboxInput(),
            'discoverydate': forms.DateInput(format=('%Y-%m-%d'), 
                                             attrs={'type':'date', 
                                            'placeholder':'Select a date'},
                                            ),
            'overview': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 6}),
#            'actual_file1': forms.ClearableFileInput(attrs={'multiple': True}),
            'cause': forms.Textarea(attrs={'cols': 80, 'rows': 6}),
            'counterplan': forms.Textarea(attrs={'cols': 80, 'rows': 6}),
            'checklist': forms.CheckboxSelectMultiple,
            'evidence': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
 #           'checklist': forms.CheckboxSelectMultiple(attrs={
 #                                                       'class': 'form-check-input',
 #                                                       }),
 #           'checklist': forms.ModelMultipleChoiceField(queryset=Checklist_A.objects.all()),
            'completiondate': forms.DateInput(format=('%Y-%m-%d'), 
                                             attrs={'type':'date', 
                                                    'placeholder':'Select a date'},
                                            ),
         }
  
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)   
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        #-- Checklist_Aの名前でソート
#        self.fields['checklist'].queryset = Checklist_A.objects.order_by('name')
#        self.fields['checklist'].choices = Checklist_A.objects.all().values_list("name")
#
#        self.fields['equipment'].queryset = Equipment.objects.order_by('name')
#        self.fields['equipment'].choices = Equipment.objects.all().values_list("name")


#--問い合わせフォーム 
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(max_length=1000)
    sender = forms.EmailField()

#--検索フォーム 
class SearchForm(forms.Form):
#    equipment = models.ForeignKey(
#            Equipment, 
#            on_delete=models.PROTECT,
#            required=False,  # 必須ではない
#            label='機種名称',
#    )
    equipment = forms.CharField(
        max_length=128, 
        initial='',
        label='機種名称',
        required=False,  # 必須ではない
    )
    overview = forms.CharField(
        max_length=128, 
        initial='',
        label='発見概要',
        required=False,  # 必須ではない
    )
    content = forms.CharField(
        max_length=128, 
        initial='',
        label='発見内容',
        required=False,  # 必須ではない
    )
    category = forms.CharField(
        max_length=128, 
#        choices=CATEGORY_CHOICES,
        initial='',
        label='大分類',
        required=False,  # 必須ではない
    )
    subcategory = forms.CharField(
        max_length=128, 
#        choices=CATEGORY_CHOICES,
        initial='',
        label='小分類',
        required=False,  # 必須ではない
    )
    state = forms.CharField(
        max_length=128, 
#        choices=STATE_CHOICES,
        initial='',
        label='状態',
        required=False,  # 必須ではない
    )
    discoverydiv = forms.CharField(
        max_length=128, 
#        choices=DISCOVERYDIV_CHOICES,
        initial='',
        label='発見区分',
        required=False,  # 必須ではない
    )
    severity = forms.CharField(
        max_length=128, 
#        choices=SEVERITY_CHOICES,
        initial='',
        label='重大度',
        required=False,  # 必須ではない
    )
    causediv = forms.CharField(
        max_length=128, 
#        choices=CAUSEDIV_CHOICES,
        initial='',
        label='原因区分',
        required=False,  # 必須ではない
    )
    cause = forms.CharField(
        max_length=128, 
        initial='',
        label='原因内容',
        required=False,  # 必須ではない
    )
    counterplan = forms.CharField(
        max_length=128, 
        initial='',
        label='対策内容',
        required=False,  # 必須ではない
    )
    checklist = forms.CharField(
        max_length=128, 
        initial='',
        label='チェックリスト',
        required=False,  # 必須ではない
    )
    author = forms.CharField(
        max_length=128, 
        initial='',
        label='登録者',
        required=False,  # 必須ではない                
    )


#class Image_FileForm(ModelForm):
#    image = forms.ImageField(
#        widget=forms.ClearableFileInput(attrs={'multiple': True}),
#    )
#    class Meta:
#        model = Image_File
#        fields = ('image',)

class ContentFileForm(forms.ModelForm):
    class Meta:
        model=ContentFile
        fields = ('content_file',)

    def __init__(self, *args, **kwargs):
        super(ContentFileForm, self).__init__(*args, **kwargs)

FileFormset = inlineformset_factory(
    parent_model=Post,
    model=ContentFile,
    form=ContentFileForm,
#    form=PostForm,
    fields='__all__',
    extra=3, 
    max_num=5, 
    can_delete=True,
    )

