from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Directory, Folder

class FolderInline(admin.StackedInline):
    model = Folder
    extra = 1

class DirectoryAdmin(admin.ModelAdmin):
    inlines = [FolderInline]

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'directory', 'picture',)
    list_filter = ('directory',)
    search_fields = ('name', 'directory__path',)
    readonly_fields = ('picture',)

admin.site.register(Directory, DirectoryAdmin)
admin.site.register(Folder, FolderAdmin)
