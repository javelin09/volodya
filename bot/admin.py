from django.contrib import admin

from .models import VoiceMessage, Sticker, SwearWord, HolidayGreeting


@admin.register(VoiceMessage)
class VoiceMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name')


@admin.register(Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name')


@admin.register(SwearWord)
class SwearWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word')


@admin.register(HolidayGreeting)
class HolidayGreetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'holiday', 'send_on')
