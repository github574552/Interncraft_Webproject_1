from django.contrib import admin
from django.urls import path
from My_app import views  # Ensure My_app is the correct name of your app
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Redirect root URL to signup page
    path('', views.SignupPage, name='signup'),
    path('home/', views.HomePage, name='home'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.logout_view, name='logout'), 

    # Other URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('payment/execute/', views.payment_execute, name='payment_execute'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('test-paypal-api/', views.test_paypal_api, name='test_paypal_api'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('generate-order-slip/<int:order_id>/', views.generate_order_slip_pdf, name='generate_order_slip_pdf'),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
