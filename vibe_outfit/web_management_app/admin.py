from django.contrib import admin
from django.utils.html import format_html

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

@admin.register(CompanyLogo)
class CompanyLogoAdmin(admin.ModelAdmin):
    list_display = ('id','logo_preview','url','is_active','created_at','updated_at',)
    # search_fields = ('url','is_active',)
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    list_per_page = 100

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:contain;" />',
                obj.logo.url
            )
        return "-"

    logo_preview.short_description = "Logo"

@admin.register(NavOption)
class NavOptionAdmin(admin.ModelAdmin):
    list_display = ('id','title','url','order','is_active','created_at','updated_at',)
    search_fields = ('title',)
    list_filter = ('is_active',)
    list_editable = ('order','is_active',)
    list_per_page = 100
    ordering = ('order',)

@admin.register(NavButtons)
class NavButtonsAdmin(admin.ModelAdmin):
    list_display = ('id','icon_preview','url','order','is_active','created_at','updated_at',)
    list_filter = ('is_active',)
    list_editable = ('order','is_active',)
    list_per_page = 100
    ordering = ('order',)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="40" height="40" />',
                obj.icon.url
            )
        return "-"

    icon_preview.short_description = "Icon"

# --------------------------- navigation bar end here ---------------------------


# --------------------------- Hero Section end here ---------------------------
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'bg_img_preview', 'catalog_name', 'heading', 'short_sub_heading', 'cta_btn_1', 'cta_btn_2', 'is_active', 'created_at', 'updated_at')
    search_fields = ('catalog_name',)
    list_filter = ('catalog_name', 'is_active')
    list_editable = ('is_active',)
    list_per_page = 100
    ordering = ('-updated_at',)

    # to preview img in admin
    def bg_img_preview (self, obj):
        if obj.bg_img:
            return format_html(
                '<img src="{}" width ="50" height="40" />',
                obj.bg_img.url
            )
        return "-"
    bg_img_preview.short_description = "BG Img"


    # to show only first few word in admin
    def short_sub_heading(self, obj):
        if obj.sub_heading: 
            words = obj.sub_heading.split()
            return " ".join(words[:8]) + ("...." if len (words) >10 else " ")
        return "-"
    short_sub_heading.short_description = "Sub Heading"

# --------------------------- Hero Section end here ---------------------------


# --------------------------- Products Table start here ---------------------------

@admin.register(ProductCategory)
class ProductCategoryTable(admin.ModelAdmin):
    list_display = ('id','name','slug','order','image','parent_id','is_active','created_at','updated_at',)
    search_fields = ('name',)
    list_filter = ('is_active','parent_id',)
    list_editable = ('order','is_active',)
    list_per_page = 100
    ordering = ('order','name','parent_id')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'base_price', 'category', 'featured_products','new_arrivals','is_active', 'created_at')
    list_filter = ('is_active', 'category','featured_products','new_arrivals')
    search_fields = ('name', 'description')

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('id','product','image','order','is_active','created_at','updated_at',)
    search_fields = ('product',)
    list_filter = ('is_active','product',)
    list_editable = ('order','is_active',)
    list_per_page = 100
    ordering = ('product', 'order')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'user',
        'rating',
        'short_comment',
        'created_at',
    )

    search_fields = (
        'product__name',
        'user__username',
        'comment',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    list_per_page = 50
    ordering = ('-created_at',)

    def short_comment(self, obj):
        return obj.comment[:40] + "..." if len(obj.comment) > 40 else obj.comment

    short_comment.short_description = "Comment"


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'sku',
        'color',
        'size',
        'material',
        'stock',
        'is_active',
        'created_at',
    )

    search_fields = (
        'sku',
        'product__name',
    )

    list_filter = (
        'is_active',
        'color',
        'size',
        'material',
    )

    list_editable = (
        'stock',
        'is_active',
    )

    list_per_page = 100
    ordering = ('product', 'sku')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_at',
        'total_items',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    list_filter = (
        'created_at',
    )

    inlines = [CartItemInline]
    list_per_page = 50
    ordering = ('-created_at',)

    def total_items(self, obj):
        return obj.items.count()

    total_items.short_description = "Items"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'variant',
        'quantity',
    )

    search_fields = (
        'variant__sku',
        'cart__user__username',
    )

    list_filter = (
        'variant',
    )

    list_per_page = 100


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__email', 'user__username', 'id']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'total_amount')
        }),
        ('Status & Payment', {
            'fields': ('status', 'payment_method')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )