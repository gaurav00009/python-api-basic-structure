from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from packages.globalfunction import generateapikey

from .managers import CustomUserManager



# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=255, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type_data = ((1, "Parent"), (2, "Child"), (3, "Admin"))
    role_id = models.CharField(default=3, choices=user_type_data, max_length=10)
    username = models.CharField(_('user name'), max_length=255, unique=True)
    image = models.ImageField('Image', upload_to='user/images/', null=True)
    parent = models.ForeignKey(
        'self',
        related_name="childs",
        on_delete=models.CASCADE,
        null=True,
        default=None
    )
    register_from = models.CharField(
        max_length=50,
        choices=(
            ('web', 'WEB'),
            ('ios', 'IOS'),
            ('android', 'Android')
        ),
        default='web'
    )
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name.capitalize()

    def get_name(self):
        return self.first_name.title() + (
            '' if not self.last_name else (' ' + self.last_name.title())
        )
    
    @classmethod
    def getUserByEmail(cls, email):
        return cls.objects.filter(email=email).first()


    class Meta:
        db_table = "user"
        
    
        
@receiver(post_save, sender=User)
def save_api_key(sender, instance, created, **kwargs):
    if not instance.api_key and created:
        while True:
            api_key = generateapikey()
            user = User.objects.filter(api_key=api_key).first()
            if not user:
                break
        instance.api_key = api_key
        instance.save()
