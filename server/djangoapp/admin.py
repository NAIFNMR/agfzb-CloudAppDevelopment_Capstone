from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name','dealer_id','year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    extra = 1
    list_display = ['name','description']

# Register models here
admin.site.register(CarModel,CarModelAdmin)
admin.site.register(CarMake,CarMakeAdmin)