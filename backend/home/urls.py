from django.urls import path
from home import views


urlpatterns = [

    path("",views.index),
    path("signup/",views.signup),
    path("sellersignup/",views.sellersignup),
    path("getrequeststatus/",views.getrequeststatus),
    path("sellerregister/",views.sellerregister),
    path("signin/",views.signin),
    path("getbooks/",views.getbooks),
    path("uploadbook/",views.uploadbook),
    path("addtolist/",views.addtolist),
    path("deletefromlist/",views.deletefromlist),
    path("addtocart/",views.addtocart),
    path("deletefromcart/",views.deletefromcart),
    path("getcartelements/",views.getcartelements),
    path("getwishlistelements/",views.getwishlistelements),
    path("getorderelements/",views.getorderelements),
    path("placeorder/",views.placeorder),
    path("searchbook/",views.searchbook),
    path("logout/",views.logout),
    path("updatecart/",views.updatecart),


    
]