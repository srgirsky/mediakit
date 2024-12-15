from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.forms import modelformset_factory
from django.views.decorators.http import require_http_methods
from .models import MediaKit, SocialPlatform, WorkWithMe, BrandPartner, Gallery, Tag
from .forms import MediaKitForm, SocialPlatformForm, WorkWithMeForm, BrandPartnerForm, GalleryForm
import json

# Define the formsets at the top
WorkWithMeFormSet = modelformset_factory(
    WorkWithMe, 
    form=WorkWithMeForm,
    can_delete=True,
    extra=1
)

SocialPlatformFormSet = modelformset_factory(
    SocialPlatform,
    form=SocialPlatformForm,
    can_delete=True,
    extra=1
)

GalleryFormSet = modelformset_factory(
    Gallery,
    form=GalleryForm,
    can_delete=True,
    extra=1,
    fields=['platform', 'example_url', 'video_priority']
)

BrandPartnerFormSet = modelformset_factory(
    BrandPartner,
    fields=['name', 'logo', 'integration_url'],
    extra=1,
    can_delete=True
)

def home(request):
    creators = MediaKit.objects.all()
    return render(request, 'mediakit/home.html', {'creators': creators})


def media_kit_detail(request, media_kit_id):
    media_kit = get_object_or_404(MediaKit, id=media_kit_id)
    
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
        'social_platforms': social_platforms,
    }
    
    return render(request, 'mediakit/media_kit_detail2.html', context)


def media_kit_detail_by_slug(request, url_slug):
    media_kit = get_object_or_404(MediaKit, url_slug=url_slug)
    
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
        'social_platforms': social_platforms,
    }
    
    return render(request, 'mediakit/media_kit_detail2.html', context)


