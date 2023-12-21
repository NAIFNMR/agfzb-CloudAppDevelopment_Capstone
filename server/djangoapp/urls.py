from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),
    path(route='dealer/<int:dealer_id>/',view=views.get_dealer_by,name='dealer_id'),
    path(route='dealer/<str:dealer_state>/',view=views.get_dealer_by,name='dealer_state'),
    path(route='dealer_detail/<int:dealer_id>/',view=views.get_dealer_details,name='dealer_detail'),
    path(route='dealer/<int:dealer_id>/<str:review>', view= views.add_review, name='add_review')
    
    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)