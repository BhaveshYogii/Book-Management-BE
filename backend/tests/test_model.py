from django.test import TestCase
from home.models import *
from django.utils import timezone

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(
            FirstName="John",
            LastName="Doe",
            Email="john.doe@example.com",
            Password="Test12345", 
            PhoneNo="1234567890", 
            Address="123 Street, City",
            Role="Buyer" 
        )

        self.assertIsNotNone(user)
        self.assertEqual(user.FirstName, "John")
        self.assertEqual(user.LastName, "Doe")
        self.assertEqual(user.Email, "john.doe@example.com")
        self.assertTrue(user.Password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')))

class SellerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            FirstName="John",
            LastName="Doe",
            Email="john.doe@example.com",
            Password="Test12345",
            PhoneNo="1234567890",
            Address="123 Street, City",
            Role="Seller"
        )

    def test_create_seller(self):
        seller = Seller.objects.create(
            UserObj=self.user,
            Company="ABC Inc.",
            CompanyLocation="City XYZ"
        )

        self.assertIsNotNone(seller)
        self.assertEqual(seller.UserObj, self.user)
        self.assertEqual(seller.Company, "ABC Inc.")
        self.assertEqual(seller.CompanyLocation, "City XYZ")

class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            FirstName="John",
            LastName="Doe",
            Email="john.doe@example.com",
            Password="Test12345",
            PhoneNo="1234567890",
            Address="123 Street, City",
            Role="Seller"
        )

        self.seller = Seller.objects.create(
            UserObj=self.user,
            Company="ABC Inc.",
            CompanyLocation="City XYZ"
        )

    def test_create_book(self):
        book = Book.objects.create(
            SellerObj=self.seller,
            Title="Sample Book",
            Author="John Doe",
            Genre="Fiction",
            Price=19.99,
            PublishYear="2022",
            Image="https://example.com/image.jpg",
            Description="A sample book description",
            AvailQuantity=10,
            Language="English",
            OverallRating=4.5,
            TotalReviews=100
        )

        self.assertIsNotNone(book)
        self.assertEqual(book.SellerObj, self.seller)
        self.assertEqual(book.Title, "Sample Book")

    def test_unique_together_constraint(self):
        Book.objects.create(
            SellerObj=self.seller,
            Title="Sample Book",
            Author="John Doe",
            Genre="Fiction",
            Price=19.99,
            PublishYear="2022",
            Image="https://example.com/image.jpg",
            Description="A sample book description",
            AvailQuantity=10,
            Language="English",
            OverallRating=4.5,
            TotalReviews=100
        )

        with self.assertRaises(Exception):
            Book.objects.create(
                SellerObj=self.seller,
                Title="Sample Book",
                Author="Jane Smith",
                Genre="Non-Fiction",
                Price=24.99,
                PublishYear="2021",
                Image="https://example.com/image2.jpg",
                Description="Another sample book description",
                AvailQuantity=15,
                Language="Spanish",
                OverallRating=4.0,
                TotalReviews=50
            )

class RequestModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            FirstName="John",
            LastName="Doe",
            Email="john.doe@example.com",
            Password="Test12345",
            PhoneNo="1234567890",
            Address="123 Street, City",
            Role="Seller"
        )

        self.seller = Seller.objects.create(
            UserObj=self.user,
            Company="ABC Inc.",
            CompanyLocation="City XYZ"
        )

    def test_create_request(self):
        request = Request.objects.create(
            SellerObj=self.seller,
            Status="Pending"
        )

        self.assertIsNotNone(request)
        self.assertEqual(request.SellerObj, self.seller)
        self.assertEqual(request.Status, "Pending")

class WishListModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            FirstName="John",
            LastName="Doe",
            Email="john.doe@example.com",
            Password="Test12345",
            PhoneNo="1234567890",
            Address="123 Street, City",
            Role="Buyer"
        )

    def test_create_wishlist(self):
        wishlist = WishList.objects.create(
            UserObj=self.user,
            TotalQuantity=0
        )

        self.assertIsNotNone(wishlist)
        self.assertEqual(wishlist.UserObj, self.user)
        self.assertEqual(wishlist.TotalQuantity, 0)

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            FirstName="John",
            LastName="Doe",
            Email="john.doe@example.com",
            Password="Test12345",
            PhoneNo="1234567890",
            Address="123 Street, City",
            Role="Buyer"
        )

    def test_create_cart(self):
        cart = Cart.objects.create(
            UserObj=self.user,
            TotalQuantity=0
        )

        self.assertIsNotNone(cart)
        self.assertEqual(cart.UserObj, self.user)
        self.assertEqual(cart.TotalQuantity, 0)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            FirstName="John",
            LastName="Doe",
            Email="john.doe@example.com",
            Password="Test12345",
            PhoneNo="1234567890",
            Address="123 Street, City",
            Role="Buyer"
        )

    def test_create_order(self):
        order = Order.objects.create(
            UserObj=self.user,
            TotalQuantity=2,
            TotalAmount=50.0
        )

        self.assertIsNotNone(order)
        self.assertEqual(order.UserObj, self.user)
        self.assertEqual(order.TotalQuantity, 2)
        self.assertEqual(order.TotalAmount, 50.0)
        self.assertAlmostEqual(timezone.now(), order.PlacedTime, delta=timezone.timedelta(seconds=1))
      




