"""testnewslab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', 'hellonewslab.views.front'),
    url(r'^test/$', 'hellonewslab.views.test'),
    url(r"^contact/$", "hellonewslab.views.contact"),
    
    # vote
    url(r"^sudogwon413/$", "votenewslab.views.vote_home"),
    url(r"^sudogwon413/([, \w \[\]\.]+)/$", "votenewslab.views.vote_result"),


    # nin2-calc
    url(r'^calc/$', 'nin2newslab.views.calc_home'),
    
    # nin2-choice-all
    #url(r'^ninx2/([\w \[\]\.]+)/home/$', 'nin2newslab.views.choice_home'),
    #url(r'^ninx2/([\w \[\]\.]+)/([\d]+)/$', 'nin2newslab.views.choice_nump'),
    #url(r'^ninx2/([\w \[\]\.]+)/result/([\d]+)/$', 'nin2newslab.views.choice_result'),
    
    # nin2-choice-tuition
    url(r'^ninx2/(tuition)/home/$', 'nin2newslab.views.choice_home'),
    url(r'^ninx2/(tuition)/([\d]+)/$', 'nin2newslab.views.choice_nump'),
    url(r'^ninx2/(tuition)/result/([\d]+)/$', 'nin2newslab.views.choice_result'),

    # nin2-network
    url(r'^albawords/network/$', 'nin2newslab.views.network_web'),
    url(r"^albawords/network/mobile/$", "nin2newslab.views.network_mobile"),   

    # media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
]
