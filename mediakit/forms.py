# forms.py
from django import forms
from .models import MediaKit, SocialPlatform, WorkWithMe, BrandPartner, Gallery

class MediaKitForm(forms.ModelForm):
    class Meta:
        model = MediaKit
        fields = ['name', 'username', 'location', 'bio', 'profile_photo', 'banner_image']
        widgets = {
            'profile_photo': forms.FileInput(attrs={'show_clear_checkbox': False}),
            'banner_image': forms.FileInput(attrs={'show_clear_checkbox': False})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SocialPlatformForm(forms.ModelForm):
    class Meta:
        model = SocialPlatform
        fields = '__all__'  # Or list all fields explicitly
        exclude = ['media_kit']  # Exclude the foreign key field

class WorkWithMeForm(forms.ModelForm):
    class Meta:
        model = WorkWithMe
        fields = ['platform', 'offering', 'service_description', 'price', 
                  'number_of_deliverables', 'length_of_deliverables', 'cta_button']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields optional if needed
        self.fields['cta_button'].required = False
        # Add any other field customizations here

class BrandPartnerForm(forms.ModelForm):
    class Meta:
        model = BrandPartner
        fields = ['name', 'logo', 'integration_url']
        widgets = {
            'logo': forms.FileInput(attrs={'show_clear_checkbox': False})
        }

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['platform', 'example_url', 'video_priority']
        exclude = ['media_kit', 'image', 'caption']
        widgets = {
            'video_priority': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video_priority'].required = False  # Make it optional if needed

