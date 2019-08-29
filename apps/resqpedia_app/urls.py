from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^resqpedia/myaccount$', views.show_user_info),
    url(r'^resqpedia/myaccount/{user_id}/edit$', views.edit_user),
    url(r'^resqpedia$', views.all_recipes),
    url(r'^resqpedia/addrecipe$', views.add_recipe),
    url(r'^resqpedia/recipe/<recipe_id>$', views.show_individual_recipe),
    url(r'^resqpedia/recipe/<recipe_id>/edit$', views.edit_recipe),
    url(r'^resqpedia/recipe/<recipe_id>/delete$', views.delete_recipe),
    url(r'^resqpedia/recipe/add_message$', views.add_message),
    url(r'^resqpedia/recipe/edit_message/<message_id>$', views.edit_message),
    url(r'^resqpedia/recipe/delete/<message_id>$', views.delete_message),
    url(r'^resqpedia/recipe/<message_id>/add_comment$', views.add_comment),
    url(r'^resqpedia/recipe/edit_comment/<comment_id>$', views.edit_message),
    url(r'^resqpedia/recipe/delete/<comment_id>$', views.delete_message),
]