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

items = stripe.Product.list()
for item in items:
    if item['active']:
        price = stripe.Price.retrieve(item['default_price'])
        obj, created = Item.objects.update_or_create(
            name=item['name'],
            description=item['description'],
            price=price['unit_amount']/10,
            prod_id=item['id'],
            price_id=price['id'])
        obj.save()
if DEBUG:
    print(Item.objects.all())


