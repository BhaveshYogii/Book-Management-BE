# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from django.test import TestCase, RequestFactory
# from home.models import *
# from home.serializers import *
# from django.contrib.sessions.models import Session
# from django.contrib.sessions.backends.db import SessionStore
# from rest_framework.test import APITestCase
# from rest_framework import status
# from home.models import User, Seller, Request
# from django.contrib.sessions.models import Session
# from django.utils import timezone
# from django.contrib.sessions.middleware import SessionMiddleware
# from django.http import HttpRequest
# from django.urls import reverse
# from django.utils import timezone
# from django.forms.models import model_to_dict




# class SignupViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_signup_valid_data(self):
#         valid_user_data = {
#             'FirstName': 'John',
#             'LastName': 'Doe',
#             'Email': 'johndoe@example.com',
#             'Password': 'Test@123',
#             'PhoneNo': '1234567890',
#             'Address': '123 Street, City',
#             'Role': 'Buyer'
#         }

#         response = self.client.post('/signup/', valid_user_data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(User.objects.get().FirstName, 'John') 

#     def test_signup_invalid_data(self):
#         invalid_user_data = {
#             'FirstName': 'John',
#             'LastName': 'Doe',
#             'Password': 'Test123',
#             'PhoneNo': '1234567890',
#             'Address': '123 Street, City',
#             'Role': 'Buyer'
#         }

#         response = self.client.post('/signup/', invalid_user_data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('Email', response.data['error'])  


# class SignInTest(APITestCase):
#     def setUp(self):
#         self.user_data = {
#             'Email': 'test@example.com',
#             'Password': 'Test1234'
#         }
#         self.user = User.objects.create(**self.user_data)

#     def test_signin_missing_email(self):
#         url = reverse('signin')
#         data = {
#             'Password': 'Test1234',
#             'Email': ''

#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['error'], 'Email Id required')

#     def test_signin_missing_password(self):
#         url = reverse('signin')
#         data = {
#             'Password': '',
#             'Email': 'test@example.com',
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['error'], 'Password required')        

#     def test_signin_success(self):
#         url = reverse('signin')
#         data = {
#             'Email': 'test@example.com',
#             'Password': 'Test1234'
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue('session_key' in response.data)
    
#     def test_signin_invalid_credentials(self):
#         url = reverse('signin')
#         data = {
#             'Email': 'test@example.com',
#             'Password': 'WrongPassword'
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(response.data['error'], 'Invalid credentials')


# class SellerSignupTest(TestCase):
#     def setUp(self):
#         # Create a user for the session
#         self.user = User.objects.create(
#             FirstName='John',
#             LastName='Doe',
#             Email='john.doe@example.com',
#             Password='Test123',
#             PhoneNo='1234567890',
#             Address='123 Street, City',
#             Role='Buyer'
#         )
#         # Create a session for the user
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#         # Create a session and attach it to the request
#         self.factory = RequestFactory()
#         self.session = self.client.session
#         self.session['Email'] = self.user.Email
#         self.session.save()

#     def test_sellersignup_notsignup(self):
#         url = reverse('sellersignup')
#         data = {
#             'Company': 'ABC Inc.',
#             'CompanyLocation': 'City XYZ',
#             'session_key': '',
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 401)
#         self.assertEqual(Seller.objects.count(), 0)     

#     def test_sellersignup_success(self):
#         url = reverse('sellersignup')
#         data = {
#             'Company': 'ABC Inc.',
#             'CompanyLocation': 'City XYZ',
#             'session_key': self.session.session_key
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Seller.objects.count(), 1)        

#     def test_sellersignup_missing(self):
#         url = reverse('sellersignup')
#         data = {
#             'Company': '',
#             'CompanyLocation': 'City XYZ',
#             'session_key': self.session.session_key
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 400)


#     def test_sellersignup_already_seller(self):
#         Seller.objects.create(
#             UserObj=self.user,
#             Company='Existing Company',
#             CompanyLocation='Existing Location'
#         )
#         url = reverse('sellersignup')
#         data = {
#             'Company': 'New Company',
#             'CompanyLocation': 'New Location',
#             'session_key': self.session.session_key
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(Seller.objects.count(), 1)


# class ValidationTest(TestCase):
#     def test_validation_empty_session_key(self):
#         session_key = ""
#         self.assertFalse((session_key))


# class SellerRegisterTest(APITestCase):
#     def setUp(self):
#         # Create a user for the session
#         self.user = User.objects.create(
#             FirstName='John',
#             LastName='Doe',
#             Email='johndoe@example.com',
#             Password='Test123',
#             PhoneNo='1234567890',
#             Address='123 Street, City',
#             Role='Buyer'
#         )

#         self.admin = User.objects.create(
#             FirstName='John',
#             LastName='Doe',
#             Email='admin@example.com',
#             Password='Test123',
#             PhoneNo='1234567891',
#             Address='123 Street, City',
#             Role='Admin'
#         )
#         # Create a session for the user
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.admin)
#         # Create a session and attach it to the request
#         self.factory = RequestFactory()
#         self.session = self.client.session
#         self.session['Email'] = self.admin.Email
#         self.session.save()

