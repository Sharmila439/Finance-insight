from django.contrib import admin
from .models import Lesson
from embed_video.admin import AdminVideoMixin
# Register your models here.
class LessonAdmin(AdminVideoMixin,admin.ModelAdmin):
    list_display = ('title', 'published_date', 'video')
    search_fields = ('title',)
    list_filter = ('published_date',)

admin.site.register(Lesson, LessonAdmin)