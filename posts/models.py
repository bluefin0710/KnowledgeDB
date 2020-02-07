import os
from django.db import models
#from django.forms import ModelForm
#from django.urls import reverse
#from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.timezone import localtime 

# 2020-02-04 User Authentication start
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
# 2020-02-04 User Authentication end


# Create your models here.

#-- unused
#CATEGORY_CHOICES = [
#        ('ハードウェア', 'ハードウェア'),
#        ('ファームウェア', 'ファームウェア'),
#        ('ソフトウェア', 'ソフトウェア'),
#        ('メカトロニクス', 'メカトロニクス'),
#        ('その他', 'その他'),
#    ]

#-- unused
#SUBCATEGORY_CHOICES = [
#        ('0', 'BCA_CNT_300'),
#        ('1', 'INSERT_300'),
#        ('2', 'BACK_UP_300'),
#        ('3', 'BDET_PT_300'),
#        ('4', 'DISTR_300'),
#        ('5', 'INSERT_PT_300'),
#        ('6', 'POOL_300'),
#        ('99', 'その他'),
#    ]

#-- unused
#STATE_CHOICES = [
#        ('再現待ち', '再現待ち'),
#        ('調査中', '調査中'),
#        ('修正中', '修正中'),
#        ('修正なし', '修正なし'),
#        ('完了', '完了'),
#    ]

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

#-----------------------------------------------------------------------------


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

# 2020-02-04 User Authentication start
class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル

    usernameを使わず、emailアドレスをユーザー名として使うようにしています。

    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.email
# 2020-02-04 User Authentication end


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
            self.slug = slugify(self.name) +'E'+ slugify(localtime(timezone.now())) 
        super(Equipment, self).save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=255,
                            )
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#    def save(self, *args, **kwargs):
#        if not self.slug:
##            self.slug = slugify(self.name)
#            self.slug = slugify(self.name) +'C'+ slugify(localtime(timezone.now())) 
#        super(Category, self).save(*args, **kwargs)

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
            self.slug = slugify(self.name) +'Su'+ slugify(localtime(timezone.now()))
        super(Subcategory, self).save(*args, **kwargs)

