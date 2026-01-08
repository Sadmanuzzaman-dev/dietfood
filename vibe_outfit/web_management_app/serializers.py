from rest_framework import serializers

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

# --------------------------- navigation bar start here ---------------------------
class CompanyLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyLogo
        fields = ('id','logo', 'url','is_active','created_at', 'updated_at')
        read_only_fields = ['id', 'is_active','created_at', 'updated_at']

class NavOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavOption
        fields = ('id','title', 'url', 'order', 'is_active','created_at', 'updated_at')
        read_only_fields = ['id', 'is_active','created_at', 'updated_at']

class NavButtonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavButtons
        fields = ('id','icon', 'url', 'order','is_active','created_at', 'updated_at')
        read_only_fields = ['id', 'is_active','created_at', 'updated_at']

# --------------------------- navigation bar end here ---------------------------


# --------------------------- hero section start here ---------------------------
class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = ('id','bg_img', 'catalog_name','heading','sub_heading',
                  'cta_btn_1', 'cta_btn_1_url','cta_btn_2', 'cta_btn_2_url',
                  'is_active', 'created_at', 'updated_at')
        read_only_fields = ['id', 'is_active','created_at', 'updated_at']

# --------------------------- hero section end here ---------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"

class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'image']
            
class ParentCategorySerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id','name','slug','image','children']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'image', 'order']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id','sku','color','size','material','stock']

class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'base_price',
            'discount_price',
            'image',
            'featured_products',
            'new_arrivals',
        ]
    def get_image(self, obj):
        image = obj.images.filter(is_active=True).first()
        return image.image.url if image else None
    
class ProductDetailsSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'short_description',
            'description',
            'base_price',
            'discount_price',
            'images',
            'variants'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='variant.product.name', read_only=True)
    price = serializers.DecimalField(
        source='variant.product.base_price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product_name',
            'variant',
            'quantity',
            'price'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    variant_sku = serializers.CharField(source='product_variant.sku', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'product_name',
            'variant_sku',
            'quantity',
            'price'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='iteams', many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'total_amount',
            'status',
            'payment_method',
            'created_at',
            'items'
        ]