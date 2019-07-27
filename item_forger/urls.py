from django.conf.urls import url
from .views import view_collection, create_item_view, edit_item_view
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r"^collection/$", view_collection, name="item_collection"),
    url(r"^creator/$", create_item_view, name="forge_item"),
    url(r"^edit/(?P<id>[\d]+)/$", edit_item_view, name="edit_item"),
]
