from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView, Response
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import (
    CompanyLogo,
    NavOption,
    NavButtons,
    HeroSection,
    ProductCategory,
    Product,
    ProductImages,
    ProductReview,
    ProductVariant,
    Cart,
    CartItem,
    Order,
    OrderItem,
)
from .serializers import *


# --------------------------- navigation bar start here ---------------------------
class NavigationViewSet(APIView):
    def get(self, request):
        logo = CompanyLogo.objects.filter(is_active= True).order_by('-updated_at').first()
        nav_option = NavOption.objects.filter(is_active= True).order_by('order')[:4]
        nav_button = NavButtons.objects.filter(is_active= True).order_by('order')[:3]

        return Response (
            {
                "logo" : CompanyLogoSerializer(logo).data,
                "nav_option" : NavOptionSerializer(nav_option, many = True).data,
                "nav_button" : NavButtonsSerializer(nav_button, many = True).data,
            },
            status= status.HTTP_200_OK
        )
    
# --------------------------- navigation bar end here ---------------------------

# --------------------------- hero section start here ---------------------------
class HeroSectionViewSet(APIView):
    def get(self, request):
        hero_section = HeroSection.objects.filter(is_active = True).order_by('-updated_at').first()
        return Response (
            {
                "hero_section": HeroSectionSerializer(hero_section).data
            },
            status= status.HTTP_200_OK
        )
# --------------------------- hero section end here ---------------------------



# This API will return Only Parent categorys
class CategoryAPIView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return ProductCategory.objects.filter(is_active = True, parent_id__isnull=True).order_by('order')[:4]

# This API will return Parent & child categorys
class CategoryWithChildrenAPIView(APIView):
    def get(self, request):
        categories = ProductCategory.objects.filter(is_active=True,parent_id__isnull=True).prefetch_related('children')

        serializer = ParentCategorySerializer(categories, many=True)
        return Response(serializer.data)

# Using this api we can see Category-wise Product List
class CategoryProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(
            category__slug=self.kwargs['slug'],
            is_active=True
        ).prefetch_related('images')

# Product Api Start here.    
class ProductDetailsAPIView(RetrieveAPIView):
    serializer_class = ProductDetailsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).prefetch_related('images', 'variants')
    
class FeaturedProductAPIView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        print("🔥 FEATURED API HIT 🔥")
        qs = Product.objects.filter(
            featured_products=True,
            is_active=True
        )
        print("QUERYSET:", qs)
        return qs.prefetch_related('images')

        # return Product.objects.filter(
        #     featured_products=True,
        #     is_active=True
        # ).prefetch_related('images')
    
class NewArrivalProductAPIView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(
            new_arrivals=True,
            is_active=True
        ).prefetch_related('images')
    
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

# add procut in cart
class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        variant_id = request.data.get('variant_id')
        quantity = int(request.data.get('quantity', 1))

        variant = ProductVariant.objects.get(id=variant_id)
        cart = get_user_cart(request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        return Response({
            "message": "Added to cart",
            "item": CartItemSerializer(item).data
        })

# to see all carts
class CartListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_user_cart(request.user)
        items = cart.items.select_related('variant__product')

        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)
    
class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        quantity = int(request.data.get('quantity'))

        item = CartItem.objects.get(
            id=pk,
            cart__user=request.user
        )
        item.quantity = quantity
        item.save()

        return Response({
            "message": "Quantity updated"
        })
    
class RemoveCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        item = CartItem.objects.get(
            id=pk,
            cart__user=request.user
        )
        item.delete()

        return Response({
            "message": "Item removed"
        })
    
class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # Order List
    def list(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    # Order Create (MOST IMPORTANT)
    def create(self, request):
        cart = Cart.objects.get(user=request.user)
        items = cart.items.select_related('variant__product')

        if not items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = 0
        order = Order.objects.create(
            user=request.user,
            total_amount=0,
            payment_method=request.data.get('payment_method', 'cash_on_delivery')
        )

        for item in items:
            price = item.variant.product.base_price
            total += price * item.quantity

            OrderItem.objects.create(
                order=order,
                product=item.variant.product,
                product_variant=item.variant,
                quantity=item.quantity,
                price=price
            )

        order.total_amount = total
        order.save()

        cart.items.all().delete()  # clear cart

        return Response(
            {"message": "Order placed successfully"},
            status=status.HTTP_201_CREATED
        )

    # Order Details
    def retrieve(self, request, pk=None):
        order = Order.objects.get(id=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)