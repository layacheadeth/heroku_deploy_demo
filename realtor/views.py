from django.shortcuts import render
from django.http import HttpResponse
from .models import Realtor
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import RealtorSerializer
from rest_framework.generics import ListAPIView,RetrieveAPIView

# @api_view(['GET','POST'])
# def Realtor_view(request):
#     if request.method=='GET':
#         realtor=Realtor.objects.all()
#         serializer=RealtorSerializer(realtor,many=True)
#         return Response(serializer.data)
#     elif request.method=='POST':
#         serializer=RealtorSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
@api_view(['GET','POST','DELETE'])
def Realtor_detail(request,pk):
    try:
        realtor_ind=Realtor.objects.get(pk=pk)
    except Realtor.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=RealtorSerializer(realtor_ind)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=RealtorSerializer(realtor_ind,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=="DELETE":
        realtor_ind.delete()
        return Response(satus=status.HTTP_204_NO_CONTENT)
class Realtor_view(ListAPIView):
    queryset=Realtor.objects.all()
    serializer_class = RealtorSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     file = request.data['file']
    #     image = Realtor.objects.create(image=file)
    #     import json
    #     return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)

class Realtor_detail(RetrieveAPIView):
    queryset = Realtor.objects.all()
    serializer_class = RealtorSerializer
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, id):
        listing=self.get_object(id)
        serializer=RealtorSerializer(listing,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

