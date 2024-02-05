from home.serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def index(request):
    return Response({"message":"Home"},status=201)

def validation(data):
    session_key=data
    if session_key=="":
        return False
    queryset=Session.objects.filter(session_key=session_key)
    if len(queryset)>0:
        temp=queryset[0]
        if queryset[0].expire_date<timezone.now():
            return False
        if temp.session_key==session_key:
            return True 
    return False


@csrf_exempt
@api_view(['POST'])
def signup(request):
    data = request.data
    
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User created successfully"},status=201)
    else:
        return Response({"Failed":serializer.errors},status=400)


@csrf_exempt
@api_view(['POST'])
def sellersignup(request):

    data=request.data.copy()
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId
    data["UserObj"]=userId
    serializer = SellerSerializer(data=data)
   
    if serializer.is_valid():
        serializer.save()
        userObj=User.objects.filter(UserId=userId)[0]
        sellerObj=Seller.objects.filter(UserObj=userObj)[0]
        if(userObj.Role!="Seller"):
            request=Request.objects.create(SellerObj=sellerObj)
            return Response({"message":"Request sent"},status=201)
        else:
            return Response({"message":"Already a seller"},status=201)
    else:
        return Response({"Failed":serializer.errors},status=400)


@csrf_exempt
@api_view(['POST'])
def sellerregister(request):
    data=request.data.copy()
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
        }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId
    data["UserObj"]=userId

    if(not Seller.objects.filter(UserObj=userObj)):
        return Response({"message":"Seller Does Not Exist"},status=400)
    sellerObj=Seller.objects.filter(UserObj=userObj)[0]
    if(not Request.objects.filter(SellerObj=sellerObj)):
        return Response({"message":"Request Does Not Exist"},status=400)
    request=Request.objects.filter(SellerObj=sellerObj)[0]

    if(request.Status=="Pending"):
        return Response({"message":"Request is in pending state"},status=200)
    elif(request.Status=="Accepted"):
        userObj.Role="Seller"
        userObj.save()
        return Response({"message":"Registered as Seller"},status=200)
    else:
        userObj.Role="Buyer"
        userObj.save()
        Seller.objects.filter(UserObj=userObj).delete()
        return Response({"message":"Request Declined"},status=200)


@csrf_exempt
@api_view(['POST'])
def getrequeststatus(request):
    data=request.data.copy()
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId
    data["UserObj"]=userId

    if(not Seller.objects.filter(UserObj=userObj)):
        return Response({"message":"Seller Does Not Exist"},status=400)
    sellerObj=Seller.objects.filter(UserObj=userObj)[0]
    if(not Request.objects.filter(SellerObj=sellerObj)):
        return Response({"message":"Request Does Not Exist"},status=400)
    request=Request.objects.filter(SellerObj=sellerObj)[0]
    response={
        "data":request.Status,
    }
    return Response(response,status=200)

@csrf_exempt
@api_view(['POST'])
def signin(request):
    response={}
    if request.data['Email']=='':
        response['success']=False
        response['message']='Email Id required'
        return Response(response,status.HTTP_400_BAD_REQUEST)
    if request.data['Password']=='':
        response['success']=False
        response['message']='Password required'
        return Response(response,status.HTTP_400_BAD_REQUEST)
    
    Email=request.data['Email']
    Password=request.data['Password']
    user=User.objects.filter(Email=Email).first()
    if not user:
        response={
        "success": False,
        "message": "User does not exist",
        }
        return Response(response,status.HTTP_401_UNAUTHORIZED)
    
    if Email == user.Email and check_password(Password, user.Password):
        request.session['Email'] = Email
        request.session.create()
        session_key = request.session.session_key
        print(session_key)

        response={
            "success": True,
            "message": "User successfully authenticated",
            "session_key":session_key,
        }

        if(not Cart.objects.filter(UserObj=user)):
            Cart.objects.create(UserObj=user,TotalQuantity=0)

        if(not WishList.objects.filter(UserObj=user)):
            WishList.objects.create(UserObj=user,TotalQuantity=0)

        return Response(response,status=200)
    else:
        response={
            "success": False,
            "message": "Invalid credentials",
        }
    return Response(response,status=401)
    
