from django.contrib import admin

from contact import models


# Register your models here.
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone']
    search_fields = ['id', 'first_name']
    ordering = ['-id']
    list_per_page = 10
    list_max_show_all = 240
    list_display_links = ['id', 'phone']
    list_editable = ['first_name']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['-id']
