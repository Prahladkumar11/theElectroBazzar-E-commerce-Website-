from .models import *
def GlobalData(request):
    categorys=Categories.objects.all()
    products=Product.objects.all()
    if request.user.is_authenticated:
        try:
            active_cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            # Create a new cart if it doesn't exist
            active_cart = Cart.objects.create(user=request.user)
        wishlist=Wishlist.objects.filter(user=request.user)
       
        # Fetch cart items for the user's cart
        cart_items = Cart_item.objects.filter(cart=active_cart)

        total_price = sum(item.product.discounted_price * item.quantity for item in cart_items)
        total_item=sum(item.quantity for item in cart_items)
    else:
        # For non-authenticated users, set empty values
        active_cart = None
        cart_items = []
        wishlist = []
        total_price = 0
        total_item = 0
    
    
    context={
        'categorys':categorys,
        'products':products,
        'cart_items':cart_items,
        'wishlist':wishlist,
        'total_price':total_price,
        'total_item':total_item
        
        

    }
    
    return {'data':context}
