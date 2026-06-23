from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Info
    surname = models.CharField(max_length=50, default="")
    first_name = models.CharField(max_length=50, default="")
    middle_name = models.CharField(max_length=50, default="")
    name_extension = models.CharField(max_length=10, blank=True, default="")
    age = models.CharField(max_length=5, default="")
    dob = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, default="")
    SEX_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='Male')
    CIVIL_STATUS_CHOICES = [
        ('Single', 'Single'), ('Married', 'Married'),
        ('Widowed', 'Widowed'), ('Separated', 'Separated'),
    ]
    civil_status = models.CharField(max_length=20, choices=CIVIL_STATUS_CHOICES, default='Single')
    height = models.CharField(max_length=10, default="")
    weight = models.CharField(max_length=10, default="")
    BLOOD_TYPE_CHOICES = [
        ('', ''), ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'),
        ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES, default='N/A')
    CITIZENSHIP_CHOICES = [('Filipino', 'Filipino'), ('Dual Citizen', 'Dual Citizen'), ('Other', 'Other')]
    citizenship = models.CharField(max_length=50, choices=CITIZENSHIP_CHOICES, default='Filipino')

    # Residential Address
    res_house_no = models.CharField(max_length=50, default="")
    res_street = models.CharField(max_length=100, default="")
    res_subdivision = models.CharField(max_length=100, default="")
    res_barangay = models.CharField(max_length=100, default="")
    res_barangay_name = models.CharField(max_length=100, default="")  # ← NEW
    res_city = models.CharField(max_length=100, default="")
    res_city_name = models.CharField(max_length=100, default="")      # ← NEW
    res_province = models.CharField(max_length=100, default="")
    res_province_name = models.CharField(max_length=100, default="")  # ← NEW
    res_zip = models.CharField(max_length=10, default="")

    # Permanent Address
    same_as_residential = models.BooleanField(default=False)
    per_house_no = models.CharField(max_length=50, default="")
    per_street = models.CharField(max_length=100, default="")
    per_subdivision = models.CharField(max_length=100, default="")
    per_barangay = models.CharField(max_length=100, default="")
    per_barangay_name = models.CharField(max_length=100, default="")  # ← NEW
    per_city = models.CharField(max_length=100, default="")
    per_city_name = models.CharField(max_length=100, default="")      # ← NEW
    per_province = models.CharField(max_length=100, default="")
    per_province_name = models.CharField(max_length=100, default="")  # ← NEW
    per_zip = models.CharField(max_length=10, default="")

    # Contact
    telephone = models.CharField(max_length=20, default="N/A")
    mobile_number = models.CharField(max_length=20, default="N/A")
    email_address = models.CharField(max_length=100, default="")

    # Government IDs
    agency_employee_no = models.CharField(max_length=50, default="N/A")

    # Emergency Contact
    emergency_name = models.CharField(max_length=100, default="")
    emergency_relationship = models.CharField(max_length=50, default="")
    emergency_phone = models.CharField(max_length=20, default="")
    emergency_address = models.TextField(default="")

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Education(models.Model):
    LEVEL_CHOICES = [
        ('Elementary', 'Elementary'),
        ('Secondary', 'Secondary'),
        ('College', 'College'),
        ('Vocational', 'Vocational'),
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    school_name = models.CharField(max_length=200, default="")
    degree = models.CharField(max_length=200, default="")
    year_graduated = models.CharField(max_length=10, default="")

    def __str__(self):
        return f"{self.level} - {self.school_name}"


class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='work_experiences')
    company = models.CharField(max_length=200, default="")
    position = models.CharField(max_length=200, default="")
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.position} at {self.company}"


class Skill(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CivilServiceEligibility(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='eligibilities')
    career_service = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, default="N/A")
    valid_until = models.DateField(null=True, blank=True)


class TrainingProgram(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='trainings')
    title = models.CharField(max_length=200)
    dates = models.CharField(max_length=50)
    hours = models.IntegerField(default=0)
    conducted_by = models.CharField(max_length=200)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='post_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class PersonalDataSheet(models.Model):
    province_code     = models.CharField(max_length=10, blank=True)
    province_name     = models.CharField(max_length=100, blank=True)
    municipality_code = models.CharField(max_length=10, blank=True)
    municipality_name = models.CharField(max_length=100, blank=True)
    barangay_code     = models.CharField(max_length=10, blank=True)
    barangay_name     = models.CharField(max_length=100, blank=True)
    zip_code          = models.CharField(max_length=4,  blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()