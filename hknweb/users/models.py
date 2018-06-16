from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class CustomUserManager(UserManager):
    """
    User Manager for users.CustomUser.

    For the moment, CustomUser isn't doing anything different enough from auth.User
    to require this class to change anything, but I'm including it as future-proofing
    in case something changes.
    """
    pass

class CustomUser(AbstractUser):
    username = models.CharField(blank=True, max_length=255)
    first_name = models.CharField(_('first name'), max_length=40, blank=True, null=True, unique=False)
    last_name = models.CharField(_('last name'), max_length=40, blank=True, null=True, unique=False)
    display_name = models.CharField(_('display name'), max_length=14, blank=True, null=True, unique=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'
        abstract = False

    def __str__(self):
        return self.email

class CustomUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCASE)

    date_of_birth = models.DateField(null=True, blank=True)
    picture = models.ImageField(blank=True)
    private = models.BooleanField(default=True, verbose_name="Private profile?")
    phone_regex = RegexValidator(regex=r'^/([^\d]*\d){10}$/', message="Phone number must be ten digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    resume = models.FileField(blank=True)
    graduation_date = models.DateField(null=True, blank=True)

    class Meta():
        db_table = 'user_profile'

#    @receiver(post_save, sender=User)
#    def create_user_profile(sender, instance, created, **kwargs):
#        if created:
#            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def clean(self):
        if self.phone_number:
            self.phone_number = re.sub("[^0-9]", "",self.phone_number)
            self.phone_number = "("+self.phone_number[0:3]+") "+self.phone_number[3:6]+"-"+self.phone_number[6:]

@reciever(user_signed_up)
def set_initial_user_names(request, user, sociallogin=None, **kwargs):

    if sociallogin:
        if sociallogin.account.provider == 'google':
            user.first_name = sociallogin.account.extra_data['given_name']
            user.last_name = sociallogin.account.extra_data['family_name']

    profile = UserProfile(user=user)
    profile.save

#    user.guess_display_name()
#    user.save()

