from django.urls import path,include
from . import  views


urlpatterns = [
   path('',views.index,name='index'),
   path('signup/',views.signup,name='signup'),
   path('login/',views.loginUser,name='login'),
   path('logout/',views.logoutUser,name='logout'),
   path('wishlist/',views.wishlist,name='wishlist'),
   path('checkout/',views.checkout,name='checkout'),
   path('orderpage/',views.orderPage,name='orderpage'),
   path('order/<int:id>',views.orderdetail,name='order'),
   path('accdetail/',views.accDetail,name='accdetail'),
   path('editdetail/',views.editdetail,name='editdetail'),
   path('placeorder/',views.placeorder,name='placeorder'),
   path('changepsd/',views.change_password,name='changepsd'),
   path('products/<str:item>/',views.Products,name='products'),
   path('additem/<int:pk>/',views.addToCart,name='additem'),
   path('removeitem/<int:pk>/',views.removeFromCart,name='removeitem'),
   path('addtowishlist/<int:pk>/',views.addTowishlist,name='addtowishlist'),
   path('removefromwishlist/<int:pk>/',views.removeFromWishlist,name='removefromwishlist'),
   path('deletebillingaddress/<int:pk>/',views.deleteBillingaddress,name='deletebillingaddress'),
   path('editbillingaddress/<int:pk>/',views.editBillingaddress,name='editbillingaddress'),
   path('deleteshippingaddress/<int:pk>/',views.deleteshippingaddress,name='deleteshippingaddress'),
   path('editshippingaddress/<int:pk>/',views.editShippingaddress,name='editshippingaddress'),
   path('get-updated-cart-items/',views.get_updated_cart_items, name='get_updated_cart_items'),

   
    
]