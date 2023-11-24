"""
URL configuration for esite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from esite_app import views
from django.conf.urls.static import static
from esite import settings

urlpatterns = [

    path('data',views.data),
     path('about',views.about),           
    #path('contact',views.abc),
    #path('hello',views.hello)
    #path('edit/<abc>',views.edit),
    path('hello',views.hello),
    #  pass dynamic code
    path('pdetails/<pid>',views.product_details),
    path('register',views.register),
    path('contact',views.contact),
    path('about',views.about),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('addtocart/<pid>',views.addtocart),
    path('range',views.range),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail/<uemail>',views.sendusermail),
]
if settings.DEBUG:
   urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)