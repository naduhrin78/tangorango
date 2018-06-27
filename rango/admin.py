from django.contrib import admin
from rango.models import Category, Page, UserProfile
from django.utils.html import format_html
# Register your models here.

class TableLayout(admin.ModelAdmin):
    list_display = ('category', 'title', 'url', 'change_button', 'delete_button')

    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/my_app/my_model/{}/change/">Change</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/my_app/my_model/{}/delete/">Delete</a>', obj.id)

admin.site.register(Category)
admin.site.register(Page, TableLayout)
admin.site.register(UserProfile)