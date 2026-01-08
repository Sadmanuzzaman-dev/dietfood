import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibe_outfit.settings')
django.setup()
from web_management_app.models import ProductReview
print("hello wsadfasdf")

product_review= ProductReview.objects.all()
print(product_review)
# product.delete()
# print(product)
# product_review.objects.all().delete()
# print("delete done")