@require_http_methods(["POST"])
def create_tag(request):
    try:
        data = json.loads(request.body)
        tag_name = data.get('tag_name', '').strip()
        
        if not tag_name:
            return JsonResponse({'success': False, 'error': 'Tag name is required'})
            
        # Convert to title case before saving
        tag_name = tag_name.title()
        
        # Try to get existing tag or create new one
        tag, created = Tag.objects.get_or_create(name=tag_name.lower())
        
        return JsonResponse({
            'success': True,
            'tag_id': tag.id,
            'tag_name': tag.name  # This will be properly capitalized
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def edit_media_kit(request, media_kit_id):
    media_kit = get_object_or_404(MediaKit, id=media_kit_id)
    
    # Add this debug print
    print(f"Current tags: {[tag.name for tag in media_kit.tags.all()]}")
    
    # Initialize all forms/formsets at the start
    media_kit_form = MediaKitForm(instance=media_kit)
    work_with_me_formset = WorkWithMeFormSet(
        queryset=WorkWithMe.objects.filter(media_kit=media_kit),
        prefix='work_with_me'
    )
    social_platform_formset = SocialPlatformFormSet(
        queryset=SocialPlatform.objects.filter(media_kit=media_kit),
        prefix='social_platform'
    )
    gallery_formset = GalleryFormSet(
        queryset=Gallery.objects.filter(media_kit=media_kit),
        prefix='gallery'
    )
    brand_partner_formset = BrandPartnerFormSet(
        queryset=BrandPartner.objects.filter(media_kit=media_kit),
        prefix='brand_partners'
    )
    
    if request.method == 'POST':
        section = request.POST.get('section')
        
        if section == 'profile':
            try:
                media_kit_form = MediaKitForm(request.POST, request.FILES, instance=media_kit)
                if media_kit_form.is_valid():
                    # Save the form without committing
                    media_kit = media_kit_form.save(commit=False)
                    media_kit.save()
                    
                    # Handle tags separately from the form
                    tags_str = request.POST.get('tags', '')
                    if tags_str:
                        try:
                            tag_ids = [int(tid) for tid in tags_str.split(',') if tid.strip()]
                            media_kit.tags.clear()
                            media_kit.tags.set(tag_ids)
                        except ValueError as e:
                            print(f"Error processing tag IDs: {e}")
                    else:
                        media_kit.tags.clear()
                    
                    return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid form data'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
                
        elif section == 'social_platforms':
            social_platform_formset = SocialPlatformFormSet(
                request.POST,
                queryset=SocialPlatform.objects.filter(media_kit=media_kit),
                prefix='social_platform'
            )
            if social_platform_formset.is_valid():
                for form in social_platform_formset:
                    if form.is_valid():
                        if form.cleaned_data.get('DELETE'):
                            if form.instance.pk:
                                form.instance.delete()
                        else:
                            instance = form.save(commit=False)
                            instance.media_kit = media_kit
                            instance.save()
                return JsonResponse({'success': True, 'message': 'Social platforms updated successfully'})
            return JsonResponse({'success': False, 'error': 'Invalid form data'})
                
        elif section == 'work_with_me':
            # Check if this is a deletion operation
            is_deletion = request.POST.get('is_deletion') == 'true'
            
            work_with_me_formset = WorkWithMeFormSet(
                request.POST,
                queryset=WorkWithMe.objects.filter(media_kit=media_kit),
                prefix='work_with_me'
            )

            if is_deletion:
                # For deletions, we only care about processing the DELETE fields
                for form in work_with_me_formset.forms:
                    if form.instance.pk and form.data.get(f'{form.prefix}-DELETE'):
                        form.instance.delete()
                return JsonResponse({'success': True, 'message': 'Offering deleted successfully'})
            
            # Regular form processing for non-deletion operations
            if work_with_me_formset.is_valid():
                instances = work_with_me_formset.save(commit=False)
                for instance in instances:
                    instance.media_kit = media_kit
                    instance.save()
                # Handle deletions
                for obj in work_with_me_formset.deleted_objects:
                    obj.delete()
                return JsonResponse({'success': True, 'message': 'Work with me section updated successfully'})
            else:
                # Filter out errors from empty forms
                real_errors = []
                for form in work_with_me_formset.forms:
                    if any(field.data for field in form.visible_fields()):
                        if form.errors:
                            real_errors.append(form.errors)
                
                print("Form errors:", real_errors)
                return JsonResponse({
                    'success': False, 
                    'error': 'Please fill in all required fields',
                    'form_errors': real_errors
                })
                
        elif section == 'gallery':
            gallery_formset = GalleryFormSet(
                request.POST,
                queryset=Gallery.objects.filter(media_kit=media_kit),
                prefix='gallery'
            )
            
            # Check if this is a deletion request
            is_deletion = any(
                key.endswith('-DELETE') and value == 'on'
                for key, value in request.POST.items()
            )
            
            if is_deletion:
                try:
                    # Get the ID of the item to delete
                    for key, value in request.POST.items():
                        if key.endswith('-id') and value:
                            gallery_id = value
                            gallery_item = Gallery.objects.get(id=gallery_id)
                            gallery_item.delete()
                            return JsonResponse({'success': True, 'message': 'Gallery item deleted successfully'})
                    return JsonResponse({'success': False, 'error': 'Item not found'})
                except Gallery.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Gallery item not found'})
                except Exception as e:
                    print(f"Error during deletion: {e}")
                    return JsonResponse({'success': False, 'error': str(e)})
            
            # Regular form processing
            if gallery_formset.is_valid():
                try:
                    # Get existing items to check for deletions
                    existing_items = set(Gallery.objects.filter(media_kit=media_kit).values_list('id', flat=True))
                    submitted_items = set()
                    
                    for form in gallery_formset.forms:
                        if form.cleaned_data:
                            # Skip if marked for deletion
                            if form.cleaned_data.get('DELETE'):
                                continue
                            
                            # Only process if we have the required fields
                            if form.cleaned_data.get('platform') and form.cleaned_data.get('example_url'):
                                instance = form.save(commit=False)
                                instance.media_kit = media_kit
                                instance.save()
                                if instance.id:
                                    submitted_items.add(instance.id)
                    
                    # Don't delete items that weren't in the form
                    # items_to_delete = existing_items - submitted_items
                    # Gallery.objects.filter(id__in=items_to_delete).delete()
                    
                    return JsonResponse({'success': True, 'message': 'Gallery updated successfully'})
                except Exception as e:
                    print(f"Error saving gallery: {e}")
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                print("Gallery formset errors:", gallery_formset.errors)
                return JsonResponse({
                    'success': False, 
                    'error': 'Please fill in all required fields',
                    'form_errors': gallery_formset.errors,
                    'non_form_errors': gallery_formset.non_form_errors()
                })
                
        elif section == 'brand_partners':
            formset = BrandPartnerFormSet(
                request.POST,
                request.FILES,
                prefix='brand_partners',
                queryset=BrandPartner.objects.filter(media_kit=media_kit)
            )
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.media_kit = media_kit
                    instance.save()
                formset.save_m2m()
                # Handle deletions
                for obj in formset.deleted_objects:
                    obj.delete()
                return JsonResponse({'success': True, 'message': 'Brand partners updated successfully'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid form data'})

    return render(request, 'mediakit/edit_media_kit.html', {
        'media_kit': media_kit,
        'media_kit_form': media_kit_form,
        'work_with_me_formset': work_with_me_formset,
        'social_platform_formset': social_platform_formset,
        'gallery_formset': gallery_formset,
        'brand_partner_formset': brand_partner_formset,
    })