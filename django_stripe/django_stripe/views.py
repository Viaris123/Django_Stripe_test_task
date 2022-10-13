import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET


from .models import Item
from .settings import API_SECRET_KEY, API_PUBLIC_KEY


@require_GET
def home(request):
    item_list = Item.objects.all()
    context = {'item_list': item_list}
    return render(request, 'home.html', context)


@require_GET
def item(request, item_id):
    product = get_object_or_404(Item, pk=item_id)
    context = {'product': product,
               'public_key': API_PUBLIC_KEY}
    reverse('item', kwargs={'item_id': item_id})
    return render(request, "item.html", context)


@require_GET
def buy(request, item_id):
    stripe.api_key = API_SECRET_KEY
    product = get_object_or_404(Item, pk=item_id)
    session = stripe.checkout.Session.create(success_url=request.build_absolute_uri('/success'),
                                             cancel_url=request.build_absolute_uri(f'/item/{item_id}'),
                                             line_items=[
                                                 {
                                                     "price": product.price_id,
                                                     "quantity": 1,
                                                 },
                                             ],
                                             mode='payment')
    return JsonResponse(session)


def success(request):
    return render(request, 'success.html')
