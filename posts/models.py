from django.db import models
#from django.forms import ModelForm
#from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.timezone import localtime 


# Create your models here.

CATEGORY_CHOICES = [
        ('ハードウェア', 'ハードウェア'),
        ('ファームウェア', 'ファームウェア'),
        ('ソフトウェア', 'ソフトウェア'),
        ('メカトロニクス', 'メカトロニクス'),
        ('その他', 'その他'),
    ]

SUBCATEGORY_CHOICES = [
        ('0', 'BCA_CNT_300'),
        ('1', 'INSERT_300'),
        ('2', 'BACK_UP_300'),
        ('3', 'BDET_PT_300'),
        ('4', 'DISTR_300'),
        ('5', 'INSERT_PT_300'),
        ('6', 'POOL_300'),
        ('99', 'その他'),
    ]

STATE_CHOICES = [
        ('再現待ち', '再現待ち'),
        ('調査中', '調査中'),
        ('修正中', '修正中'),
        ('修正なし', '修正なし'),
        ('完了', '完了'),
    ]

DISCOVERYDIV_CHOICES = [
        ('単体テスト', '単体テスト'),
        ('総合テスト', '総合テスト'),
        ('その他', 'その他'),
    ]

SEVERITY_CHOICES = [
        ('重度', '重度'),
        ('軽度', '軽度'),
        ('正常', '正常'),
    ]

CAUSEDIV_CHOICES = [
        ('仕様ミス', '仕様ミス'),
        ('ハード設計ミス', 'ハード設計ミス'),
        ('ソフト設計ミス', 'ソフト設計ミス'),
        ('仕様変更', '仕様変更'),
        ('その他', 'その他'),
    ]


#
#CHECKLIST_CHOICES = [
#        ('単体動作確認', '単体動作確認'),
#        ('総合動作確認', '総合動作確認'),
#        ('BOM改版', 'BOM改版'),
#        ('回路図改版', '回路図改版'),
#        ('P版改版', 'P版改版'),
#        ('組立図改版', '組立図改版'),
#    ]
#

#class Post(models.Model):
#    title = models.CharField(max_length=100)
#    published = models.DateTimeField()
#    image = models.ImageField(upload_to='media/')
#    body = models.TextField()
#
#    def __str__(self):
#        return self.title
#
#    def summary(self):
#        return self.body[:30]


class Equipment(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='装置名称',
                            )
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
#            self.slug = slugify(self.name)
            self.slug = slugify(self.name) +'E'+ slugify(localtime(timezone.now())) 
            super(Equipment, self).save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=255,
                            )
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
#            self.slug = slugify(self.name)
            self.slug = slugify(self.name) +'C'+ slugify(localtime(timezone.now())) 
            super(Category, self).save(*args, **kwargs)

class Subcategory(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='小区分',                            
                            )
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
#            self.slug = slugify(self.name)
            self.slug = slugify(self.name) +'Su'+ slugify(localtime(timezone.now()))
            super(Subcategory, self).save(*args, **kwargs)

