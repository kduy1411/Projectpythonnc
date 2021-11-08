from .serializers import DroneSerializer, CategorySerializer
from rest_framework import permissions
from rest_framework import viewsets
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER
from cart.forms import CartAddDroneForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models
from django.db.models import Count, F, Value
from django.contrib.auth import authenticate, login, logout
import json
import urllib.request

DEFAULT_ENCODING = 'utf-8'

# rest_framework

from django.contrib.auth.decorators import login_required
import datetime
now = datetime.datetime.now()
from . import forms

category_list = models.Category.objects.all()

category = 0
search_str = ''


def index(request):    
   username = request.session.get('username', 0)
 
   drone_list = models.Drone.objects.order_by("-public_day")
   most_viewed_list = models.Drone.objects.order_by("-viewed")[:3]
   newest = drone_list[0]
   twenty_newest = drone_list[:20]

   return render(request, "store/index.html",
                 {'newest': newest,
                  'twenty_newest': twenty_newest,
                  'most_viewed_list': most_viewed_list,
                  'categories': category_list,
                  
                  'username': username
                  })
    




def about(request):
    return render(request, 'store/about.html')


def shop(request, pk):
    username = request.session.get('username', 0)
    category = pk
    drone_list = []
    category_name = ''
    if pk != 0:
        drone_list = models.Drone.objects.filter(
            category=pk).order_by("-public_day")
        selected_category = models.Category.objects.get(pk=pk)
        category_name = selected_category.name
    else:
        drone_list = models.Drone.objects.order_by("-name")

    three_newest = drone_list[:3]

    page = request.GET.get('page', 1)  # trang bat dau
    paginator = Paginator(drone_list, 9)  # so product/trang

    try:
        drones = paginator.page(page)
    except PageNotAnInteger:
        drones = paginator.page(1)
    except EmptyPage:
        drones = paginator.page(paginator.num_pages)

    return render(request, "store/shop.html",
                  {'three_newest': three_newest,
                   'subcategories': category_list,
                   'pk': pk,
                   'drones': drones,
                   'categories': category_list,
                   'category_name': category_name,
                   'username': username
                   })


def search_form(request):
    username = request.session.get('username', 0)
    global category
    global search_str
    drone_items = 0
    three_newest = models.Drone.objects.all().order_by("-public_day")[:3]
    drone_list = []
    if request.method == 'GET':
        form = forms.FormSearch(request.GET, models.Drone)

        if form.is_valid():
            category = form.cleaned_data['category_id']
            search_str = form.cleaned_data['name']
            if category != 0:
                drone_list = models.Drone.objects.filter(
                    category=category, name__contains=search_str).order_by("-public_day")
            else:
                drone_list = models.Drone.objects.filter(
                    name__contains=search_str).order_by("-public_day")

            drone_items = len(drone_list)
            page = request.GET.get('page', 1)
            paginator = Paginator(drone_list, 9)
            try:
                drones = paginator.page(page)
            except PageNotAnInteger:
                drones = paginator.page(1)
            except EmptyPage:
                drones = paginator.page(paginator.num_pages)

        return render(request, "store/shop.html",
                      {'three_newest': three_newest,
                       'categories': category_list,
                       'drones': drones,
                       'pk': category,
                       'categories': category_list,
                       'drone_items': drone_items,
                       'category': category,
                       'search_str': search_str,
                       'username': username
                       })



def filter_by_prices(request):
    username = request.session.get('username', 0)
    global category
    global search_str
    drone_items = 0
    
    drone_list = models.Drone.objects.all().order_by("price")
   
    result = "chua nhan gi ca"
    three_newest = models.Drone.objects.all().order_by("-public_day")[:3]
    if request.method == 'GET':
        result = "da nhan GET"
        category = request.GET.get('category_id_1')
        x = 'yes'
        if request.GET.get('name_1'):
            search_str = request.GET.get('name_1')
        else:
            search_str = ''
            x = 'no'
        a = float(request.GET.get('price_from'))
        b = float(request.GET.get('price_to'))
        price_from = a
        price_to = b
        if(a > b):
            price_from = b
            price_to = a

        if category != '0':
            result = " da nhan category " + \
                str(category) + " - " + \
                str(price_from) + " - " + str(price_to)
            if(x != 'no'):
                Drone_list = models.Drone.objects.filter(
                    name__contains=search_str, category=category).order_by("price")
            else:
                Drone_list = models.Drone.objects.filter(
                    category=category).order_by("price")

        if category == '0':
            result = " da nhan category = 0" + str(category)
            if(x != 'no'):
                drone_list = models.Drone.objects.filter(
                    name__contains=search_str).order_by("price")

        drone_list = [drone for drone in drone_list if drone.price >=
                        price_from and drone.price <= price_to]

        drone_items = len(drone_list)

        result = 'from ' + \
            '{:20,.0f}'.format(price_from) + ' $ đến ' + \
            '{:20,.0f}'.format(price_to) + ' $'

        page = request.GET.get('page', 1)
        paginator = Paginator(drone_list, 9) 

        try:
            drones = paginator.page(page)
        except PageNotAnInteger:
            drones = paginator.page(1)
        except EmptyPage:
            drones = paginator.page(paginator.num_pages)

        return render(request, "store/shop.html",
                      {'three_newest': three_newest,
                       'subcategories': category_list,
                       'drones': drones,
                       'pk': category,
                       'subcategories': category_list,
                       'drone_items': drone_items,
                       'category': category,
                       'search_str': search_str,
                       'result': result,
                       'username': username
                       })





