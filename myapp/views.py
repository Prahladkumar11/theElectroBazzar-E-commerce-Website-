from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from .models import *


def index(request):      
    """
    View for rendering the index page.
    """
    return render(request, 'index.html')


def get_updated_cart_items(request):
    """
    View for getting updated cart items for the current user.
    """
    if request.user.is_authenticated:
        try:
            active_cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            active_cart = Cart.objects.create(user=request.user)

        cart_items = Cart_item.objects.filter(cart=active_cart)
        total_price = sum(item.product.discounted_price * item.quantity for item in cart_items)
        
        updated_cart_items = [
            {
                'id': item.product.id,
                'product_name': item.product.name,
                'product_price': item.product.discounted_price,
                'quantity': item.quantity,
                'product_image': item.product.image[0],  # Assuming 'image' is a FileField in your Product model
            }
            for item in cart_items
        ]
    else:
        updated_cart_items = []

    return JsonResponse({'cart_items': updated_cart_items, 'total': total_price})


CustomUser = get_user_model()


def signup(request):
    """
    View for user signup.
    """
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password == cpassword:
            # Create a new user
            user = CustomUser.objects.create_user(username=email, email=email, password=password)
            
            user.save()

            # Log in the user
            login(request, user)
            
            return redirect('index')  # Redirect to your home or dashboard page
        else:
            messages.error(request, 'Passwords do not match.')
  
    return render(request, 'signup.html')


