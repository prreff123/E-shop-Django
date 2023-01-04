from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .middleware.auth import auth_middleware

urlpatterns = [
    path('',views.Index.as_view(),name="index"),
    path('signup',views.signup, name="signup"),
    path('login',views.Login.as_view(), name="login"),
    path('logout',views.logout, name="logout"),
    path('order',auth_middleware(views.OrderView.as_view()), name="order"),
    path('cart',views.Cart.as_view(), name="cart"),
    path('check-out',views.CheckOut.as_view(), name="checkout"),
    path('pay',views.pay,name="pay"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
