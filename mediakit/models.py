from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class MediaKit(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    url_slug = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-z0-9-]+$',
                message='URL slug must contain only lowercase letters, numbers, and hyphens',
                code='invalid_url_slug'
            )
        ]
    )
    show_offering_price = models.BooleanField(default=True)
    show_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.url_slug:
            return reverse('media_kit_detail_by_slug', kwargs={'url_slug': self.url_slug})
        return reverse('media_kit_detail', kwargs={'media_kit_id': self.id})

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.url_slug:
            self.url_slug = slugify(self.name)
        # Ensure slug is properly formatted
        self.url_slug = slugify(self.url_slug)
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        # Capitalize first letter of each word
        self.name = self.name.title()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class SocialPlatform(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
        ('twitch', 'Twitch'),
        ('linkedin', 'LinkedIn'),
        ('facebook', 'Facebook'),
        ('other', 'Other'),
    ]
    
    media_kit = models.ForeignKey(MediaKit, on_delete=models.CASCADE, related_name='social_platforms')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    
    # Platform Stats
    followers = models.IntegerField(default=0)
    engagement_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    average_views = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        default=0
    )
    
    # Audience Demographics
    male_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    female_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    
    # Age Distribution
    age_18_34_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    age_35_44_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    age_45_54_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    age_55_64_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    age_65_plus_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    
    # Top Countries
    top_country_1 = models.CharField(max_length=100, null=True, blank=True)
    top_country_1_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    top_country_2 = models.CharField(max_length=100, null=True, blank=True)
    top_country_2_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    top_country_3 = models.CharField(max_length=100, null=True, blank=True)
    top_country_3_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )

    example_url_1 = models.URLField(max_length=200, blank=True, null=True)
    example_url_2 = models.URLField(max_length=200, blank=True, null=True)
    example_url_3 = models.URLField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"{self.media_kit.name} - {self.get_platform_display()}"

class WorkWithMe(models.Model):
    media_kit = models.ForeignKey(MediaKit, on_delete=models.CASCADE, related_name='work_with_me')
    platform = models.CharField(max_length=50)  # e.g., "Instagram"
    offering = models.CharField(max_length=150)
    service_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_deliverables = models.IntegerField(default=1)
    length_of_deliverables = models.IntegerField(default=30)
    cta_button = models.CharField(max_length=50, default="Book now")
    
    def __str__(self):
        return f"{self.media_kit.name} - {self.platform} Offering"

class BrandPartner(models.Model):
    media_kit = models.ForeignKey(MediaKit, on_delete=models.CASCADE, related_name='brand_partners')
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    integration_url = models.URLField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Gallery(models.Model):
    media_kit = models.ForeignKey(MediaKit, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='gallery/',blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True, null=True)
    example_url = models.URLField(max_length=200, blank=True, null=True)
    platform = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Instagram"
    video_priority = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.media_kit.name} Gallery Image"
