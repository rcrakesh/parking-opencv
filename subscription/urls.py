# subscriptions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_subscription, name='create_subscription'),
    path('generateqr/', views.generate_qrcode, name='generate_qrcode'),
    path('generateqrpass/', views.generate_qrcode_dailypass, name='generate_qrcode_dailypass'),
    path('video_feed2/', views.video_feed2, name ="video_feed2"),
    path('video_feed3', views.video_feed3, name ="video_feed3"),
    path('verify_sub', views.verify_sub, name='verify_sub'),
    path('Dpass', views.Dpass, name='Dpass'),
    # path('verify/', views.verify_subscription, name='verify_subscription'),
    # path('ver/', views.verify_sub, name='verify_sub'),
     # Example URL pattern for 'ver/'
    # path('ver/video_feed2', views.video_feed2, name='video_feed2'),
    #  path('detect', views.generate_video_feed, name='generate_video_feed'),
    #  path('gen/', views.qr_code_scanner_view, name='generate_qr_code'),
   

]
# ]path('save/', views.save_qr_code_view, name='save_qr_code_view'),


# ignore this just , adding the code link to this 

# -------------------------------end of urls.py subscription------------------------------------------------------------------