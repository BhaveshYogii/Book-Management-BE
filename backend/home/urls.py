from django.urls import path
from home import views


urlpatterns = [

    path("",views.index),
    path("signup/",views.signup),
    path("sellersignup/",views.sellersignup, name='sellersignup'),
    path("getrequeststatus/",views.getrequeststatus),
    path("sellerregister/",views.sellerregister , name='sellerregister'),
    path("signin/",views.signin ,name='signin'),
    path("getbooks/",views.getbooks, name='getbooks'),
    path("uploadbook/",views.uploadbook),
    path("addtolist/",views.addtolist , name='addtolist'),
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
    path("generate_pdf_invoice/",views.generate_pdf_invoice),
    path("getrole/",views.getrole),
    path("admingetbooks/",views.admingetbooks),
    path("admingetusers/",views.admingetusers),
    path("admingetrequests/",views.admingetrequests),
    path("adminupdaterequests/",views.adminupdaterequests),
    path("sellergetbooks/",views.sellergetbooks),
    path("sellerupdatebook/",views.sellerupdatebook),


    
]