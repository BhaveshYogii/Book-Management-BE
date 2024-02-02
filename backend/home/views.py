from django.shortcuts import render
from home.serializers import *
# Create your views here.

@csrf_exempt
@api_view(['POST'])
def signup(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Sucess":"User created successfully"},status=201)
    else:
        return Response({"Failed":serializer.errors},status=400)



@csrf_exempt
@api_view(['POST'])
def sellersignup(request):
    data = request.data
    serializer = SellerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Sucess":"Seller created successfully"},status=201)
    else:
        return Response({"Failed":serializer.errors},status=400)



@csrf_exempt
@api_view(['POST'])
def signin(request):
    if 'Email' not in request.data:
        response['success']=False
        response['message']='email id required'
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
        response={
            "success": True,
            "message": "User successfully authenticated"
        }
        if(not Cart.objects.filter(UserObj=user)):
            Cart.objects.create(UserObj=user,TotalQuantity=0)

        if(not WishList.objects.filter(UserObj=user)):
            WishList.objects.create(UserObj=user,TotalQuantity=0)

        return Response(response,status.HTTP_200_OK)
    else:
        response={
            "success": False,
            "message": "Invalid credentials",
        }
    return Response(response,status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET'])
def getbooks(request):
    data = getbooks.objects.all()
    serializer = BookSerializer(data,many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def uploadbook(request):
    data = request.data
    serializer = BookSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Sucess":"Book created successfully"},status=201)
    else:
        return Response({"Failed":serializer.errors},status=400)    