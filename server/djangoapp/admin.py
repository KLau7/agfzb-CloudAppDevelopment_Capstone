from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel
    search_fields = ['car_make']
    extra = 3

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    search_fields = ['car_make', 'name', 'type', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'description']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)