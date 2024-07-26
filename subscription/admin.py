from django.contrib import admin
from .models import Subscription , DailyPass

# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin): # declaring the subscription data to the admin panel for admin 
    list_display = ('id', 'user_id', 'first_name', 'email', 'username','company_name','is_active','subscription_id',)
    search_fields = ('first_name', 'company_name' ,'email', 'user_id', )
    list_filter = ('subscription_id', 'user_id',)
admin.site.register(Subscription , SubscriptionAdmin)  

class DailyPassAdmin(admin.ModelAdmin):
    list_display = ('id','pass_code' , 'valid_from' , 'valid_to','num_people','company', 'reference_name',)
    list_filter = ('valid_from', 'company' ,'reference_name',)
    search_fields = ('company' ,'reference_name', )

admin.site.register(DailyPass , DailyPassAdmin)
    


    




# --------------------------------end of admin.py Subscription---------------------------------------------------------------