from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator,MaxLengthValidator,RegexValidator,EmailValidator
# Create your models here.

class User(models.Model):

    UserId=models.AutoField(primary_key=True)
    FirstName=models.CharField(max_length=32)
    LastName=models.CharField(max_length=32)
    Email = models.EmailField(
        validators=[
            EmailValidator(message='Enter a valid email address.')
        ]
    )
    Password=models.CharField(max_length=4096)
    PhoneNo = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(limit_value=10, message='Phone number must be exactly 10 digits.'),
            MaxLengthValidator(limit_value=10, message='Phone number must be exactly 10 digits.'),
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be a 10-digit integer.',
                code='invalid_phone_number'
            )
    ])
    Address=models.CharField(max_length=100)

    ROLE_CHOICES = (
    ("Buyer", "Buyer"),
    ("Seller", "Seller"),
    ("Admin", "Admin"),
    )
    Role=models.CharField(max_length=6,choices=ROLE_CHOICES,default="Buyer")

    def save(self, *args, **kwargs):
        # Check if the password is not already hashed
        if not self.Password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')):
            # Hash the password before saving
            self.Password = make_password(self.Password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user'



class Seller(models.Model):
    SellerId=models.AutoField(primary_key=True)
    UserObj=models.OneToOneField(User,on_delete=models.CASCADE)
    Company=models.TextField(max_length=32)
    CompanyLocation=models.TextField(max_length=50)

    class Meta:
        db_table = 'seller'


class Book(models.Model):
    BookId=models.AutoField(primary_key=True)
    Seller=models.ForeignKey(Seller,on_delete=models.CASCADE)
    Title=models.CharField(max_length=50)
    Author=models.CharField(max_length=30)
    Genre=models.CharField(max_length=20)
    Price=models.FloatField()
    PublishYear=models.CharField(max_length=4)
    Image=models.URLField(max_length=128)
    Description=models.TextField(max_length=200)
    AvailQuantity=models.IntegerField()
    SoldQuantity=models.IntegerField()
    Language=models.CharField(max_length=20)
    OverallRating=models.FloatField(max_length=100)
    TotalReviews=models.IntegerField()

    class Meta:
        db_table = 'book'
        unique_together = (('Seller', 'Title'),)



class Request(models.Model):
    RequestId=models.AutoField(primary_key=True)
    SellerObj=models.OneToOneField(Seller,on_delete=models.CASCADE)

    class Meta:
        db_table = 'request'

class WishList(models.Model):
    ListId=models.AutoField(primary_key=True)
    UserObj=models.OneToOneField(User,on_delete=models.CASCADE)
    TotalQuantity=models.IntegerField()
    
    class Meta:
        db_table = 'wishlist'

class WishListElement(models.Model):
    ListElementId=models.AutoField(primary_key=True)
    ListObj=models.ForeignKey(WishList,on_delete=models.CASCADE)
    BookObj=models.ForeignKey(Book,on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlistelement'

class Cart(models.Model):
    CartId=models.AutoField(primary_key=True)
    UserObj=models.OneToOneField(User,on_delete=models.CASCADE)
    TotalQuantity=models.IntegerField()

    class Meta:
        db_table = 'cart'

class CartElement(models.Model):
    CartElementId=models.AutoField(primary_key=True)
    CartObj=models.ForeignKey(Cart,on_delete=models.CASCADE)
    BookObj=models.ForeignKey(Book,on_delete=models.CASCADE)
    ElementQuantity=models.IntegerField()

    class Meta:
        db_table = 'cartelement'

class Order(models.Model):
    OrderId=models.AutoField(primary_key=True)
    UserObj=models.ForeignKey(User,on_delete=models.CASCADE)
    PlacedTime=models.DateTimeField(auto_now_add=True)
    TotalQuantity=models.IntegerField()
    TotalAmount=models.FloatField()

    class Meta:
        db_table = 'order'

class OrderElement(models.Model):
    OrderElementId=models.AutoField(primary_key=True)
    OrderObj=models.ForeignKey(Order,on_delete=models.CASCADE)
    BookObj=models.ForeignKey(Book,on_delete=models.CASCADE)
    ElementQuantity=models.IntegerField()
    ElementTotalPrice=models.FloatField()

    class Meta:
        db_table = 'orderelement'

class Reviews(models.Model):
    ReviewId=models.AutoField(primary_key=True)
    UserObj=models.ForeignKey(User,on_delete=models.CASCADE)
    BookObj=models.ForeignKey(Book,on_delete=models.CASCADE)
    Rating=models.IntegerField()
    ReviewComment=models.TextField(max_length=128)
    ReviewDate=models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'reviews'