@csrf_exempt
@api_view(['POST'])
def getbooks(request):
    key=request.data["Key"]
    data = Book.objects.all().order_by(key)
    serializer = BookSerializer(data,many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def uploadbook(request):
    data=request.data.copy()
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    
    if(not Seller.objects.filter(UserObj=userObj)):
        return Response({"message":"Seller Does Not Exist"},status=400)
    
    serializer = BookSerializer(data=data)

    seller=Seller.objects.filter(UserObj=userObj)[0]
    data["SellerObj"]=seller.SellerId

    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Book created successfully"},status=201)
    else:
        return Response({"Failed":serializer.errors},status=400)
    
@csrf_exempt
@api_view(['POST'])
def addtocart(request):
    
    bookId=request.data["BookObj"]
    totalQuantity=int(request.data["TotalQuantity"])
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId

    if(not User.objects.filter(UserId=userId)):
        return Response({"message":"User Does Not Exist"},status=400)
    
    user=User.objects.filter(UserId=userId)[0]
    if(not Book.objects.filter(BookId=bookId)):
        return Response({"message":"Book Does Not Exist"},status=400)
    
    book=Book.objects.filter(BookId=bookId)[0]
    if(totalQuantity<=0):
        return Response({"message":"Please select atleast one book"},status=400)
    
    
    cart=Cart.objects.filter(UserObj=user)[0]
    CartElement.objects.create(CartObj=cart,BookObj=book,ElementQuantity=totalQuantity)
    cart.TotalQuantity+=totalQuantity
    cart.save()
    return Response({"message":"Book added successfully"},status=201)

@csrf_exempt
@api_view(['POST'])
def addtolist(request):
    bookId=request.data["BookObj"]
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId

    if(not User.objects.filter(UserId=userId)):
        return Response({"message":"User Does Not Exist"},status=400)
    
    user=User.objects.filter(UserId=userId)[0]
    if(not Book.objects.filter(BookId=bookId)):
        return Response({"message":"Book Does Not Exist"},status=400)
    
    book=Book.objects.filter(BookId=bookId)[0]
    
    
    list=WishList.objects.filter(UserObj=user)[0]
    WishListElement.objects.create(ListObj=list,BookObj=book)
    list.TotalQuantity+=1
    list.save()
    return Response({"message":"Book added successfully"},status=201)


@csrf_exempt
@api_view(['DELETE'])
def deletefromlist(request):
    bookId=request.data["BookObj"]
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId

    if(not User.objects.filter(UserId=userId)):
        return Response({"message":"User Does Not Exist"},status=400)
    
    user=User.objects.filter(UserId=userId)[0]
    if(not Book.objects.filter(BookId=bookId)):
        return Response({"message":"Book Does Not Exist"},status=400)
    
    book=Book.objects.filter(BookId=bookId)[0]

    list=WishList.objects.filter(UserObj=user)[0]
    
    if(not WishListElement.objects.filter(ListObj=list,BookObj=book)):
        return Response({"message":"Book not present in wishlist"},status=201)
    
    WishListElement.objects.filter(ListObj=list,BookObj=book).delete()
    list.TotalQuantity-=1
    list.save()
    return Response({"message":"Book removed from wishlist successfully"},status=201)



@csrf_exempt
@api_view(['DELETE'])
def deletefromcart(request):
    moveToList=request.data["MoveToList"]
    bookId=request.data["BookObj"]
    
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId

    if(not User.objects.filter(UserId=userId)):
        return Response({"message":"User Does Not Exist"},status=400)
    
    user=User.objects.filter(UserId=userId)[0]
    if(not Book.objects.filter(BookId=bookId)):
        return Response({"message":"Book Does Not Exist"},status=400)
    
    book=Book.objects.filter(BookId=bookId)[0]

    cart=Cart.objects.filter(UserObj=user)[0]
    if(not CartElement.objects.filter(CartObj=cart,BookObj=book)):
        return Response({"message":"Book not present in cart"},status=201)
    
    queryset=CartElement.objects.filter(CartObj=cart,BookObj=book)
    quantity=queryset[0].ElementQuantity
    queryset.delete()
    cart.TotalQuantity-=quantity
    cart.save()

    if(moveToList):
        list=WishList.objects.filter(UserObj=user)[0]
        if(not WishListElement.objects.filter(ListObj=list,BookObj=book)):
            WishListElement.objects.create(ListObj=list,BookObj=book)
            list.TotalQuantity+=1
            list.save()
        return Response({"message":"Book sent to wishlist successfully"},status=201)

    return Response({"message":"Book removed from cart successfully"},status=201)

@csrf_exempt
@api_view(['Post'])
def getcartelements(request):
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    user=User.objects.filter(Email=email)[0]
    userId=user.UserId

    cart=Cart.objects.filter(UserObj=user)[0]
    allcartelement = CartElement.objects.filter(CartObj=cart)
    serializer = CartElementSerializer(allcartelement, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def placeorder(request): 
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId

    if(not User.objects.filter(UserId=userId)):
        return Response({"message":"User Does Not Exist"},status=400)
    
    user=User.objects.filter(UserId=userId)[0]
 
    cart=Cart.objects.filter(UserObj=user)[0]
    order = Order.objects.create(UserObj=user , TotalQuantity=cart.TotalQuantity , TotalAmount=0)
    allcartelement = CartElement.objects.filter(CartObj=cart)
    sum=0
    for i in allcartelement.values():  
        print(i)  
        print(i.get('BookObj_id'))
        book=Book.objects.filter(BookId=i.get('BookObj_id'))[0]
        price=(book.Price) * (i.get('ElementQuantity'))
        sum+=price            
        # book=i.BookObj.filter(BookId=)
        OrderElement.objects.create(OrderObj=order , BookObj=book , ElementQuantity=i.get('ElementQuantity'), ElementTotalPrice=price )
    order.TotalAmount=sum
    order.save()   

    CartElement.objects.filter(CartObj=cart).delete()
    cart.TotalQuantity=0
    cart.save()
    return Response({"message":"Order Placed successfully"},status=201)

@csrf_exempt
@api_view(['Post'])
def getwishlistelements(request):
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    user=User.objects.filter(Email=email)[0]
    userId=user.UserId

    wishlist=WishList.objects.filter(UserObj=user)[0]
    alllistelement = WishListElement.objects.filter(ListObj=wishlist)
    serializer = ListElementSerializer(alllistelement, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['Post'])
def getorderelements(request):
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "message": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    user=User.objects.filter(Email=email)[0]
    userId=user.UserId

    recent_order = Order.objects.filter(UserObj=userId).order_by('PlacedTime').first()

    if not recent_order:
        response = {
            "success": False,
            "message": "No orders found for the user"
        }
        return Response(response, status=404)

    # Generate a PDF invoice for the recent order
    pdf_response = generate_pdf_invoice(recent_order)

    return pdf_response

def generate_pdf_invoice(order):
    # Create a response object with PDF MIME type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_order_{order.OrderId}.pdf'

    # Create a PDF object using reportlab
    p = canvas.Canvas(response)
    
    # Add content to the PDF based on your Order and OrderElement models
    p.drawString(100, 800, f'Invoice for Order #{order.OrderId}')
    p.drawString(100, 780, f'Order Date: {order.PlacedTime.strftime("%Y-%m-%d %H:%M:%S")}')
    p.drawString(100, 760, f'Total Quantity: {order.TotalQuantity}')
    p.drawString(100, 740, f'Total Amount: Rs{order.TotalAmount}')

    # Add information about order elements
    y_position = 720
    for order_element in OrderElement.objects.filter(OrderObj=order):
        p.drawString(120, y_position, f'Book: {order_element.BookObj.Title}')
        p.drawString(140, y_position - 20, f'Quantity: {order_element.ElementQuantity}')
        p.drawString(160, y_position - 40, f'Total Price: Rs{order_element.ElementTotalPrice}')
        y_position -= 60

    # Save the PDF
    p.save()
    return response