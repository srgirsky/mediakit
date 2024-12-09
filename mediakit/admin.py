from django.contrib import admin
from django.utils.html import format_html
from .models import (
    MediaKit, 
    Tag, 
    SocialPlatform, 
    WorkWithMe, 
    BrandPartner, 
    Gallery
)

class SocialPlatformInline(admin.TabularInline):
    model = SocialPlatform
    extra = 1
    fields = (
        'platform', 
        'followers', 
        'engagement_rate', 
        'average_views'
    )

class WorkWithMeInline(admin.TabularInline):
    model = WorkWithMe
    extra = 1
    fields = (
        'platform', 
        'offering', 
        'price', 
        'number_of_deliverables'
    )

class BrandPartnerInline(admin.TabularInline):
    model = BrandPartner
    extra = 1
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.logo.url
            )
        return 'No logo'
    logo_preview.short_description = 'Logo Preview'

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.image.url
            )
        return 'No image'
    image_preview.short_description = 'Image Preview'

@admin.register(MediaKit)
class MediaKitAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'username', 
        'location', 
        'get_platform_count', 
        'get_brand_partner_count'
    )
    search_fields = ('name', 'username', 'location')
    list_filter = ('tags',)
    
    inlines = [
        SocialPlatformInline, 
        WorkWithMeInline, 
        BrandPartnerInline, 
        GalleryInline
    ]

    def get_platform_count(self, obj):
        return obj.social_platforms.count()
    get_platform_count.short_description = 'Platforms'

    def get_brand_partner_count(self, obj):
        return obj.brand_partners.count()
    get_brand_partner_count.short_description = 'Brand Partners'

@admin.register(SocialPlatform)
class SocialPlatformAdmin(admin.ModelAdmin):
    list_display = (
        'media_kit', 
        'platform', 
        'followers', 
        'engagement_rate', 
        'average_views'
    )
    list_filter = ('platform', 'media_kit')
    search_fields = ('media_kit__name', 'platform')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(WorkWithMe)
class WorkWithMeAdmin(admin.ModelAdmin):
    list_display = (
        'media_kit', 
        'platform', 
        'offering', 
        'price', 
        'number_of_deliverables'
    )
    list_filter = ('platform', 'media_kit')
    search_fields = ('media_kit__name', 'offering')

@admin.register(BrandPartner)
class BrandPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'media_kit', 'logo_preview')
    search_fields = ('name', 'media_kit__name')
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.logo.url
            )
        return 'No logo'
    logo_preview.short_description = 'Logo'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('media_kit', 'caption', 'image_preview')
    search_fields = ('media_kit__name', 'caption')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.image.url
            )
        return 'No image'
    image_preview.short_description = 'Image'