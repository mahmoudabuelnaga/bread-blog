from django.urls import path
from . import views
urlpatterns = [
    # path('',views.PostList.as_view() , name='post-list'),
    path('', views.post_list , name='post-list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail , name='post-detail'),
    path('<int:post_id>/share/', views.post_share , name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_list , name='post_detail_by_tag'),
    path('contact/' , views.contact_us, name='contact_us'),
    path('category/<slug:slug>/', views.category_detail , name='category_detail'),
    # path('category/<slug:slug>/',views.CategoryDetail.as_view() , name='category_detail'),
]