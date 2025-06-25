from .views import shop_view, buy_item_view, purchase_item, add_item_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from users.views import purchase_history


urlpatterns=[
    path('shop/', shop_view, name='shop'),
    path('shop/buy/<int:item_id>/', buy_item_view, name='buy_item'),
    path('shop/purchase/<int:item_id>/', purchase_item, name='purchase_item'), 
    path('shop/purchases/', purchase_history, name='purchase_history'),  
    path('purchase/<int:item_id>/', purchase_item, name='purchase_item'),
    path('purchase-history/',purchase_history, name='purchase_history'),
    path('add-item/', add_item_view, name='add_item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