class State(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Discoverydiv(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Severity(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Causediv(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#    def save(self, *args, **kwargs):
#        if not self.slug:
##            self.slug = slugify(self.name)
#            self.slug = slugify(self.name) +'Sa'+ slugify(localtime(timezone.now())) 
#        super(State, self).save(*args, **kwargs)
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

#    discoverydate = models.DateField(
#            null=False, 
#            blank=False,
#            verbose_name='発見日',
#            help_text='※必須',
#            )   

    discoverydate = models.CharField(
            max_length=10, 
            null=True, 
            blank=True,
            verbose_name='発見日',
            help_text='※必須',
            )   

#    discoverydiv = models.CharField(
#            choices=DISCOVERYDIV_CHOICES,
#            null=False, 
#            blank=False,
#            max_length=20,
#            verbose_name='発見カテゴリ',
#            help_text='※必須',
#            )

#---発見カテゴリの外部テーブルバージョン
    discoverydiv = models.ForeignKey(
            Discoverydiv, 
            on_delete=models.PROTECT,
            null=False, 
            blank=False,
            verbose_name='発見カテゴリ',
            help_text='※必須',
            )

#    severity = models.CharField(
#            choices=SEVERITY_CHOICES,
#            null=False, 
#            blank=False,
#            max_length=20,
#            verbose_name='重大度',
#            help_text='※必須',
#            )

#---重大度の外部テーブルバージョン
    severity = models.ForeignKey(
            Severity, 
            on_delete=models.PROTECT,
            null=False, 
            blank=False,
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

#    causediv = models.CharField(
#            choices=CAUSEDIV_CHOICES,
#            null=True, 
#            blank=True, 
#            max_length=20,
#            verbose_name='原因区分',
#            help_text='',
#            )

#---原因区分のの外部テーブルバージョン
    causediv = models.ForeignKey(
            Causediv, 
            on_delete=models.PROTECT,
            null=True, 
            blank=True,
            verbose_name='原因区分',
            help_text='',
            )
    cause = models.TextField(
            blank=True, 
            default='',
            verbose_name='詳細原因',
            help_text='',
            )
    counterplan = models.TextField(
            blank=True, 
            default='',
            verbose_name='処置内容(対策)',
            help_text='',
            )
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
            verbose_name='関連資料の置き場（共有ファイルサーバーのパス）',
            help_text='※任意　パスの存在はチェックしていません。正しいパスを入力してください。',
            )
#    completiondate = models.DateField(
#            null=True, 
#            blank=True,
#            verbose_name='完了日',
#            help_text='',
#            )
    completiondate = models.CharField(
            max_length=10, 
            null=True, 
            blank=True,
            verbose_name='完了日',
            help_text='',
            )   
#    author = models.ForeignKey(
#           'auth.User', 
#            null=True, 
#            blank=True,
#            on_delete=models.CASCADE,
#            )    
    author = models.CharField(
            max_length=128, 
            null=True, 
            blank=True,
            verbose_name='登録者',
            help_text='',
#            on_delete=models.CASCADE,
            )    
    published_date = models.DateTimeField( #published_atと重複しているので、削除対象
            null=True,
            blank=True, 
            )
    created_at = models.DateField(
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
#            self.author = User.username
#            print(User.email)
#            print(User.username)
#            print(User.email)
#            print(User.EMAIL_FIELD)
#            print(User.get_full_name)

            super().save(*args, **kwargs)

#admin サイトで、オブジェクトをわかりやすく表示するために指定        
    def __str__(self):
        return self.overview[:15]
#        return self.pk

    def summary(self):
        return self.content[:30]

#-----------------------------------------------------------------------------

class ContentImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_image = models.ImageField(
 #                                    upload_to='uploaded_files/',
                                    verbose_name='画像ファイル',
                                    )
 
class ContentFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_file = models.FileField(
#                                    upload_to='uploaded_files/',
                                    verbose_name='添付ファイル',
                                    )
    def css_class(self):
        name, extension = os.path.splitext(self.content_file.name)
        if extension == '.jpg':
            return 'image'
        if extension == '.gif':
            return 'image'
        if extension == '.png':
            return 'image'
        if extension == '.jpeg':
            return 'image'
        if extension == '.tiff':
            return 'image'
        if extension == '.bmp':
            return 'image'
        return 'other'
#    file_type = models.CharField(max_length=10, 
#                                 null=True, 
#                                 blank=True,
#                                 verbose_name='ファイルタイプ',
#                                 help_text='添付したファイルタイプ',                                
#                                 )

#-----------------------------------------------------------------------------
class Factordiv(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#-- 追加項目：市場への波及性
class MarketSpillover(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.TextField(
            blank=True, 
            default='',
            verbose_name='理由',
            help_text='',
            )
#    factordiv = models.ForeignKey(Factordiv, on_delete=models.CASCADE)
#            null=True, 
#            blank=True,
#            verbose_name='要因',
#            help_text='(※「その他」を選択した場合、その内容を理由の欄に記入してください。)',
#            )
    factor = models.CharField(
            max_length=25, 
            null=True, 
            blank=True,
            verbose_name='要因',
            help_text='(「作業者」、「部品」、「設計」、「設備」、「作業指導」等)',
            )
    shippingdate_start = models.CharField(
            max_length=10, 
            null=True, 
            blank=True,
            verbose_name='対象品出荷開始日',
            help_text='',
            )   
    shippingdate_end = models.CharField(
            max_length=10, 
            null=True, 
            blank=True,
            verbose_name='対象品出荷終了日',
            help_text='',
            )   
    shipping = models.CharField(
            max_length=255, 
            null=True, 
            blank=True,
            verbose_name='出荷先',
            help_text='',
            )
    serial_start = models.CharField(
            max_length=255,
            null=True, 
            blank=True,
            verbose_name='対象製造番号開始',
            help_text='',
            )
    serial_end = models.CharField(
            max_length=255,
            null=True, 
            blank=True,
            verbose_name='対象製造番号終了',
            help_text='',
            )
    targetno = models.CharField(
            max_length=255,
            null=True, 
            blank=True,
            verbose_name='対象台数',
            help_text='',
            )
    influence = models.TextField(
            blank=True, 
            default='',
            verbose_name='他機種への影響',
            help_text='',             
            )

#-----------------------------------------------------------------------------
#--登録内容に対するコメント
class Comment(models.Model):
    """コメント."""
    name = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    target = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_publick = models.BooleanField(default=False)
 
    def __str__(self):
        return self.name
  
#--登録内容に対するコメントの返信
class Reply(models.Model):
    """返信コメント."""
    name = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
 
    def __str__(self):
        return self.name
    
#-----------------------------------------------------------------------------

def user_portfolio_directory_path(instance, filename):
    return 'image-{0}/{1}'.format(instance.id, filename)

#class Image_file(models.Model):
# ｍ   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    image = models.ImageField(upload_to=user_portfolio_directory_path, null=True, blank=True)
#    uploaded_at = models.DateTimeField(auto_now_add=True)
