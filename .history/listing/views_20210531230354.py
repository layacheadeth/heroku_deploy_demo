from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import mixins
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import generics
from .models import Listing
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import ListingSerializer
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
# code below import Or condition
from django.db.models import Q
import math
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

# @api_view(['GET','POST'])
# def Listing_view(request):
#     if request.method=='GET':
#         listing=Listing.objects.all()
#         serializer=ListingSerializer(listing,many=True)
#         return Response(serializer.data)
#     elif request.method=='POST':
#         serializer=ListingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#




# class Listing_detail_1(APIView):
#     def get_object(self,id):
#         try:
#             return Listing.objects.get(id=id)
#         except Listing.DoesNotExist:
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self,request,id):
#         listing=self.get_object(id)
#         serializer=ListingSerializer(listing)
#         return Response(serializer.data)
#
#     def put(self,request,id):
#         listing=self.get_object(id)
#         serializer=ListingSerializer(listing,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,id):
#         listing=self.get_object(id)
#         listing.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#


# @api_view(['GET','POST','DELETE'])
# def Listing_detail(request,pk):
#     try:
#         listing_ind=Listing.objects.get(pk=pk)
#     except Listing.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#     if request.method=='GET':
#         serializer=ListingSerializer(listing_ind)
#         return Response(serializer.data)
#     elif request.method=='PUT':
#         serializer=ListingSerializer(listing_ind,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method=="DELETE":
#         listing_ind.delete()
#         return Response(satus=status.HTTP_204_NO_CONTENT)



# class Listing_view(ListAPIView):
#     queryset=Listing.objects.all()
#     serializer_class = ListingSerializer
#
#     # def post(self, request, *args, **kwargs):
#     #     file = request.data['file']
#     #     image = Listing.objects.create(image=file)
#     #     import json
#     #     return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
#
#
#
#
# class Listing_detail(RetrieveAPIView):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#     def put(self, request, id):
#         listing=self.get_object(id)
#         serializer=ListingSerializer(listing,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




    # lookup_field = 'members'




# class Listing_detail_1(ListAPIView):
#
#     def __init__(self, pk):
#         self.pk = pk
#         queryset = Listing.objects.get(pk=pk)
#         serializer_class = ListingSerializer

class Listing_view(generics.ListCreateAPIView):
    queryset=Listing.objects.order_by('-list_date').filter(is_published=True)
    serializer_class = ListingSerializer

class Listing_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing
    serializer_class = ListingSerializer

# class Listing_search(generics.RetrieveAPIView):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#     def get(self,request):
#         s=request.GET.get('s')
#         listing=Listing.objects.all()
#
#         if s:
#             listing=listing.filter(title__icontains=1)
#         serializer=ListingSerializer(listing,many=True)
#         return Response(serializer.data)

class Listing_search(APIView):

    def get(self,request):
        s=request.GET.get('s')
        sort=request.GET.get('sort')
        listing=Listing.objects.all()
        page=int(request.GET.get('page',1))
        per_page=3

        listing=Listing.objects.all()
        # it filters item using title and description. Use the string get from s and match it with the product with title and description
        # containing s string being given.
        if s:
            listing=listing.filter(Q(title__icontains=s)|Q(description__icontains=s))

        if sort=='asc':
            listing=listing.order_by('price')

        if sort =='desc':
            listing=listing.order_by('-price')

        total=listing.count()
        start=(page-1)*per_page
        end=page*per_page

        serializer=ListingSerializer(listing[start:end],many=True)
        return Response({
            'data':serializer.data,
            'total':total,
            'page':page,
            'last_page':math.ceil(total/per_page)
        })

# class Listing_searchs(generics.ListAPIView):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#     filter_backends = (SearchFilter,OrderingFilter)
#     search_fields=('title','address','city','description','price','realtor__name')
#     pagination_class = PageNumberPagination

class Listing_home(generics.ListCreateAPIView):
    queryset = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    serializer_class = ListingSerializer


class Listing_search_with_condition(APIView):

    def get(self,request):
        s=request.GET.get('s')
        num_room=request.GET.get('num_room')
        sort=request.GET.get('sort')
        price=request.GET.get('price')
        location=request.GET.get('location')
        sqft=request.GET.get('sqft')
        listing=Listing.objects.all()
        page=int(request.GET.get('page',1))
        per_page=3

        listing=Listing.objects.all()
        # it filters item using title and description. Use the string get from s and match it with the product with title and description
        # containing s string being given.
        if s:
            listing=listing.filter(Q(title__icontains=s)|Q(description__icontains=s))
        if num_room:
            listing = listing.filter(num_room__lte=num_room)
        if price:
            listing = listing.filter(price__lte=price)
        if location:
            listing = listing.filter(location__iexact=location)
        if sqft:
            listing = listing.filter(sqft__lte=sqft)

        if sort=='asc':
            listing=listing.order_by('price')

        if sort =='desc':
            listing=listing.order_by('-price')

        total=listing.count()
        start=(page-1)*per_page
        end=page*per_page

        serializer=ListingSerializer(listing[start:end],many=True)
        return Response({
            'data':serializer.data,
            'total':total,
            'page':page,
            'last_page':math.ceil(total/per_page)
        })











