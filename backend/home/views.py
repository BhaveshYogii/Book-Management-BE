from home.serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.models import Session
from django.utils import timezone
import json
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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
        return Response({"error":serializer.errors},status=400)


@csrf_exempt
@api_view(['POST'])
def sellersignup(request):

    data=request.data.copy()
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId
    data["UserObj"]=userId
    
    if(userObj.Role!="Seller"):  
        serializer = SellerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            sellerObj=Seller.objects.filter(UserObj=userObj)[0]
            request=Request.objects.create(SellerObj=sellerObj)
            return Response({"message":"Request sent"},status=201)
        else:
            return Response({"error":serializer.errors},status=400)
    else:
        return Response({"error":"Already a seller"},status=400)
    


@csrf_exempt
@api_view(['POST'])
def sellerregister(request):
    session_key=request.data["session_key"]
    sellerId=request.data["sellerId"]

    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
        }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]

    if(userObj.Role!="Admin"):
        return Response({"error":"You are not admin"},status=400)
    
    if(not Seller.objects.filter(SellerId=sellerId)):
        return Response({"error":"Seller Does Not Exist"},status=400)
    
    sellerObj=Seller.objects.filter(SellerId=sellerId)[0]
    sellerUserObj=sellerObj.UserObj
    if(not Request.objects.filter(SellerObj=sellerObj)):
        return Response({"error":"Request Does Not Exist"},status=400)
    
    request=Request.objects.filter(SellerObj=sellerObj)
    if(request[0].Status=="Pending"):
        return Response({"error":"Request is in pending state"},status=200)
    elif(request[0].Status=="Accepted"):
        sellerUserObj.Role="Seller"
        sellerUserObj.save()
        return Response({"message":"Registered as Seller"},status=200)
    else:
        sellerUserObj.Role="Buyer"
        sellerUserObj.save()
        request.delete()
        Seller.objects.filter(SellerId=sellerId).delete()
        return Response({"error":"Request Declined"},status=200)


@csrf_exempt
@api_view(['POST'])
def getrequeststatus(request):
    data=request.data.copy()
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId
    data["UserObj"]=userId

    if(not Seller.objects.filter(UserObj=userObj)):
        return Response({"error":"Seller Does Not Exist"},status=400)
    sellerObj=Seller.objects.filter(UserObj=userObj)[0]
    if(not Request.objects.filter(SellerObj=sellerObj)):
        return Response({"error":"Request Does Not Exist"},status=400)
    request=Request.objects.filter(SellerObj=sellerObj)[0]
    response={
        "message": request.Status,
    }
    return Response(response,status=200)

@csrf_exempt
@api_view(['POST'])
def signin(request):
    response={}
    if request.data['Email']=='':
        response['success']=False
        response['error']='Email Id required'
        return Response(response,status.HTTP_400_BAD_REQUEST)
    
    if request.data['Password']=='':
        response['success']=False
        response['error']='Password required'
        return Response(response,status.HTTP_400_BAD_REQUEST)
    
    Email=request.data['Email']
    Password=request.data['Password']
    user=User.objects.filter(Email=Email).first()
    if not user:
        response={
        "success": False,
        "error": "User does not exist",
        }
        return Response(response,status.HTTP_401_UNAUTHORIZED)
    
    if Email == user.Email and check_password(Password, user.Password):
        request.session['Email'] = Email
        request.session.create()
        session_key = request.session.session_key

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
            "error": "Invalid credentials",
        }
    return Response(response,status=401)
    
@csrf_exempt
@api_view(['POST'])
def getbooks(request):
    key=request.data["Key"]
    way=request.data["Order"]
    limit=int(request.data["Limit"])
    temp=""
    if(way=="AESC"):
        temp=key
    else:
        temp+="-"
        temp+=key
    
    if(limit==-1):
        data = Book.objects.all().order_by(temp)
    else:
        data = Book.objects.all().order_by(temp)[:limit]
        
    serializer = BookSerializer(data,many=True)
    return Response({"list":serializer.data},status=200)


@csrf_exempt
@api_view(['POST'])
def uploadbook(request):
    data=request.data.copy()
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    
    if(not Seller.objects.filter(UserObj=userObj)):
        return Response({"error":"Seller Does Not Exist"},status=400)
    
    seller=Seller.objects.filter(UserObj=userObj)[0]
    if(Book.objects.filter(SellerObj=seller,Title=request.data["Title"])):
        return Response({"error":"Book with this title is already present"},status=400)

    
    serializer = BookSerializer(data=data)

    data["SellerObj"]=seller.SellerId

    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Book created successfully"},status=201)
    else:
        return Response({"error":serializer.errors},status=400)
    
