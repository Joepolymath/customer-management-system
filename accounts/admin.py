from django.contrib import admin
from .models import *

admin.site.site_header = "CRM ADMIN SECTION"
admin.site.site_title = "Welcome to the Admin Section"
admin.site.index_title = "Welcome to the Admin Section"

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
