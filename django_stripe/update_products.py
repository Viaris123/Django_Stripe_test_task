import os
import sys
import django
import stripe
from django_stripe.settings import API_SECRET_KEY, DEBUG

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_stripe.settings')
django.setup()

from django_stripe.models import Item

stripe.api_key = API_SECRET_KEY

items = stripe.Product.search(query="active:'true'",)

for item in items:
    price = stripe.Price.retrieve(item["default_price"])["unit_amount"]/100
    obj, created = Item.objects.update_or_create(name=item['name'],
                                                 description=item['description'],
                                                 price=price,
                                                 prod_id=item['id'],
                                                 img_url=item['images'])

if DEBUG:
    # print(items)
    print(Item.objects.all())



