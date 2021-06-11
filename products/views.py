from celery.utils.serialization import jsonify
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, TemplateView
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.mixins import UserPassesTestMixin
from account.models import UserProfile, User
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator

from .models import *
from sellers.models import Seller
from .forms import ProductCreateForm, ProductImageFrom

import stripe

stripe.api_key = "sk_test_51ImWnySAF2GIiT99gaY9l33N1gINm1xKVmsIpECk4xGWBDc4pExKjmPmL6xHzKVXWyeYznDuBascdGeNRoC7lnZQ00nHL4Hbz3"



    

class CreateProducts(View):
    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        user = request.user
        seller = Seller.objects.filter(user=user).last()
        # seller=Seller.objects.all().get(user=user)
        if seller is None:
            print("none")
        else:
            if seller.user == user:
                # form = ProductCreateForm(request.POST)
                if request.method == "POST":
                    title = request.POST.get('title')
                    desc= request.POST.get('desc')
                    cate = request.POST.get('cate')
                    price = request.POST.get('price')
                    images = request.FILES.getlist('file')
                    print(images)
                   
                

                    seller = Seller.objects.get(user=request.user)
              
                    obj = Product.objects.create(seller=seller,name=title, description=desc,price=price)
                
                    obj.save()

                    for img in images:
                        ProductImages.objects.create(product=obj, image=img)

                else:
                    print( "is not valid data ")

            else:
                return HttpResponse("you can't add products ")

        return HttpResponse("data submitted")

    def get(self, request):
        form = ProductCreateForm
        category = Category.objects.all()
        img_form = ProductImageFrom

        return render(request, 'products/createproduct.html', {'form': form, 'img_form': img_form,'category': category})


class ProductListView(View):
    def get(self, request):
        context = {}

        if request.user.is_authenticated:
            cart_item = Cart.objects.filter(user=request.user)
            context['cart_item'] = cart_item

        products = Product.objects.all()
        pages=Paginator(products, 5)

        page_number = request.GET.get('page')
        page_obj = pages.get_page(page_number)
        print(pages.num_pages)
        categories = Category.objects.all()
        context['products'] = products
        context['page_obj'] = page_obj

        context['categories'] = categories

        return render(request, 'products/productlist.html', context)


class ProductDetail(View):

    def get(self, request, id):
        context = {}
        if request.user.is_authenticated:
            cart_item = Cart.objects.filter(user=request.user)
            context['cart_item'] = cart_item

        product = Product.objects.get(id=id)
        images = product.product_images.all()
        context['images'] = images
        for i in images:
            print(i)
        context['product_detail'] = product

        return render(request, 'products/productdetail.html', context)


class ProductSearch(View):

    def get(self, request):
        data = {}

        search = request.GET.get('search')
        category = request.GET.get('category')
        if (category != "") and (search != ""):
            print(search)
            print(category)
            products = Product.objects.filter(
                name__startswith=search, category__name=category)
            data['products'] = products
        elif search != "":
            print("second")
            print(search)
            products = Product.objects.filter(name__startswith=search)
            data['products'] = products
        else:
            print("no data ")

        return render(request, 'products/suggestions.html', data)


class AddToCart(View):
    @method_decorator(login_required(login_url=''))
    def get(self, request):
        data = {}
        if request.user.is_authenticated:
            product_id = request.GET.get('add_product')
            if product_id is not None:
                product = Product.objects.get(id=product_id)
                user = request.user
                try:
                    seller = Seller.objects.filter(id=user.id).last()
                    if request.user.username != seller.user.username:
                        data['product'] = product
                        # import  pdb; pdb.set_trace()
                        obj = Cart.objects.update_or_create(
                            user=request.user, product=product)
                        data['add_to_cart'] = obj
                    else:
                        messages.error(request, "Seller Account can not  use for Shopping Please Create New Customer "
                                                "Account "
                                                "to shop")
                        return render(request, 'products/cart.html', data)

                except Exception as e:
                    print(e)

            return render(request, 'products/cart.html', data)


class RemoveFromCart(DeleteView):

    @method_decorator(login_required(login_url='/account/'))
    def get(self, request):
        c_id = request.GET.get("cart_id")
        # import pdb; pdb.set_trace()
        cart = Cart.objects.get(id=c_id)
        cart.delete()

        return redirect('list_products')


class CheckOut(View):

    def get(self, request):
        context = {}
        cart = Cart.objects.filter(user=request.user)
        t=0
        for p in cart:
            t =t+p.product.price


        context['cart_item'] = cart
        context['total'] = t


        return render(request, 'products/checkout-page.html', context)


class OrderDetailView(View):

    def post(self, request):
        name = request.POST.get('name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        state = request.POST.get('state')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')
        # import pdb;
        # pdb.set_trace()
        user = request.user

        address = BillingAddress.objects.create(name=name, address1=address1, address2=address2, state=state,
                                                city=city, mobile=mobile)
        product_id = request.POST.getlist('prdouct')

        for pro_id in product_id:
            ord_id = uuid.uuid4().hex[:6].upper()
            product = Product.objects.get(id=pro_id)
            order = OrderDetail(user=user, order_id=ord_id,
                                product=product, amount=product.price, address=address)
            # Cart.objects.filter(product=product).delete()
            order.save()

        return redirect('stripe')


class HomePageView(View):

    def get(self, request):
        context = {}

        order = Cart.objects.filter(user=request.user)

        context['order_item'] = order
        address = BillingAddress.objects.last()
        context['address'] = address

        template_name = 'products/stripe.html'
        return render(request, template_name, context)


class CancelView(TemplateView):
    template_name = 'products/cancel.html'


@csrf_exempt
def payment(request):
    orderDetails = Cart.objects.filter(user=request.user)

    for order in orderDetails:
        customer = stripe.Customer.create(
            email=order.user.email,
            source=request.POST['stripeToken'],
            name=order.user.username,
            address={
                'line1': '510 Townsend St',
                'postal_code': '98140',
                'city': 'San Francisco',
                'state': 'CA',
                'country': 'US',
            },
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            description=order.product.name,
            amount=order.product.price * 100,
            currency='inr',
        )

    return render(request, 'products/success.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:

            orderDetails = Cart.objects.filter(user=request.user)
            total = 0
            for order in orderDetails:
                total = total + order.product.price
                products = [order.product.name]
                str1 = ''.join(products)
                checkout_session = stripe.checkout.Session.create(
                    success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + 'cancel/',
                    payment_method_types=['card'],
                    shipping_address_collection={
                        'allowed_countries': ['US', 'CA', 'IN'],

                    },

                    customer_email=order.user.email,
                    mode='payment',
                    line_items=[
                        {
                            'name': str1,
                            'quantity': 1,
                            'currency': 'inr',
                            'amount': total*100,
                        }
                    ]

                )

            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(View):
    def get(self, request):
        status = stripe.checkout.Session.retrieve(request.GET.get('session_id'))

        # amt = stripe.Charge.retrieve(request.GET.get('session_id'))


        print(status)

        # if s_id.payment_status == 'paid':


        template = 'products/success.html'
        return render(request, template, {'order_s': status})



class ChatBotView(View):

    def get(self, request):

        return render(request, 'chatbot.html')
