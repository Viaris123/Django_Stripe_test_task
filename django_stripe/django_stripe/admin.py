from django.contrib import admin
from .models import Item
from .settings import API_SECRET_KEY
import stripe

stripe.api_key = API_SECRET_KEY


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    exclude = ('prod_id', )

    def save_model(self, request, obj, form, change):
        print(request.body)
        try:
            new_product = stripe.Product.create(name=request.POST['name'],
                                                description=request.POST['description'],
                                                default_price_data={'unit_amount': request.POST['price'] * 100,
                                                                    'currency': 'usd'})
        except Exception as e:
            raise e
        obj.name = new_product.name
        obj.description = new_product.description
        obj.price = request.POST['price']
        obj.prod_id = new_product.id
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            print(obj.prod_id)
            stripe.Product.modify(obj.prod_id, active=False)
            obj.delete()

    search_fields = ('name__startswith',)

