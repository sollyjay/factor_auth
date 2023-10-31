from django.db import models
from django.core.validators import RegexValidator
from django.db.models.deletion import CASCADE
from FactorApp.manager import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
import uuid
from django.utils.timezone import now

GENDER_CHOICE = (('Male','Male'),('Female','Female'))

def upload_to(instance, filename):
    return 'profile_pics/{filename}'.format(filename=filename)

def post_upload(instance, filename):
    file_extension = filename.split('.')[-1]
    file = f"post_uploads/{uuid.uuid4()}.{file_extension}"
    return file

class User(AbstractUser):
    """CustomUser model."""
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    objects = UserManager()
    contact = models.CharField(validators = [RegexValidator(regex = r"^\+?1?\d{8,15}$")], max_length = 16)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=34, default='Male')
    dob = models.DateField(max_length=23, null=True)
    avatar = models.ImageField(_('Image'), upload_to=upload_to, default='default.png')
    followers = models.ManyToManyField(to="self", through="Follow", related_name="user_followers", symmetrical=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        try:
            image = Image.open(self.avatar.path)
            if image.height > 300 or image.width > 300:
                image.thumbnail((150,150))
                image.save(self.avatar.path)   
        except:
            print("******Error in Processing images*******")
            return        
    
    @property
    def get_photo_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "/static/default.png"
    
    @property
    def get_followers(self):
        return self.followers.count()

    def __str__(self):
        return f'{self.email}'

"""
class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed_date = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["from_user", "to_user"]
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(from_user=models.F("to_user")),
            ),
        ]
"""


class Follow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_follower')
    followers = models.ManyToManyField(User, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def num_followers(self):
        return self.followers.count()
    
    def __str__(self):
        return f'{self.user}'


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_following')
    followings = models.ManyToManyField(User, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def num_followings(self):
        return self.followings.count()
    
    def __str__(self):
        return f'{self.user}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    images = models.ImageField(_('Image'), upload_to=upload_to, blank=True, null=True)
    videos = models.FileField(_('Video'), upload_to=upload_to, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    unlikes = models.ManyToManyField(User, related_name='post_unlikes', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)

    def duration(self):
        return now() - self.created_date
    
    @property
    def num_likes(self):
        return self.likes.count()

    @property
    def num_unlikes(self):
        return self.unlikes.count()

    def __str__(self):
        return f'{self.user.email}'

