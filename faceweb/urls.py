from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('index', views.index, name='index'),
    path('indexlogout', views.indexlogout, name='indexlogout'),
    path('1', views.hello , name='hello'),
    # path('sensi', views.sensi , name='sensi'),
    # path('admin1', views.home_view, name='admin1'),
    
    path('register', views.register , name='register'),
    path('login/', views.login, name="login"),
    path('loginadmin', views.loginadmin, name="loginadmin"),
    path('admin1', views.admin1, name="admin1"),
    path('logout', views.logout, name="logout"),
    path('logoutadmin', views.logoutadmin, name="logoutadmin"),
    path('details',views.details,name='details'),
    path('dailypass',views.dailypass,name='dailypass'),
    path('upload/', views.upload_vehicle, name='upload_vehicle'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('capture/', views.capture_snapshot, name='capture_snapshot'),
    path('video_feed1/', views.video_feed1, name='video_feed1'),
   
    path('capturelogout/', views.capture_snapshot_logout, name='capture_snapshot_logout'),
    # path('generate_qrcode/', views.generate_qrcode, name='generate_qrcode'),
    # path('vehicle',views.vehicle,name='vehicle'),
    # path('access-control/', views.access_control, name='access_control'),
    # path('scan_qr/', views.scan_qr_code, name='scan_qr_code'),
    # path('save_image_to_db/',views.save_image_to_db, name ='save_image_to_db'),
] 

# ignore this... its just declaring the codes 