from django.contrib import admin
from .models import wall,Videos

# Register your models here.

class WallAdmin(admin.ModelAdmin):
    list_display=('id','title')
    list_display_links = ('id','title')
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 25

class VideosAdmin(admin.ModelAdmin):
    list_display=('id','title','wall','youtube')
    list_display_links = ('id','title','youtube')
    list_filter = ('title','youtube')
    search_fields = ('title','youtube')
    list_per_page = 25


admin.site.register(wall,WallAdmin)
admin.site.register(Videos,VideosAdmin)