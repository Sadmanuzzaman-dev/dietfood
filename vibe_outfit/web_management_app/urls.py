from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    # path('', home, name='home'),

    path('api/navigation/', NavigationViewSet.as_view(), name='navigation'),
    path('api/hero-section/', HeroSectionViewSet.as_view(), name='hero_section'),

    path('api/categories/', CategoryAPIView.as_view(), name='category-list'),
    path('api/categories/all/',CategoryWithChildrenAPIView.as_view(),name='category-with-children'),
    path('api/categories/<slug:slug>/products/', CategoryProductListAPIView.as_view()),
    path('api/products/featured/', FeaturedProductAPIView.as_view()),
    path('api/products/new-arrivals/', NewArrivalProductAPIView.as_view()),
    path('api/products/<slug:slug>/', ProductDetailsAPIView.as_view()),
    
    path('api/cart/add/', AddToCartAPIView.as_view()),
    path('api/cart/', CartListAPIView.as_view()),
    path('api/cart_item/<int:pk>/', UpdateCartItemAPIView.as_view()),
    path('api/cart_item/<int:pk>/delete/', RemoveCartItemAPIView.as_view()),
]


# icon, image admin e preview dekhanor jonno
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)