@csrf_exempt
@api_view(['POST'])
def addtocart(request):
    bookId=request.data["BookObj"]
    totalQuantity=int(request.data["TotalQuantity"])
    session_key=request.data["session_key"]
    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId
    if(not User.objects.filter(UserId=userId)):
        return Response({"error":"User Does Not Exist"},status=400)
    user=User.objects.filter(UserId=userId)[0]
    if(not Book.objects.filter(BookId=bookId)):
        return Response({"error":"Book Does Not Exist"},status=400)
    book=Book.objects.filter(BookId=bookId)[0]
    if(totalQuantity<=0):
        return Response({"error":"Please select atleast one book"},status=400)
    cart=Cart.objects.filter(UserObj=user)[0]
    if(not CartElement.objects.filter(CartObj=cart,BookObj=book)):
        CartElement.objects.create(CartObj=cart,BookObj=book,ElementQuantity=totalQuantity)
        cart.TotalQuantity+=totalQuantity
        cart.save()
        return Response({"message":"Book added successfully"},status=201)
    else:
        return Response({"error":"Book already in cart"},status=400)
    

@csrf_exempt
@api_view(['POST'])
def addtolist(request):
    bookId=request.data["BookObj"]
    session_key=request.data["session_key"]
    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId
    if(not User.objects.filter(UserId=userId)):
        return Response({"error":"User Does Not Exist"},status=400)
    user=User.objects.filter(UserId=userId)[0]
    if(not Book.objects.filter(BookId=bookId)):
        return Response({"error":"Book Does Not Exist"},status=400)
    book=Book.objects.filter(BookId=bookId)[0]
    list=WishList.objects.filter(UserObj=user)[0]
    if(not WishListElement.objects.filter(ListObj=list,BookObj=book)):
        WishListElement.objects.create(ListObj=list,BookObj=book)
        list.TotalQuantity+=1
        list.save()
        return Response({"message":"Book added successfully"},status=201)
    else:
        return Response({"error":"Book already in wishlist"},status=400)

