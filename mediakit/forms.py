# forms.py
from django import forms
from .models import MediaKit, SocialPlatform, WorkWithMe, BrandPartner, Gallery

class MediaKitForm(forms.ModelForm):
    class Meta:
        model = MediaKit
        fields = ['name', 'username', 'location', 'bio', 'profile_photo', 'banner_image', 'tags']

class SocialPlatformForm(forms.ModelForm):
    class Meta:
        model = SocialPlatform
        fields = ['platform', 'followers', 'engagement_rate', 'average_views', 
                  'male_percentage', 'female_percentage', 'age_18_34_percentage', 
                  'age_35_44_percentage', 'age_45_54_percentage', 'age_55_64_percentage', 
                  'age_65_plus_percentage', 'top_country_1', 'top_country_1_percentage', 
                  'top_country_2', 'top_country_2_percentage', 'top_country_3', 
                  'top_country_3_percentage', 'example_url_1', 'example_url_2', 'example_url_3']

class WorkWithMeForm(forms.ModelForm):
    class Meta:
        model = WorkWithMe
        fields = ['platform', 'offering', 'service_description', 'price', 
                  'number_of_deliverables', 'length_of_deliverables', 'cta_button']

class BrandPartnerForm(forms.ModelForm):
    class Meta:
        model = BrandPartner
        fields = ['name', 'logo', 'integration_url']

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image', 'caption', 'example_url']

