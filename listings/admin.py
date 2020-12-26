from django.contrib import admin
from .models import Listing
# Register your models here.


class q(admin.ModelAdmin):
    list_display=('id','title','owner','category','price','is_published','last_date')
    list_display_links=('id','title')
    list_filter=('category','is_published')
    list_per_page=30
    search_fields=('title','price','description','address','city','state','zipcode',)


admin.site.register(Listing,q)