from rest_framework import generics
from rest_framework.views import APIView
from App.models import User
from App.serializers import createUserSerializer,LoginSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#register the user / create the user 
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = createUserSerializer

#login the user    
class LoginUserView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                #check the password 
                if user.password == serializer.validated_data['password']:
                    token = Token.objects.get_or_create(user=user)
                    return Response({"success":True, "message":token[0].key})
                else:
                    return Response({"success":False, "message":"Incorrect Password"})
                
            except ObjectDoesNotExist:
                return Response({"success":False, "message":"User is not Exists"})
        
#get the user 
class RetriveUserView(generics.RetrieveAPIView):
    queryset =User.objects.all()
    serializer_class = createUserSerializer
    
#update the user 
class UpdateUserView(APIView):
    queryset = User.objects.all()
    serializer_class = createUserSerializer 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self,request):
        #get the serializer 
        serializer = self.serializer_class(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True, "message":"User is Updated"})
        else:
            print(serializer.errors)
            return Response({"success":False, "message":"Something is went wrong User is not updated"})
       
        

#destroy/ delete the user 
class DestroyUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = createUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes =[IsAuthenticated]
    
    def destroy(self,request,pk):
        try:
            user = User.objects.get(id=pk)
            #check the right person to do this work 
            if pk == request.user.id:
                self.perform_destroy(request.user)
                return Response({"success":True, "message":"User is Deleted Successfully"})
            else:
                return Response({"success":False, "message":"You are not allowed to do this!!!"})
        except ObjectDoesNotExist:
            return Response({"success":False, "message":"User doest not Found"})
        
        

    

            
                
    
    
    