from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
      path("register/", views.reg, name="register"),
 
    path('userhome',views.userhome,name='userhome'),
    path('footer',views.footer,name='footer'),
    path('login/',views.login,name='login'),
    path('reg',views.reg,name='reg'),
    path('contact',views.contact,name='contact'),
    path('About',views.About,name='About'),
    path('services',views.services,name='services'),
    path('contact_admin',views.contact_admin, name='contact_admin'),
    path('admindash/', views.admin_dashboard, name='admindash'),
    path('migrantreg', views.migrantreg, name='migrantreg'),
    path('registration_choice', views.registration_choice, name='registration_choice'),
    path('book_job', views.book_job, name='book_job'),
    path('success/', views.success_view, name='success'),
    path('index.html', views.index, name='index_html'),
    path('logout/', views.logout, name='logout'),
    path('agenthome/', views.agenthome, name='agenthome'),

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    