@csrf_exempt
@api_view(['DELETE'])
def deletefromlist(request):
    bookId=request.data["BookObj"]
    session_key=request.data["session_key"]

    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId

    if(not User.objects.filter(UserId=userId)):
        return Response({"error":"User Does Not Exist"},status=400)
    
    user=User.objects.filter(UserId=userId)[0]
    if(not Book.objects.filter(BookId=bookId)):
        return Response({"error":"Book Does Not Exist"},status=400)
    
    book=Book.objects.filter(BookId=bookId)[0]

    list=WishList.objects.filter(UserObj=user)[0]
    
    if(not WishListElement.objects.filter(ListObj=list,BookObj=book)):
        return Response({"error":"Book not present in wishlist"},status=201)
    
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
                "error": "Please login"
            }
        return Response(response,status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId

    if(not User.objects.filter(UserId=userId)):
        return Response({"error":"User Does Not Exist"},status=400)
    
    user=User.objects.filter(UserId=userId)[0]
    if(not Book.objects.filter(BookId=bookId)):
        return Response({"error":"Book Does Not Exist"},status=400)
    
    book=Book.objects.filter(BookId=bookId)[0]

    cart=Cart.objects.filter(UserObj=user)[0]
    if(not CartElement.objects.filter(CartObj=cart,BookObj=book)):
        return Response({"error":"Book not present in cart"},status=201)
    
    queryset=CartElement.objects.filter(CartObj=cart,BookObj=book)
    quantity=queryset[0].ElementQuantity
    queryset.delete()
    cart.TotalQuantity-=quantity
    cart.save()
    if(moveToList==1):
        list=WishList.objects.filter(UserObj=user)[0]
        if(not WishListElement.objects.filter(ListObj=list,BookObj=book)):
            WishListElement.objects.create(ListObj=list,BookObj=book)
            list.TotalQuantity+=1
            list.save()
        return Response({"message":"Book sent to wishlist successfully"},status=201)

    return Response({"message":"Book removed from cart successfully"},status=201)


@csrf_exempt
@api_view(['POST'])
def placeorder(request):
    session_key=request.data["session_key"]
    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId
    if(not User.objects.filter(UserId=userId)):
        return Response({"error":"User Does Not Exist"},status=400)
    user=User.objects.filter(UserId=userId)[0]
    cart=Cart.objects.filter(UserObj=user)[0]
    order = Order.objects.create(UserObj=user , TotalQuantity=cart.TotalQuantity , TotalAmount=0)
    allcartelement = CartElement.objects.filter(CartObj=cart)
    sum=0
    for i in allcartelement.values():
        book=Book.objects.filter(BookId=i.get('BookObj_id'))[0]
        elementQuantity=i.get('ElementQuantity')
        price=(book.Price) * (elementQuantity)
        book.SoldQuantity+=elementQuantity
        book.save()
        sum+=price
        OrderElement.objects.create(OrderObj=order , BookObj=book , ElementQuantity=i.get('ElementQuantity'), ElementTotalPrice=price )
    
    order.TotalAmount=sum
    order.save()
    CartElement.objects.filter(CartObj=cart).delete()
    cart.TotalQuantity=0
    cart.save()
    return Response({"message":"Order Placed successfully"},status=201)



@api_view(['POST'])
def logout(request):
    
    session=Session.objects.get(session_key=request.data["session_key"])
    response={
        "success": True,
        "message": "Session Deleted succesfully!"
    }
    if session is None:
        response['success']=False,
        response['error']='User not found!'
        return Response(response,status.HTTP_404_NOT_FOUND)
    session.delete()
    return Response(response,status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['Post'])
def searchbook(request):
    try:
        search_term = request.POST.get('searchTerm')
        if search_term:
            matched_books = Book.objects.filter(Title__icontains=search_term) | Book.objects.filter(Author__icontains=search_term)
            serializer = BookSerializer(matched_books,many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Search term is required'}, status=400)
    except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON data'}, status=400)
    

@csrf_exempt
@api_view(['Post'])
def getcartelements(request):
    session_key=request.data["session_key"]
    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    user=User.objects.filter(Email=email)[0]
    userId=user.UserId
    cart=Cart.objects.filter(UserObj=user)[0]
    allcartelement = CartElement.objects.filter(CartObj=cart).order_by("BookObj")
    serializer = CartElementSerializer(allcartelement, many=True)

    for i in serializer.data:
        tempbookid=i['BookObj']
        tempbook=Book.objects.filter(BookId=tempbookid)[0]
        bookSerializer=BookSerializer(tempbook)
        i['BookObj']=bookSerializer.data


    cartSerializer=CartSerializer(cart)
    response={
        "BookData": serializer.data,
        "CartData": cartSerializer.data,
    }
    return Response(response,status=200)


@csrf_exempt
@api_view(['POST'])
def updatecart(request):
    bookId=request.data["BookId"]
    new_quantity=request.data["new_quantity"]
    session_key=request.data["session_key"]
    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    userId=userObj.UserId
    if(not User.objects.filter(UserId=userId)):
        return Response({"error":"User Does Not Exist"},status=400)
    user=User.objects.filter(UserId=userId)[0]
    if(not Book.objects.filter(BookId=bookId)):
        return Response({"error":"Book Does Not Exist"},status=400)
    book=Book.objects.filter(BookId=bookId)[0]
    cart=Cart.objects.filter(UserObj=user)[0]
    if(not CartElement.objects.filter(CartObj=cart,BookObj=book)):
        return Response({"error":"Book not present in cart"},status=201)
    queryset=CartElement.objects.filter(CartObj=cart,BookObj=book)
    if queryset.exists():
       quantity = queryset[0].ElementQuantity
       queryset.update(ElementQuantity=int(new_quantity))
       cart.TotalQuantity -= quantity
       cart.TotalQuantity += int(new_quantity)
       cart.save()
    
    return Response({"message":"Quantity updated"},status=201)


@api_view(['POST'])
def getrole(request):
    session_key=request.data["session_key"]
    if(not validation(session_key)):
        response={
                "success": False,
                "error": "Please login"
            }
        return Response(response,status=401)
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]
    response={
        "role":userObj.Role,
        "success":True,
    }
    return Response(response,status=200)

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

    orders = Order.objects.filter(UserObj=userId)
    orderSerializer = OrderSerializer(orders, many=True)

    list=[]
    for i in orderSerializer.data:
        orderId=i['OrderId']
        order=Order.objects.filter(OrderId=orderId)[0]
        orderElements=OrderElement.objects.filter(OrderObj=order)
        orderElementsSerializer=OrderElementSerializer(orderElements,many=True)
        
        for j in orderElementsSerializer.data:
            bookId=j['BookObj']
            book=Book.objects.filter(BookId=bookId)[0]
            bookSerializer=BookSerializer(book)
            j['BookData']=bookSerializer.data

        i['OrderElements']=orderElementsSerializer.data
        list.append(i)

    response={
        "Data": list,
    }
    return Response(response, status=200)



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
    

    for i in serializer.data:
        tempbookid=i['BookObj']
        tempbook=Book.objects.filter(BookId=tempbookid)[0]
        bookSerializer=BookSerializer(tempbook)
        i['BookObj']=bookSerializer.data

    listSerializer=wishListSerializer(wishlist)
    response={
        "BookData": serializer.data,
        "ListData": listSerializer.data,
    }
    return Response(response,status=200)   



@csrf_exempt
@api_view(['Post'])
def generate_pdf_invoice(request):
    # Create a response object with PDF MIME type
    OrderId=request.data['orderId']
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

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_order_{OrderId}.pdf'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    order=Order.objects.filter(OrderId=OrderId)[0]


    # Create data for the table
    data = [['Book', 'Quantity', 'Total Price']]
    for order_element in OrderElement.objects.filter(OrderObj=order):
        data.append([
            order_element.BookObj.Title,
            order_element.ElementQuantity,
            f'Rs{order_element.ElementTotalPrice}'
        ])

     # Add additional information as Paragraph objects
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f'<para>Invoice for Order #{order.OrderId}</para>', styles['Title']))
    elements.append(Paragraph(f'<para>Order Date: {order.PlacedTime.strftime("%Y-%m-%d %H:%M:%S")}</para>', styles['Normal']))
    elements.append(Paragraph(f'<para>Total Quantity: {order.TotalQuantity}</para>', styles['Normal']))
    elements.append(Paragraph(f'<para>Total Amount: Rs{order.TotalAmount}</para>', styles['Normal']))    

    # Create the table and apply styles
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    elements.append(table)

   

    # Build the PDF document
    doc.build(elements)

    return response


