"""mytrail1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,re_path
from . import views

app_name = 'sanskritannotator'

urlpatterns = [
    path('',views.index,name='index'),
    # path('wordtable/',views.ZeroConfigurationDatatableView.as_view(),name='wordtableview'),
    path('wordtable/',views.wordtableview,name='wordtableview'),
    path('linetable/',views.sentenceview,name='sentenceview'),
    path('wordsinsentencetable/',views.wordsinsentenceview,name='wordsinsentenceview'),
    path('presentdata/',views.presentdataview,name='presentdataview'),
    re_path(r'select/(?P<sent_id>[0-9]+)/(?P<wordoption_id>[0-9]+)/$', views.select_wordoptionview, name='select_wordoption'),
    re_path(r'eliminate/(?P<sent_id>[0-9]+)/(?P<wordoption_id>[0-9]+)/$', views.eliminate_wordoptionview, name='eliminate_wordoption'),
    re_path(r'refresh/(?P<sent_id>[0-9]+)/$', views.reset_allselectionview, name='reset_allselection'), 
    path("presentdata/ajax/save_data/",views.save_dragdata,name='save_dragdata'),
    path("presentdata/ajax/get_data/",views.get_dragdata,name='get_dragdata'),
    ]
