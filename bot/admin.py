from django.contrib import admin

from .models import VoiceMessage, Sticker


@admin.register(VoiceMessage)
class VoiceMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name')


@admin.register(Sticker)
class VoiceMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name')