#         # Create a Seller and a Request for the user
#         self.seller = Seller.objects.create(
#             UserObj=self.user,
#             Company='ABC Inc.',
#             CompanyLocation='City XYZ'
#         )
#         self.request = Request.objects.create(
#             SellerObj=self.seller,
#             Status='Pending'
#         )

#     def test_seller_register_pending_request(self):
#         url = reverse('sellerregister')
#         data = {'session_key': self.session.session_key,
#                 'sellerId' : self.seller.SellerId}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Request is in pending state', response.data.get('error', ''))       

#     def test_seller_register_accepted_request(self):
#         self.request.Status = 'Accepted'
#         self.user.Role='Seller'
#         self.request.save()
#         url = reverse('sellerregister')
#         data = {'session_key': self.session.session_key,
#                 'sellerId' : self.seller.SellerId}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(self.user.Role, 'Seller')
#         self.assertEqual(Seller.objects.filter(UserObj=self.user).count(), 1)

#     def test_seller_register_declined_request(self):
#         self.request.Status = 'Declined'
#         self.request.save()
#         url = reverse('sellerregister')
#         data = {'session_key': self.session.session_key,
#                 'sellerId' : self.seller.SellerId}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(self.user.Role, 'Buyer')
#         self.assertEqual(Request.objects.filter(SellerObj=self.seller).count(), 0)
#         self.assertEqual(Seller.objects.filter(UserObj=self.user).count(), 0)

#     def test_seller_register_not_seller(self):
#         self.seller.delete()
#         url = reverse('sellerregister')
#         data = {'session_key': self.session.session_key,
#                 'sellerId' : self.seller.SellerId}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('Seller Does Not Exist', response.data.get('error', ''))

#     def test_seller_register_no_request(self):
#         self.request.delete()
#         url = reverse('sellerregister')
#         data = {'session_key': self.session.session_key,
#                 'sellerId' : self.seller.SellerId}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('Request Does Not Exist', response.data.get('error', ''))   
 

# class LogoutAPITestCase(TestCase):
#     def setUp(self):
#         # Create a user for the session
#         self.user = User.objects.create(
#             FirstName='John',
#             LastName='Doe',
#             Email='johndoe@example.com',
#             Password='Test123',
#             PhoneNo='1234567890',
#             Address='123 Street, City',
#             Role='Buyer'
#         )

#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#         # Create a session and attach it to the request
#         self.factory = RequestFactory()
#         self.session = self.client.session
#         self.session['Email'] = self.user.Email
#         self.session.save()


#     def test_logout(self):
#         url = reverse('logout')
#         data = {'session_key': self.session.session_key}
#         response = self.client.post(url, data)
#         self.session.delete()
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#         self.assertFalse(Session.objects.filter(session_key=self.session.session_key).exists())


# class UploadBookTest(APITestCase):
#     def setUp(self):
#         # Create a user for the session
#         self.user = User.objects.create(
#             FirstName='John',
#             LastName='Doe',
#             Email='johndoe@example.com',
#             Password='Test123',
#             PhoneNo='1234567890',
#             Address='123 Street, City',
#             Role='Buyer'
#         )

#         self.admin = User.objects.create(
#             FirstName='John',
#             LastName='Doe',
#             Email='admin@example.com',
#             Password='Test123',
#             PhoneNo='1234567891',
#             Address='123 Street, City',
#             Role='Admin'
#         )
#         # Create a session for the user
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.admin)
#         # Create a session and attach it to the request
#         self.factory = RequestFactory()
#         self.session = self.client.session
#         self.session['Email'] = self.admin.Email
#         self.session.save()

#         # Create a Seller and a Request for the user
#         self.seller = Seller.objects.create(
#             UserObj=self.user,
#             Company='ABC Inc.',
#             CompanyLocation='City XYZ'
#         )
#         self.request = Request.objects.create(
#             SellerObj=self.seller,
#             Status='Pending'
#         )      
    
#     def test_seller_register_accepted_request(self):
#         self.request.Status = 'Accepted'
#         self.user.Role='Seller'
#         self.request.save()
#         url = reverse('sellerregister')
#         data = {'session_key': self.session.session_key,
#                 'sellerId' : self.seller.SellerId}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(self.user.Role, 'Seller')
#         self.assertEqual(Seller.objects.filter(UserObj=self.user).count(), 1)
    
#     def test_upload_book_success(self):
#         url = reverse('uploadbook')  
#         # Assuming you have a URL name for the uploadbook endpoint
#         data = {
#             'session_key': self.session.session_key,
#             'Title': 'Test Book1',
#             'Author': 'Test Author',
#             'Genre': 'Test Genre',
#             'Price': 10.99,
#             'PublishYear': '2022',
#             'Image': 'https://example.com/image.jpg',
#             'Description': 'This is a test book description.',
#             'AvailQuantity': 10,
#             'Language': 'English', 
#             'SellerObj' : self.seller.SellerId
#         }
#         response = self.client.post(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Book.objects.count(), 1)
#         self.assertEqual(Book.objects.get().Title, 'Test Book')
   