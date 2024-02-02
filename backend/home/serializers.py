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