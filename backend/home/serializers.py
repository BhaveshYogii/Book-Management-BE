from rest_framework.serializers import ModelSerializer
from home.models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class wishListSerializer(ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'

class CartElementSerializer(ModelSerializer):
    class Meta:
        model = CartElement
        fields = '__all__'    

class ListElementSerializer(ModelSerializer):
    class Meta:
        model = WishListElement
        fields = '__all__'                 

class OrderElementSerializer(ModelSerializer):
    class Meta:
        model = OrderElement
        fields = '__all__'                 
                          
class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'                              

class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'          