from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class Roles(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    normalized_name = models.CharField(max_length=255, null=True, blank=True)
    concurrency_stamp = models.TextField(null=True, blank=True)
    descripton = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(null=False)

    class Meta:
        verbose_name_plural = "Roles"


class MyUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not(username):
            raise ValueError("Username is a required Field")
        if not(email):
            raise ValueError("Email is a required field")
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return (user)


    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)


def get_default_profile_image():
    return "default_images/default_profile_image.png"

def get_profile_image_filepath(self, filename):
    ext = filename.split(".")[-1]
    newfilename = f"profile-picture-{self.pk}.{ext}"
    return f'images/{self.id}/{newfilename}'


class MyUser(AbstractBaseUser):
    username = models.CharField(verbose_name='username', max_length=256, unique=True, null=True, blank=True)
    normalized_username = models.CharField(verbose_name='normalized_username', max_length=256, unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name="Email", max_length=256, unique=True, null=False, blank=False)
    normalized_email = models.EmailField(verbose_name="normalized_email", max_length=256, unique=True, null=True, blank=True)
    email_confirmed = models.BooleanField(default=False, null=False)
    security_stamp = models.TextField(null=True, blank=True)
    concurrency_stamp = models.TextField(null=True, blank=True)
    #  Change it to phone number field in furure
    phone_number = models.CharField(max_length=256, null=True)
    phone_number_confirmed = models.BooleanField(default=False, null=False)
    two_factor_enabled = models.BooleanField(default=False, null=False)
    # This field stores the time difference in date and time with UTC. 
    # [LockoutEnd] [datetimeoffset](7) NULL,
    locl_out_end = models.DateTimeField(null=True,blank=True)
    lock_out_enabled = models.BooleanField(default=False, null=False)
    access_failed_count = models.IntegerField(null=True)
    # This field has to be added
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=1, null=True)
    dob = models.DateTimeField(null=True)
    created_by = models.IntegerField(null=True) #null was False
    created_on = models.DateTimeField(null=True, auto_now_add=True)
    modified_by = models.IntegerField(null=True) #null was False
    modified_on = models.DateTimeField(null=True, auto_now_add=True)
    # is_authorised_by_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    forgot_password_otp = models.CharField(max_length=6, null=True, blank=True)
    profile_picture = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    # device_token = models.CharField(max_length=256, blank=True, null=True)
    # device_id = models.CharField(max_length=256, blank=True, null=True)

    # Tie the custom user to the custom account manager
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class UserRoles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "User Roles"



class SecModules(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='module_created_by', on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='module_modified_by', on_delete=models.SET_NULL, null=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False)
    module_name = models.CharField(max_length=255, null=True, blank=True)
    module_description = models.TextField(null=True, blank=True)
    # ParentId
    area = models.TextField(null=True, blank=True)
    action_name = models.TextField(null=True, blank=True)
    controller_name = models.TextField(null=True, blank=True)
    module_class = models.TextField(null=True, blank=True)
    order_no = models.IntegerField(null=False, blank=False)

    class Meta:
        verbose_name_plural = "Sec Modules"



class SecRoleModules(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sec_module_created_by', on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sec_module_modified_by', on_delete=models.SET_NULL, null=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(SecModules, on_delete=models.SET_NULL, null=True)
    view_permission = models.BooleanField(null=True, blank=False)
    add_permission = models.BooleanField(null=True, blank=False)
    edit_permission = models.BooleanField(null=True, blank=False)
    delete_permission = models.BooleanField(null=True, blank=False)

    class Meta:
        verbose_name_plural = "Sec Role Modules"




class LoginHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    auth_token_key = models.CharField(max_length=256, null=True, blank=True)
    signin_time = models.DateTimeField(blank=True, null=True)
    signout_time = models.DateTimeField(blank=True, null=True)
    is_signed_in = models.BooleanField(null=True, blank=True)
    DEVICE_TYPES = (
        ("w", "web"),
        ("i", "ios"),
        ("a", "android"),
    )
    device_type = models.CharField(max_length=10, default='w', blank=True, null=True, choices=DEVICE_TYPES)
    device_token = models.CharField(max_length=256, blank=True, null=True)

