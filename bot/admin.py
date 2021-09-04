from django.contrib import admin

from .models import VoiceMessage


@admin.register(VoiceMessage)
class VoiceMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name')
