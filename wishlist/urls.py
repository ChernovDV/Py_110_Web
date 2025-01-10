from django.urls import path
from wishlist.views import wishlist_view, wishlist_add_json, wishlist_del_json

app_name = 'wishlist'

urlpatterns = [
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/api/add/<str:id_product>', wishlist_add_json),
    path('wishlist/api/del/<str:id_product>', wishlist_del_json, name = 'wish_list_del_json'),

]