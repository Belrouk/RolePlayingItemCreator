from django.conf.urls import url
from .views import home_view, create_item_view, edit_item_view
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^collection/$', home_view, name='item_viewer'),
    url(r'^creator/$', create_item_view, name='create_item'),
    url(r'^edit/(?P<id>[\d]+)/$', edit_item_view, name='item_editor'),
]
