"""notebook URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from note import views as note_view
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^submitartical/', note_view.submitartical),
    url(r'^editartical/', note_view.editartical),
    url(r'^login/', note_view.login),
    url(r'^logout/', note_view.logout),
    url(r'^getartical/', note_view.getartical),
    url(r'^getarticallist/', note_view.getarticallist),
    url(r'^register/', note_view.register),
    url(r'^chkls/', note_view.CheckLogin),
    url(r'^deleteartical/', note_view.deleteartical),
    url(r'^search/', note_view.searchartical),
    url(r'^changepassword/', note_view.ChangePassword),
    url(r'^resetpassword/', note_view.ReSetPassword),
    url(r'^([\s|\S]+?)/$', note_view.getartical),
    url(r'^$', note_view.index),
]
