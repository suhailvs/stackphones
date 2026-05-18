from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps import views as sitemaps_views
from django.contrib.sitemaps import Sitemap

from myapp import views

class PhoneSpecSitemap(Sitemap):
    limit = 2000
    def items(self):
        from myapp.models import PhoneSpec
        return PhoneSpec.objects.only('title','number','created_at') #.order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at
    
sitemaps = {'phones': PhoneSpecSitemap,}
urlpatterns = [
    path('',views.home),
    path('admin/', admin.site.urls),
    path('parse/', views.parse),
    path('download/', views.download_images),
    path("<slug:slug>-<int:n>/", views.PhoneDetail.as_view(), name="phone-detail"),
    path('sitemap.xml',sitemaps_views.index,{'sitemaps': sitemaps},name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml',sitemaps_views.sitemap,{'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
]
