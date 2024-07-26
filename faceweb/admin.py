from django.contrib import admin
from .models import Vehicle, vehicle_login ,vehicle_logout
# from .models import MongoDBSnapshot
# from .admin import VehicleAdmin
# Register your models here.

class vechile_loginAdmin(admin.ModelAdmin): # we are declaring this to , view in admin panel , for admin
    # site_header = 'Vehicle login Area'
    list_display = ('text','timestamp','format','image_preview',)
    search_fields = ('text',)
    list_filter = ('timestamp',)
    def image_preview(self, obj):
        return obj.image_tag()

    image_preview.short_description = 'Image Preview'
admin.site.register(vehicle_login ,vechile_loginAdmin)

class vechile_logoutAdmin(admin.ModelAdmin): # we are declaring this to , view in admin panel , for admin
    # site_header = 'Vehicle login Area'
    list_display = ('text','timestamp','format','image_preview',)
    search_fields = ('text',)
    list_filter = ('timestamp',)
    def image_preview(self, obj):
        return obj.image_tag()

    image_preview.short_description = 'Image Preview'
admin.site.register(vehicle_logout ,vechile_logoutAdmin)
   
admin.site.index_title = "Parking Database"
admin.site.site_header = "Parking Admin Panel"
admin.site.site_title = "Parking lot system"

# ----------------------------------------------end of admin.py faceweb-------------------------------------------------------------   
# class vehicleloginAdmin(admin.ModelAdmin):
#     list_display = ('text','format')
# admin.site.register(vehicle_login , vehicleloginAdmin)



# text ='sometext that we can include'
# class PostAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('section1',{
#             'fields':('text','timestamp','format','image')
#         }),
#          ('section1',{
#             'fields':('text','timestamp','format','image')
#         }),
#     )