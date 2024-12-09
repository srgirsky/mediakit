from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import MediaKit, SocialPlatform, WorkWithMe, BrandPartner, Gallery
from .forms import MediaKitForm, SocialPlatformForm, WorkWithMeForm, BrandPartnerForm, GalleryForm
from django.forms import modelformset_factory


# Create your views here.
def home(request):
    creators = MediaKit.objects.all()
    return render(request, 'mediakit/home.html', {'creators': creators})


def media_kit_detail(request, media_kit_id):
    media_kit = MediaKit.objects.get(id=media_kit_id)
    
    # Calculate total followers
    total_followers = sum(platform.followers for platform in media_kit.social_platforms.all())
    
    # Get all work offerings for this media kit
    work_with_me = media_kit.work_with_me.all()
    
    # Get unique platforms using a distinct approach
    unique_platforms = work_with_me.values('platform').distinct()

    # Prepare the URLs for each platform
    social_platforms = []
    for platform in media_kit.social_platforms.all():
        urls = [platform.example_url_1, platform.example_url_2, platform.example_url_3]
        social_platforms.append({
            'platform': platform,
            'urls': [url for url in urls if url]  # Filter out None or empty URLs
        })
    
    context = {
        'media_kit': media_kit,
        'work_with_me': work_with_me,
        'total_followers': total_followers,
        'unique_platforms': unique_platforms,
        'social_platforms': social_platforms,  # Pass the social_platforms list
    }
    
    return render(request, 'mediakit/media_kit_detail2.html', context)




def edit_media_kit(request, media_kit_id):
    media_kit = get_object_or_404(MediaKit, pk=media_kit_id)
    
    # Create formset classes
    SocialPlatformFormSet = modelformset_factory(SocialPlatform, form=SocialPlatformForm, extra=1)
    WorkWithMeFormSet = modelformset_factory(WorkWithMe, form=WorkWithMeForm, extra=1)
    GalleryFormSet = modelformset_factory(Gallery, form=GalleryForm, extra=1)
    
    if request.method == 'POST':
        # Create forms with POST data
        media_kit_form = MediaKitForm(request.POST, request.FILES, instance=media_kit)
        
        # Pass the correct queryset when creating formsets with POST data
        social_platform_formset = SocialPlatformFormSet(
            request.POST, 
            request.FILES, 
            queryset=media_kit.social_platforms.all()
        )
        work_with_me_formset = WorkWithMeFormSet(
            request.POST, 
            queryset=media_kit.work_with_me.all()
        )
        gallery_formset = GalleryFormSet(
            request.POST, 
            request.FILES, 
            queryset=media_kit.gallery.all()
        )
        
        if media_kit_form.is_valid():
            # Save the media kit first
            media_kit_instance = media_kit_form.save()
            
            # For formsets, you might want to set the media_kit for each instance
            if social_platform_formset.is_valid():
                social_platforms = social_platform_formset.save(commit=False)
                for platform in social_platforms:
                    platform.media_kit = media_kit_instance
                    platform.save()
            
            if work_with_me_formset.is_valid():
                work_with_me_instances = work_with_me_formset.save(commit=False)
                for work_option in work_with_me_instances:
                    work_option.media_kit = media_kit_instance
                    work_option.save()
            
            if gallery_formset.is_valid():
                gallery_instances = gallery_formset.save(commit=False)
                for gallery_item in gallery_instances:
                    gallery_item.media_kit = media_kit_instance
                    gallery_item.save()
            
            return redirect('media_kit_detail', media_kit_id=media_kit.id)
    else:
        # Initial GET request
        media_kit_form = MediaKitForm(instance=media_kit)
        social_platform_formset = SocialPlatformFormSet(queryset=media_kit.social_platforms.all())
        work_with_me_formset = WorkWithMeFormSet(queryset=media_kit.work_with_me.all())
        gallery_formset = GalleryFormSet(queryset=media_kit.gallery.all())
    
    return render(request, 'mediakit/edit_media_kit.html', {
        'media_kit_form': media_kit_form,
        'social_platform_formset': social_platform_formset,
        'work_with_me_formset': work_with_me_formset,
        'gallery_formset': gallery_formset,
    })