def loginUser(request):
    """
    View for user login.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to your home or dashboard page
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'signup.html')


def logoutUser(request):
    """
    View for user logout.
    """
    logout(request)
    return redirect('index')


def Products(request, item):
    """
    View for displaying products based on category.
    """
    products = Product.objects.filter(CategoriesId__name=item)
    
    context = {
        'products': products
    }
    return render(request, 'product.html', context)


def addToCart(request, pk):
    """
    View for adding a product to the cart.
    """
    product = Product.objects.get(id=pk)
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_item, created = Cart_item.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        from django.db.models import Sum
        cart_quantity = Cart_item.objects.filter(cart=cart).aggregate(Sum('quantity'))['quantity__sum'] or 0
        Wishlist.objects.filter(user=request.user, product_id=pk).delete()
        response_data = {
            'status': 'success',
            'message': 'Item Added to Cart.',
            'cart_quantity': cart_quantity,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Pls login first'})

def removeFromCart(request, pk):
    """
    View for removing a product from the cart.
    """
    cart = Cart.objects.get(user=request.user)
    product = Product.objects.get(id=pk)
    cart_item = Cart_item.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    index(request)
    return HttpResponse(status=204) 

@login_required
def wishlist(request):
    """
    View for displaying user's wishlist.
    """
    wishlist_items = Wishlist.objects.filter(user=request.user)
    product_ids = wishlist_items.values_list('product_id', flat=True)
    products = Product.objects.filter(id__in=product_ids)
    index(request)

    context = {
        'products': products
    }

    return render(request, 'wishlist.html', context)

@login_required
def addTowishlist(request, pk):
    """
    View for adding or removing a product to/from the wishlist.
    """
    product = Product.objects.get(id=pk)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist.delete()
    referer_url = request.META.get('HTTP_REFERER', None)
    if referer_url:
        index(request)
        return redirect(referer_url)
    else:
        return redirect('index')

def removeFromWishlist(request, pk):
    """
    View for removing a product from the wishlist.
    """
    product = Product.objects.get(id=pk)
    wishlist = Wishlist.objects.get(user=request.user, product=product)
    wishlist.delete()
    index(request)
    return redirect('wishlist')

def checkout(request):
    """
    View for processing the checkout.
    """
    items = Cart_item.objects.filter(cart__user=request.user)
    user = request.user
    try:
        billingAddress = BillingAddress.objects.filter(user=user)
        shippingAddresses = ShippingAddress.objects.filter(user=user)
        context = {
            'billingAddress': billingAddress,
            'shippingAddresses': shippingAddresses,
            'items': items
        }
    except:
        context = {
            'billingAddress': None,
            'shippingAddresses': None,
            'items': items
        }
    
    return render(request, 'checkout.html', context)

@login_required
def accDetail(request):
    """
    View for displaying user's account details.
    """
    index(request)
    user = request.user
    try:
        billingAddress = BillingAddress.objects.filter(user=user)
        shippingAddresses = ShippingAddress.objects.filter(user=user)
        billing_addresses_json = serializers.serialize('json', billingAddress)
        shipping_addresses_json = serializers.serialize('json', shippingAddresses)

        context = {
            'billingAddress': billingAddress,
            'shippingAddresses': shippingAddresses,
            'billing_addresses_json': billing_addresses_json,
            'shipping_addresses_json': shipping_addresses_json
        }
    except:
        context = {
            'billingAddress': None,
            'shippingAddresses': None,
            "billing_addresses_json": None,
            "shipping_addresses_json": None
        }
    return render(request, 'accountDetail.html', context)

def deleteBillingaddress(request, pk):
    """
    View for deleting a billing address.
    """
    address = get_object_or_404(BillingAddress, id=pk, user=request.user)
    address.delete()
    return JsonResponse({'status': 'success', 'message': 'Address deleted successfully'})

def deleteshippingaddress(request, pk):
    """
    View for deleting a shipping address.
    """
    address = get_object_or_404(ShippingAddress, id=pk, user=request.user)
    address.delete()
    return JsonResponse({'status': 'success', 'message': 'Address deleted successfully'})

def editBillingaddress(request, pk):
    """
    View for editing a billing address.
    """
    address = get_object_or_404(BillingAddress, id=pk, user=request.user)

    try:
        if request.method == 'POST':
            # Update address fields using request.POST dictionary
            address.first_name = request.POST['first-name']
            address.last_name = request.POST['last-name']
            address.email = request.POST['editemail']
            address.address = request.POST['address']
            address.city = request.POST['city']
            address.state = request.POST['state']
            address.country = request.POST['country']
            address.pincode = request.POST['pincode']

            # Save the changes
            address.save()

            return JsonResponse({'status': 'success', 'message': 'Address updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def editShippingaddress(request,pk):
    """
    View for editing a shipping address.
    """
    address = get_object_or_404(ShippingAddress, id=pk, user=request.user)
    try:
        if request.method == 'POST':
            address.first_name = request.POST['first-name']
            address.last_name = request.POST['last-name']
            address.email = request.POST['email']
            address.address = request.POST['address']
            address.city = request.POST['city']
            address.state = request.POST['state']
            address.country = request.POST['country']
            address.pincode = request.POST['pincode']
            address.save()
            return JsonResponse({'status': 'success', 'message': 'Address updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
def orderPage(request):
    """
    View for rendering the order page for the current user.
    """
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'orderdetails': orders
    }
    return render(request, 'order.html', context)


def orderdetail(request, id):
    """
    View for getting order details for a specific order.
    """
    orderlines = OrderLine.objects.filter(order__orderId=id)
    
    response = [
        {
            'product_name': item.product.name,
            'product_price': item.product.discounted_price,
            'quantity': item.quantity,
        }
        for item in orderlines
    ]

    return JsonResponse({'data': response})   


def placeorder(request):
    """
    View for placing an order.
    """
    if request.method == "POST":
        # Get billing address data
        First_Name = request.POST.get('first-name')
        Last_Name = request.POST.get('last-name')
        Email = request.POST.get('email')
        Address = request.POST.get('address')
        City = request.POST.get('city')
        State = request.POST.get('state')
        Country = request.POST.get('country')
        Pincode = request.POST.get('pincode')

        # Check if billing address already exists
        billing_address, created1 = BillingAddress.objects.get_or_create(
            user=request.user,
            first_name=First_Name,
            last_name=Last_Name,
            email=Email,
            address=Address,
            city=City,
            state=State,
            country=Country,
            pincode=Pincode
        )

        # Initialize created2 to None
        created2 = None

        # Get shipping address data
        if request.POST.get('shiping-address'):
            s_First_Name = request.POST.get('s-first-name')
            s_Last_Name = request.POST.get('s-last-name')
            s_Email = request.POST.get('s-email')
            s_Address = request.POST.get('s-address')
            s_City = request.POST.get('s-city')
            s_State = request.POST.get('s-state')
            s_Country = request.POST.get('s-country')
            s_Pincode = request.POST.get('s-pincode')

            # Check if shipping address already exists
            

        else:
            # Use billing address as shipping address if not provided separately
            s_First_Name = First_Name
            s_Last_Name = Last_Name
            s_Email = Email
            s_Address = Address
            s_City = City
            s_State = State
            s_Country = Country
            s_Pincode = Pincode
            
            
        shipping_address, created2 = ShippingAddress.objects.get_or_create(
                user=request.user,
                first_name=s_First_Name,
                last_name=s_Last_Name,
                email=s_Email,
                address=s_Address,
                city=s_City,
                state=s_State,
                country=s_Country,
                pincode=s_Pincode
            )

        orderdata=order(request,billing_address.id,shipping_address.id)
        print(orderdata)
        if orderdata.status_code==200: 
            # Delete the cart
            cart = get_object_or_404(Cart, user=request.user)
            cart.delete()
            response_data = {'status': 'success', 'message': 'Order placed successfully!'}
            return JsonResponse(response_data)
        else:
            response_data = {'status': 'failure', 'message': 'Failed to place the order. '}
            return JsonResponse(response_data)

    response_data = {'status': 'failure', 'message': 'Failed to place the order. Something unexplected'}
    return JsonResponse(response_data)


def order(request, bid, sid):
    """
    Helper function for placing an order.
    """
    print("sid",sid,"bid",bid)
    try:
        ship = ShippingAddress.objects.get(id=sid)
        bill = BillingAddress.objects.get(id=bid)
        items = Cart_item.objects.filter(cart__user=request.user)
        total_price = sum(item.product.discounted_price * item.quantity for item in items)
        
        order = Order.objects.create(user=request.user, shippingAddress=ship, billingAddress=bill,amount=total_price)
        for i in items:
            order_item = OrderLine.objects.create(order=order, product=i.product, quantity=i.quantity)
            
        return JsonResponse({'status': True})
    except Exception as e:
        print("Error occured", e)
        return HttpResponse(status=500)


def change_password(request):
    """
    View for changing user's password.
    """
    if request.method == 'POST':
        oldpsd = request.POST.get('oldpsd')
        newpsd = request.POST.get('newpsd')
        cnewpsd = request.POST.get('cnewpsd')
        user = request.user

        # Check if old password matches
        try:
            if not user.check_password(oldpsd):
                return JsonResponse({'message': 'Old Password did not match'})

            # Check if new password and confirm new password match
            if newpsd != cnewpsd:
                return JsonResponse({'status':"fail",'message': 'New Password and Confirm New Password did not match'})

            # Set new password and save the user
            user.set_password(newpsd)
            user.save()
            user = authenticate(request, username=user.username, password=cnewpsd)
            if user is not None:
                login(request, user)
                index(request)
            

            return JsonResponse({'status':"success",'message': 'Password changed successfully'})
        except Exception as e:
            return JsonResponse({'status':"fail",'message': str(e)})


def editdetail(request):
    """
    View for editing user's details.
    """
    try:
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        mobNO = request.POST.get("mob")
        print(first_name, last_name, email, mobNO)
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.mobile_number = mobNO 
        user.save()
        
        return JsonResponse({'status': "success", 'message': 'Profile updated successfully'})
    except Exception as e:
        return JsonResponse({'status': "fail", 'message': str(e)})


def searchPage(request):
    """
    View for rendering the search page.
    """
    category_id = int(request.GET.get('category'))
    search_query = request.GET.get('search')

    if category_id:
        products = Product.objects.filter(CategoriesId=category_id, name__icontains=search_query)
    else :
        products = Product.objects.filter(name__icontains=search_query)
        
    return render(request, 'searchpage.html', {'products': products})


def productdetail(request, id):
    """
    View for rendering the product detail page.
    """
    product = get_object_or_404(Product, pk=id)
    relatedProduct = Product.objects.filter(CategoriesId=product.CategoriesId).exclude(pk=product.pk)[:4]
    context={
        'product':product,
        'relatedProduct':relatedProduct
    }
    return render(request,"productDetail.html",context)
   
    
    