def contact(request):
    username = request.session.get('username', 0)
    context = {
        'username' : username,
        'category' : category_list,
    }
    return render(request, 'store/contact.html',context)


def cart(request):
    return render(request, 'store/cart.html')


def register(request):
    registered = False
    if request.method == "POST":
        form_user = forms.UserForm(data=request.POST)
        form_por = forms.UserProfileInfoForm(data=request.POST)
        if (form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()
            registered = True

           
            email_address = form_user.cleaned_data['email']
            subject = 'your account has been registered'
            message = 'Enjoyyyyyy.<br/>appreciated.'
            recepient = str(email_address)

            html_content = '<h2 style="color:blue"><i>Welcome ' + form_user.cleaned_data['username']+',</i></h2>'\
                + '<p>Welcome to <strong>My drone</strong> website.</p>' \
                + '<h4 style="color:red">' + message + '</h4>'

            msg = EmailMultiAlternatives(
                subject, message, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        if form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
            form_user.add_error(
                'confirm', 'Password and confirm password are not the same!')
            print(form_user.errors, form_por.errors)
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()

    username = request.session.get('username', 0)
    return render(request, 'store/register.html',
                  {'categories': category_list,
                   'form_user': form_user,
                   'form_por': form_por,
                   'registered': registered,
                   'username': username}
                  )

    


def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = "Welcome " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return render(request, "store/login.html", {'login_result': result,
                                                        'username': username, 'categories': category_list,
                                                        })
        else:
            print("You can't login.")
            print("Username: {} and password: {}".format(username, password))
            login_result = "wrong password or username!"
            return render(request, "store/login.html", {'login_result': login_result, 'categories': category_list, })
    else:
        return render(request, 'store/login.html',{'categories': category_list})


def checkout(request):
    return render(request, 'store/checkout.html')


def forgetpass(request):
    return render(request, 'store/forget-password.html')








class DroneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed store (or edited)
    """
    queryset = models.Drone.objects.all().order_by('-public_day')
    serializer_class = DroneSerializer
    # Cấp quyền cho người dùng
    # permission_classes = [permissions.IsAdminUser] # đọc/ ghi
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # chỉ đọc


def read_drones(request):
    url = 'http://127.0.0.1:8000/api/drones/'

    urlResponse = urllib.request.urlopen(url)
    if hasattr(urlResponse.headers, 'get_content_charset'):
        encoding = urlResponse.headers.get_content_charset(DEFAULT_ENCODING)
    else:
        encoding = urlResponse.headers.getparam('charset') or DEFAULT_ENCODING

    drone_list = json.loads(urlResponse.read().decode(encoding))
    drone_list = sorted(
        drone_list, key=lambda x: x['viewed'], reverse=True)[:30]

    page = request.GET.get('page', 1)
    paginator = Paginator(drone_list, 9)  

    try:
        drones = paginator.page(page)
    except PageNotAnInteger:
        drones = paginator.page(1)
    except EmptyPage:
        drones = paginator.page(paginator.num_pages)


    username = request.session.get('username', 0)
    return render(request, "store/drones.html",
                  {'categories': category_list,
                   'username': username,
                   'drones': drones})




    


def drone_detail(request, pk):
    username = request.session.get('username', 0)
    drone_select = models.Drone.objects.get(pk=pk)
  
    models.Drone.objects.filter(
    pk=drone_select.pk).update(viewed=F('viewed') + 1)
    drone_select.refresh_from_db()
    cart_drone_form = CartAddDroneForm()
    return render(request, "store/drone.html",
                  {'drone': drone_select,
                   'categories': category_list,
                   'username': username,
                   'cart_drone_form': cart_drone_form,
                   })


def cart(request):
    username = request.session.get('username', 0)
    return render(request, 'store/cart.html',
                  {'categories': category_list,
                   'username': username
                   })


def checkout(request):
    username = request.session.get('username', 0)
    return render(request, 'store/checkout.html',
                  {'categories': category_list,
                   'username': username
                   })


@login_required
def log_out(request):
 
    logout(request)
    result = "Quý khách đã logout. Quý khách có thể login trở lại"
    return render(request, "store/login.html", {'logout_result': result, 'categories': category_list, })