class State(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
#            self.slug = slugify(self.name)
            self.slug = slugify(self.name) +'Sa'+ slugify(localtime(timezone.now())) 
            super(State, self).save(*args, **kwargs)

#
#class Checklist_A(models.Model):   
#    name = models.CharField(
#            null=False, 
#            blank=False,
#            max_length=25,
##            choices=CHECKLIST_CHOICES,
#            )
#    def __str__(self): 
#        return self.name
#
        
class Checklist_A(models.Model):   
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

        
class Post(models.Model):
    equipment = models.ForeignKey(
            Equipment, 
            on_delete=models.PROTECT,
            null=False, 
            blank=False,
            verbose_name='機種名称',
            help_text='※必須',
            )
    category = models.ForeignKey(
            Category, 
            on_delete=models.PROTECT,
            null=False, 
            blank=False,
            verbose_name='大分類',
            help_text='※必須',
            )
    subcategory = models.ForeignKey(
            Subcategory, 
            on_delete=models.PROTECT,
            null=False, 
            blank=False,
            verbose_name='小分類',
            help_text='※必須',
           )
    state = models.ForeignKey(
            State, 
            on_delete=models.PROTECT,
            null=False, 
            blank=False,
            verbose_name='状態',
            help_text='※必須',
            )
#    subtitle = models.CharField(
#            null=False, 
#            blank=False,
#            max_length=100,
#            verbose_name='不具合名称',
#            help_text='※必須',
#            )
#    category = models.CharField(
#            choices=CATEGORY_CHOICES,
#            null=False, 
#            blank=False,
#            max_length=3,
#            verbose_name='大分類',
#            help_text='※必須',
#            )
#    subcategory = models.CharField(
#            choices=SUBCATEGORY_CHOICES,
#            null=False, 
#            blank=False,
#            max_length=2,
#            verbose_name='小分類',
#            help_text='※必須',
#            )
#
#    state = models.CharField(
#            choices=STATE_CHOICES,
#            null=False, 
#            blank=False,
#            max_length=1,
#            verbose_name='状態',
#            help_text='※必須',
#            )
    discoverydate = models.DateField(
            null=False, 
            blank=False,
            verbose_name='発見日',
            help_text='※必須',
            )   
    discoverydiv = models.CharField(
            choices=DISCOVERYDIV_CHOICES,
            null=False, 
            blank=False,
            max_length=20,
            verbose_name='発見カテゴリ',
            help_text='※必須',
            )
##    actual_file = models.FileField(upload_to='uploaded_files', validators=[validate_file_extension])
#    actual_file = models.FileField(
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='添付ファイル',
#            help_text='※任意',
#            )
    severity = models.CharField(
            choices=SEVERITY_CHOICES,
            null=False, 
            blank=False,
            max_length=20,
            verbose_name='重大度',
            help_text='※必須',
            )
    overview = models.TextField(
            verbose_name='発見概要',
            help_text='※必須',
            )
    content = models.TextField(
            verbose_name='発見内容',
            help_text='※必須',
            )
#    actual_file1 = models.FileField(    
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='添付ファイル１',
#            help_text='※任意',
#            )
#    actual_file2 = models.FileField(
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='添付ファイル２',
#            help_text='※任意',
#            )
#    Image_file1 = models.ImageField(
#            upload_to='uploaded_files', 
#            null=True, 
#            blank=True,
#            verbose_name='イメージファイル１',
#            help_text='※任意',
#            )
#    Image_file2 = models.ImageField(
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='イメージファイル２',
#            help_text='※任意',
#            )
    causediv = models.CharField(
            choices=CAUSEDIV_CHOICES,
            null=True, 
            blank=True, 
            max_length=20,
            verbose_name='原因区分',
            help_text='',
            )
    cause = models.TextField(
            blank=True, 
            default='',
            verbose_name='詳細原因',
            help_text='',
            )
#    actual_file3 = models.FileField(
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='添付ファイル３',
#            help_text='※任意',
#            )
#    actual_file4 = models.FileField(
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='添付ファイル４',
#            help_text='※任意',
#            )
#    Image_file3 = models.ImageField(
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='イメージファイル３',
#            help_text='※任意',
#            )
#    Image_file4 = models.ImageField(
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='イメージファイル４',
#            help_text='※任意',
#            )
    counterplan = models.TextField(
            blank=True, 
            default='',
            verbose_name='処置内容(対策)',
            help_text='',
            )
#    actual_file5 = models.FileField(
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='添付ファイル５',
#            help_text='※任意',
#            )
#    Image_file5 = models.ImageField(
#            upload_to='uploaded_files/', 
#            null=True, 
#            blank=True,
#            verbose_name='イメージファイル５',
#            help_text='※任意',
#            )
    checklist = models.ManyToManyField(
            Checklist_A, 
            blank=True,
            verbose_name='チェックリスト',
            help_text='',
            )
    evidence = models.TextField(
            blank=True, 
            default='',
            verbose_name='エビデンス',
            help_text='（チェックリストのエビデンス登録）',
            )
    url_link = models.URLField(
            null=True, 
            blank=True,
            verbose_name='URLリンク',
            help_text='※任意',
            )
    file_link = models.CharField(
            max_length=512, 
            null=True, 
            blank=True,
            verbose_name='ファイルサーバーPATH',
            help_text='※任意',
            )
    completiondate = models.DateField(
            null=True, 
            blank=True,
            verbose_name='完了日',
            help_text='',
            )
#    author = models.CharField(
#             null=True, 
#            blank=True,
#            max_length=255,
#            )
    author = models.ForeignKey(
           'auth.User', 
             null=True, 
            blank=True,
            on_delete=models.CASCADE,
            )    
    published_date = models.DateTimeField(
            null=True, 
            blank=True,
            ) 
    created_at = models.DateTimeField(
            auto_now_add=True,
            )
    updated_at = models.DateTimeField(
            auto_now=True,
            )
    published_at = models.DateTimeField(
            null=True,
            blank=True, 
            )
    is_public = models.BooleanField(
            default=True,
#            default=False,
            )

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
#        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
 #           self.author = user.username
            super().save(*args, **kwargs)

#admin サイトで、オブジェクトをわかりやすく表示するために指定        
    def __str__(self):
        return self.overview[:15]

    def summary(self):
        return self.content[:30]

class ContentImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_image = models.ImageField(upload_to='uploaded_files/',
                                      verbose_name='画像ファイル',
                                      )

class ContentFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_file = models.FileField(upload_to='uploaded_files/',
                                    verbose_name='添付ファイル',
                                    )
    file_type = models.CharField(max_length=10, 
                                 null=True, 
                                 blank=True,
                                 verbose_name='ファイルタイプ',
                                 help_text='添付したファイルタイプ',
                                 
                                 )

def user_portfolio_directory_path(instance, filename):
    return 'image-{0}/{1}'.format(instance.id, filename)

#class Image_file(models.Model):
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    image = models.ImageField(upload_to=user_portfolio_directory_path, null=True, blank=True)
#    uploaded_at = models.DateTimeField(auto_now_add=True)
