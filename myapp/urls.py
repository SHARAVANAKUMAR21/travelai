# urls.py for the Skullcandy project

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # User authentication
    path('admin_login/', views.admin_login, name='admin_login'),
    path('user_login/', views.user_login, name='user_login'),
    path('user/register/', views.user_register, name='user_register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    

    # Admin features
    path('admin_add/', views.admin_add, name='admin_add'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('adminpageorder/', views.admin_order_view, name='adminorders'),
    path('adminordersiteam/<int:order_id>/', views.order_detail_view, name='order_detail'),

    # User features
    path('userpageorder/', views.user_order_view, name='orders'),
    path('index/', views.index, name='index'),
    
    # Product management
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),  # Ensure this exists
    path('products/category/<int:category_id>/', views.product_list, name='product_list_by_category'),
   
    # Cart and wishlist management
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('dec_from_cart/<int:product_id>/', views.decrease_to_cart, name='decrease_quantity'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),  
    path('order_summary/', views.order_summary_view, name='order_summary'),  
    
    # Wishlist management
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_to_wishlist/<int:product_id>/', views.remove_to_wishlist, name='remove_to_wishlist'),
    path('view_to_wishlist/', views.view_to_wishlist, name='view_to_wishlist'),

    # Profile and orders
    path('profile/update/', views.profile_update, name='profile_update'),
    path('update_status/<int:order_id>/', views.update_status, name='update_status'),
    path('order_list_and_detail/', views.order_list_and_detail, name='order_list_and_detail'),

    # Search functionality
    path('search/', views.search_view, name='search'),
    
    # Supplier features
    path('supplier_add/', views.supplier_add, name='supplier_add'),
    path('send_request/<int:product_id>/', views.send_request, name='send_request'),
    path('supplier/<int:id>/', views.supplier_replay, name='supplier_replay'),
    path('supplier_replies/', views.supplier_replies, name='supplier_replies'),  

    # Recommendations
    
    path('recommendation_form/', views.recommendation_form, name='recommendation_form'),
    path('generate_recommendation/', views.generate_recommendation, name='generate_recommendation'),
    
   

    # Welcome page
    # path('', views.welcome, name='welcome'),
    path('', views.welcome, name='welcome'),
    
    # Include Django's authentication URLs
    path('accounts/', include("django.contrib.auth.urls")),
    
    path('reoder/', views.reoder, name='reoder'),
    
    path('chat_home/', views.chat_home, name='chat_home'),
    
    
    path('dashboard/', views.dashboard, name='dashboard'),
        
        
        


    
    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
