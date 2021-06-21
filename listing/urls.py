from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


# routers=DefaultRouter()
# routers.register('listings/',Listing_view)

urlpatterns = [
    path('listings/<int:pk>/',Listing_detail.as_view()),
    # path('listings/<int:pk>/',Listing_detail_1.as_view()),
    # path('listings/',Listing_view),
    path('listings/',Listing_view.as_view()),
    path('listings/search',Listing_search.as_view()),
    # path('listings/searchs',Listing_searchs.as_view()),
    path('listings/home',Listing_home.as_view())

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)