import stripe
from stripe.error import SignatureVerificationError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from .models import Item
from .forms import CreateUser
from .settings import API_SECRET_KEY, API_PUBLIC_KEY, STRIPE_WEBHOOK_KEY


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
@login_required()
def buy(request, item_id):
    stripe.api_key = API_SECRET_KEY
    product = get_object_or_404(Item, pk=item_id)
    session = stripe.checkout.Session.create(success_url=request.build_absolute_uri('/success'),
                                             cancel_url=request.build_absolute_uri(f'/item/{item_id}'),
                                             line_items=[
                                                 {
                                                     "price_data": {
                                                         'currency': 'usd',
                                                         'product': product.prod_id,
                                                         'unit_amount': product.price*100
                                                     },
                                                     "quantity": 1,
                                                 },
                                             ],
                                             mode='payment')
    return JsonResponse(session)


@require_POST
def webhook_paid_endpoint(request):

    event = None
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_KEY)
        print(event)
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e

    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']
        if checkout_session.payment_status == 'paid':
            print('paid')
    return HttpResponse(status=200)


def signin(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        new_user = User.objects.create_user(username=str(form['name']),
                                            email=str(form['user_email']),
                                            password=str(form['password']))
        new_user.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        form = CreateUser()
        return render(request, 'registration/signin.html', {'form': form})


def paid_success(request):
    return render(request, 'success.html')

# TODO: add user, admin panel