@csrf_exempt
@api_view(['POST'])
def admingetbooks(request):
    session_key = request.data.get("session_key")

    if not validation(session_key):
        response = {
            "success": False,
            "message": "Please login"
        }
        return Response(response, status=401)

    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response({"books": serializer.data}, status=200)


@csrf_exempt
@api_view(['POST'])
def admingetusers(request):
    session_key = request.data.get("session_key")

    if not validation(session_key):
        response = {
            "success": False,
            "message": "Please login"
        }
        return Response(response, status=401)

    users = User.objects.all().order_by("UserId")
    serializer = UserSerializer(users, many=True)
    return Response({"users": serializer.data}, status=200)


@csrf_exempt
@api_view(['POST'])
def admingetrequests(request):
    session_key = request.data.get("session_key")

    if not validation(session_key):
        response = {
            "success": False,
            "message": "Please login"
        }
        return Response(response, status=401)

    requests = Request.objects.all().order_by("RequestId")

    serializer = RequestSerializer(requests, many=True)
    for i in serializer.data:
        Sellerid=i['SellerObj']
        seller=Seller.objects.filter(SellerId=Sellerid)[0]
        sellerSerializer=SellerSerializer(seller)
        i['SellerObj']=sellerSerializer.data
        userid= sellerSerializer.data['UserObj']
        user=User.objects.filter(UserId=userid)[0]
        userserializer=UserSerializer(user)
        i['SellerObj']['UserObj']=userserializer.data
    
    return Response({"Request": serializer.data}, status=200)


@csrf_exempt
@api_view(['POST'])
def adminupdaterequests(request):
    session_key = request.data.get("session_key")
    requestId=request.data.get("requestId")
    status=request.data.get("status")

    if not validation(session_key):
        response = {
            "success": False,
            "message": "Please login"
        }
        return Response(response, status=401)
    
    if(not Request.objects.filter(RequestId=requestId)):
        return Response({"error":"Request Not Exist"},status=400)
    
    request=Request.objects.filter(RequestId=requestId)[0]
    request.Status=status
    request.save()
    return Response({"message":"Status updated"},status=201)


@csrf_exempt
@api_view(['POST'])
def sellergetbooks(request):
    session_key = request.data.get("session_key")


    if not validation(session_key):
        response = {
            "success": False,
            "message": "Please login"
        }
        return Response(response, status=401)
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email=session_data['Email']
    userObj=User.objects.filter(Email=email)[0]

    if(not Seller.objects.filter(UserObj=userObj)):
       return Response({"error":"Seller Does Not Exist"},status=400)
    
    seller=Seller.objects.filter(UserObj=userObj)[0]

    books = Book.objects.filter(SellerObj=seller)
    serializer = BookSerializer(books, many=True)
    return Response({"books": serializer.data}, status=200) 

@csrf_exempt
@api_view(['POST'])
def sellerupdatebook(request):
    session_key = request.data.get("session_key")
    bookid=request.data.get("BookId")

    if not validation(session_key):
        response = {
            "success": False,
            "message": "Please login"
        }
        return Response(response, status=401)


    if(not Book.objects.get(BookId=bookid)):
        return Response({"error":"Book Does Not Exist"},status=400)    
    book = Book.objects.get(BookId=bookid)
    
    
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    email = session_data['Email']
    userObj = User.objects.get(Email=email)

    if(not Seller.objects.filter(UserObj=userObj)):
       return Response({"error":"You are not a seller"},status=400)
    
    seller=Seller.objects.filter(UserObj=userObj)[0]

    if book.SellerObj != seller:
        return Response({"error": "You are not authorized to update this book"}, status=403)
    
    
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Book updated successfully"}, status=200)
    else:
        return Response(serializer.errors, status=400)

