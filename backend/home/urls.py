from django.urls import path
from home.views import views


urlpatterns = [

    path("/",views.index),
    path("signup/",views.signup),
    path("sellersignup/",views.sellersignup),
    path("getbooks/",views.getbooks),
    path("uploadbook/",views.uploadbook),
    path("signin/",views.signin),
    path("addtocart/",views.addtocart),
    path("deletefromcart/",views.deletefromcart),
    path("addtolist/",views.addtolist),
    path("deletefromlist/",views.deletefromlist),
]


