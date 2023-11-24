from django.shortcuts import render, HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from esite_app.models import product,Cart,Order
from django.core.mail import send_mail
import random
import razorpay


# Create your views here.


#def data(request):
    #return render(request,'index.html')


def hello(request):
    context={}
    context['greet']="hello, i m learning DTL"
    context['x1']=50
    context['x2']=60
    context['l']=[10,20,30,45,52]
    context['products']=[

        {'id':1,'name':'vivo','cat':'mobile','price':15000},
        {'id':2,'name':'top','cat':'cloths','price':500},
        {'id':3,'name':'chair','cat':'furniture','price':3000},
        {'id':4,'name':'ring','cat':'gold','price':20000}

    ]
    context['sales']=[
        {'id':1,'name':'headphone','cat':'electronic','price':5000}
    ]
    return render(request,'hello.html',context)    




def data(request):
    #userid=request.user.id      # display the user logged in id 
    #print("id of loggedin user:",userid)

    context={}     #   display only acive product on vs command prompt using print(p)
    p=product.objects.filter(is_active=True)
    context['products']=p
    print(p)
    #print("Result:",request.user.is_authenticated)#display true command prompt if user logged in if user not loged in display false
    return render(request,'index.html',context)


def product_details(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'product_details.html',context)



def register(request):
    # data insert in table
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass==""  or ucpass=="":
            context['errmsg']="fields can not be empty"
            return render(request,'register.html',context)
        
        #   password and confirm password validation
        elif upass !=ucpass: #ana123 != ana
            context['errmsg']="password and confirmed password didn't match"
            return render(request,'register.html',context)
        else:
            try:

                    u=User.objects.create(password=upass,username=uname,email=uname)
                    u.set_password(upass)   # password not showing in model
                    u.save()
                    context['success']="user creted sucessfully,please login"
                    return render(request,'register.html',context)
                    #return HttpResponse("DATA INSERTED")
                    u.save()
            except Exception:
                        context['errmsg']="User with the same user name already exist"
                        return render(request,'register.html',context)
            #pass
    else:
          return render(request,'register.html')
    
def contact(request):
    return render(request,'con_tact.html')


def about(request):
    return render(request,'about.html')  


def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
             context['errmsg']="field can not be empty"
             return render(request,'login.html',context)
        else:
           u=authenticate(username=uname,password=upass)
          # print(u)     #object    first@gmail.com    on command rompt
           #print(u.username)      object.datamember
           #print(u.password)
           #print(u.is_superuser)


           if u is not None:
                login(request,u)
                return redirect('/data')
           else:
            
                context['errmsg']="field can not be empty"
                return render(request,'login.html',context)
                # print(uname,"--",upass)
                #return HttpResponse("data is fetched")
    else: 
        return render(request,'login.html') 

def user_logout(request):     # delete session using this cde 
     logout(request)
     return redirect('/data')

def catfilter(request,cv):
     q1=Q(is_active=True)
     q2=Q(cat=cv)
     p=product.objects.filter(q1 & q2)
     print(p)
     context={}
     context['products']=p 
     return render(request,'index.html',context)       



def sort(request,sv):
    if sv=='0':
        col='price'      #asc
    else:  
        col='-price'          #desc   
    #p=product.objects.order_by(col)
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)


def range(request):
     min=request.GET['min']
     max=request.GET['max'] 
     q1= Q(price__gte=min)
     q2= Q(price__lte=max)
     q3=Q(is_active=True)
     p=product.objects.filter(q1 & q2 & q3)
     context={}
     context['products']=p
     return render(request,'index.html',context)  
     #print(min) 
     #print(max)
     #return HttpResponse("value fetched")       
              



def addtocart(request,pid):
     if request.user.is_authenticated:
          userid=request.user.id   #4
          # print(userid)
          #print(pid)
         # return HttpResponse("data is fetched")
          u=User.objects.filter(id=userid) #queryset-- list
         # print(u)
        #  p=product.objects.filter(id=pid)
         # print(p)
          #c=Cart.objects.create(uid=u,pid=p)
         # c.save()
          #return HttpResponse("product added in he cart")
          print(u[0])
          p=product.objects.filter(id=pid)
          print(p[0])
          q1=Q(uid=u[0])
          q2=Q(pid=p[0])
          c=Cart.objects.filter(q1 & q2)   #1 quertse [1 object]
          context={} #not define in if condtion showing an error 
          context['products']=p
          n=len(c)

          if n == 1: 
               context['msg']="Product already exist in cart !!"
               return render(request,'product_details.html',context) 
          else:
               c=Cart.objects.create(uid=u[0],pid=p[0])
               c.save()
               context['success']="product Added Sucessfully to cart !!"
               return render(request,'product_details.html',context) 
         
     else:
          return redirect('/login')



def viewcart(request):
     c=Cart.objects.filter(uid=request.user.id)
     #print(c[0])
       # print(c[0].pid) pid (product) and uip(user)both object
       # print(c[0].uid)  show detils on command prompt
       #print(c[0].pid.name) print nameon command prompt  
       # print(c[0].pid.price)
      #print(c[0].uid.is_superuser)
     # print(c)
     np=len(c)
     #print(np)
     s=0
     for x in c:
          #print(x)
          #print(x.pid.price)
          s=s+ x.pid.price * x.qty       
          #print(s)
      
     context={}
     context['n']=np
     context['total']=s
     context['data']=c
     return render(request,'cart.html',context) 



         

def remove(request,cid):
     c=Cart.objects.filter(id=cid)
     c.delete()
     return redirect('/viewcart')  


def updateqty(request,qv,cid):
     c=Cart.objects.filter(id=cid)
     print(c)
     print(c[0])
     print(c[0].qty)
     if qv=='1':
          t=c[0].qty + 1
          c.update(qty=t)
     else:
          if c[0].qty > 1:
               t=c[0].qty - 1
               c.update(qty=t)
     return redirect("/viewcart")


def placeorder(request):
     userid=request.user.id
     c=Cart.objects.filter(uid=userid)
     oid=random.randrange(1000,9999)
     print("order id:",oid)
     for x in c:
          o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
          o.save()
          x.delete()
          orders=Order.objects.filter(uid=request.user.id)
          context={}
          context['data']=orders
          np=len(orders)
          s=0
          for x in orders:
               s=s+ x.pid.price * x.qty
               context['total']=s
               context['n']=np
          return render(request,'placeorder.html',context)




def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s= s + x.pid.price * x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_Me21FqLyHVLbxr", "9fUG044fVdEtNfmNcKCr5GY6"))

    data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    #print(payment)
    context={}
    context['data']=payment
    uemail=request.user.username
    print(uemail)
    context['uemail']=uemail
     
    #return HttpResponse("success")
    return render(request,'pay.html',context)


def sendusermail(request,uemail):
    #uemail=request.user.email   error 'AnonymousUser' object has no attribute 'email'
    #print(uemail)
    msg="order details are..."
    send_mail(
        "Ekart-order placed succesfully",
        msg,
        "manishathakur1396@gmail.com",
        [uemail],
        fail_silently=False,
    )
    return HttpResponse("mail send successfully")

