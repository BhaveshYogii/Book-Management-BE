from django.contrib import admin
from home.models import User,Seller,Book,Cart,CartElement,WishList,WishListElement,Request


# Register your custom user model with the admin site
admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(CartElement)
admin.site.register(WishList)
admin.site.register(WishListElement)
# admin.site.register(Order)
# admin.site.register(OrderElement)
admin.site.register(Request)
# admin.site.register(Reviews)