from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages

# Create your views here.
def warm_up_data():
    if not Add_Train.objects.exists():
        trains_data = [
            {"name": "Rajdhani Express", "no": 12423, "from": "New Delhi", "to": "Guwahati", "dep": "16:10", "arr": "19:00", "travel": "26h 50m", "dist": 1900, "fare": 3500},
            {"name": "Shatabdi Express", "no": 12002, "from": "New Delhi", "to": "Bhopal", "dep": "06:00", "arr": "14:20", "travel": "8h 20m", "dist": 700, "fare": 1200},
            {"name": "Duronto Express", "no": 12260, "from": "Sealdah", "to": "New Delhi", "dep": "14:10", "arr": "10:35", "travel": "20h 25m", "dist": 1450, "fare": 2800},
            {"name": "Vande Bharat", "no": 22436, "from": "New Delhi", "to": "Varanasi", "dep": "06:00", "arr": "14:00", "travel": "8h", "dist": 750, "fare": 1800},
            {"name": "Gatimaan Express", "no": 12050, "from": "Hazrat Nizamuddin", "to": "Jhansi", "dep": "08:10", "arr": "12:35", "travel": "4h 25m", "dist": 400, "fare": 900},
            {"name": "Garib Rath", "no": 12909, "from": "Bandra Terminus", "to": "Hazrat Nizamuddin", "dep": "16:35", "arr": "09:40", "travel": "17h 05m", "dist": 1350, "fare": 1000},
            {"name": "Humsafar Express", "no": 12595, "from": "Gorakhpur", "to": "Anand Vihar", "dep": "20:00", "arr": "08:25", "travel": "12h 25m", "dist": 800, "fare": 1500},
            {"name": "Jan Shatabdi", "no": 12051, "from": "Mumbai", "to": "Madgaon", "dep": "05:10", "arr": "14:10", "travel": "9h", "dist": 600, "fare": 700},
            {"name": "Tejas Express", "no": 22672, "from": "Madurai", "to": "Chennai", "dep": "15:00", "arr": "21:15", "travel": "6h 15m", "dist": 500, "fare": 1300},
            {"name": "Grand Trunk Express", "no": 12616, "from": "New Delhi", "to": "Chennai", "dep": "18:40", "arr": "04:30", "travel": "33h 50m", "dist": 2200, "fare": 2200},
            {"name": "Karnavati Express", "no": 12934, "from": "Ahmedabad", "to": "Mumbai", "dep": "05:00", "arr": "12:35", "travel": "7h 35m", "dist": 500, "fare": 800},
            {"name": "Coromandel Express", "no": 12842, "from": "Chennai", "to": "Howrah", "dep": "08:45", "arr": "11:50", "travel": "27h 05m", "dist": 1650, "fare": 1900},
            {"name": "Punjab Mail", "no": 12138, "from": "Firozpur", "to": "Mumbai", "dep": "21:40", "arr": "07:45", "travel": "34h 05m", "dist": 1900, "fare": 2100},
            {"name": "Tamil Nadu Express", "no": 12622, "from": "New Delhi", "to": "Chennai", "dep": "21:05", "arr": "06:15", "travel": "33h 10m", "dist": 2200, "fare": 2300},
            {"name": "Deccan Queen", "no": 12124, "from": "Pune", "to": "Mumbai", "dep": "07:15", "arr": "10:25", "travel": "3h 10m", "dist": 200, "fare": 450},
        ]
        for t in trains_data:
            train = Add_Train.objects.create(
                trainname=t["name"],
                train_no=t["no"],
                from_city=t["from"],
                to_city=t["to"],
                departuretime=t["dep"],
                arrivaltime=t["arr"],
                trevaltime=t["travel"],
                distance=t["dist"]
            )
            # Add routes for search logic to work
            Add_route.objects.create(train=train, route=t["from"], distance=0, fare=0)
            Add_route.objects.create(train=train, route=t["to"], distance=t["dist"], fare=t["fare"])



def nav(request):
    return render(request,'carousel.html')


def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')


def Login_customer(request):
    error = False
    error2 = False
    error3 = False
    if request.method == "POST":
        n = request.POST['uname']
        p = request.POST['pwd']
        try:
            user = authenticate(username=n,password=p)
        except:
            error3 = True
        try:

            if user.is_staff:
                login(request,user)
                error2 = True
            elif user:
                login(request, user)
                error=True
        except:
            error3=True



    d = {'error':error,'error2':error2,'error3':error3}
    return render(request,'login_customer.html',d)

def Register_customer(request):
    error = False
    if request.method == "POST":
        n = request.POST['uname']
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        a = request.POST['add']
        m = request.POST['mobile']
        g = request.POST['male']
        d = request.POST['birth']
        p = request.POST['pwd']
        user = User.objects.create_user(first_name=f,last_name=l,username=n,password=p,email=e)
        Register.objects.create(user=user,add=a,mobile=m,gender=g,dob=d)
        error = True
    d = {'error':error}
    return render(request,'register_customer.html',d)

def Search_Train(request):
    warm_up_data()
    if not request.user.is_authenticated:
        return redirect('login_customer')
    data = Add_route.objects.values('route').distinct()
    coun = 0
    error = False
    fare3 = 0
    route1 = []
    route = ""
    
    if request.method == "POST":
        f = request.POST["fcity"]
        t = request.POST["tcity"]
        da = request.POST["date"]
        data1 = Add_route.objects.filter(route=f)
        data2 = Add_route.objects.filter(route=t)
        
        # Reset fare1 and fare2 to avoid UnboundLocalError
        fare1 = 0
        fare2 = 0
        
        for i in data1:
            for j in data2:
                if i.train.train_no == j.train.train_no:
                    route1.append(Add_Train.objects.filter(train_no=i.train.train_no))
                    fare1 = i.fare
                    fare2 = j.fare
        
        fare3 = fare2 - fare1
        if 0 < fare3 < 5:
            fare3 = 5
        elif fare3 < 0:
            fare3 = fare3 * (-1)
            
        route = f + " to " + t
        # Use the first train's name if available, otherwise default
        train_name = "Indian Rail"
        if route1:
            train_name = route1[0][0].trainname
            
        ase_obj = Asehi.objects.create(fare=fare3, train_name=train_name, date3=da)
        coun = ase_obj.id
        error = True

    d = {"data2": data, 'route1': route1, 'fare3': fare3, "error": error, 'coun': coun, 'route': route}
    return render(request, 'search_train.html', d)



def Dashboard(request):
    warm_up_data()
    if not request.user.is_authenticated:
        return redirect('login_customer')
    return render(request,'dashboard.html')

def Logout(request):
    logout(request)
    return redirect('nav')

def Book_detail(request,coun,pid,route1):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    error = False

    try:
        data = Asehi.objects.get(id=coun)
    except:
        data = None
    data2 = Add_Train.objects.get(id=pid)
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    pro = Passenger.objects.filter(user=user1)
    book = Book_ticket.objects.filter(user=user1)
    total = 0
    for i in pro:
        if i.status != "set":
            total = total + (i.fare or 0)
    passenger=0

    if request.method=="POST":
        f = request.POST["name"]
        t = request.POST["age"]
        da = request.POST["gender"]
        passenger = Passenger.objects.create(user=user1,train=data2,route=route1,name=f,gender=da,age=t,fare=data.fare,date1=data.date3)
        Book_ticket.objects.create(user=user1, route=route1, fare=total, passenger=passenger, date2=data.date3)

        if passenger:
            error = True
    d = {'data':data,'data2':data2,'pro':pro,'total':total,'book':book,'error':error,'route1':route1,'coun':coun,'pid':pid, 'departure': data2.departuretime, 'arrival': data2.arrivaltime}
    return render(request,'book_detail.html',d)

def Delete_passenger(request, pid, bid, coun, route1):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    try:
        data = Passenger.objects.get(id=pid)
        data.delete()
        messages.info(request, 'Passenger Deleted Successfully')
    except Passenger.DoesNotExist:
        messages.error(request, 'Passenger not found')
    
    return redirect('book_detail', coun, bid, route1)

def Card_Detail(request,total,coun,route1,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    error=False
    try:
        data = Asehi.objects.get(id=coun)
    except:
        data=None
    data2 = Add_Train.objects.get(id=pid)
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    pro = Passenger.objects.filter(user=user1)
    book = Book_ticket.objects.filter(user=user1)
    count=0
    pro1 = 0
    if request.method == "POST":
        error=True
        for i in pro:
            count = i.name
            if i.status != "set":
                i.status="set"
                i.save()
        return redirect('my_booking')

    total1=total
    d = {'user':user1,'data':data,'data2':data2,'pro':pro,'pro1':pro1,'total':total1,'book':book,'error':error,'route1':route1,'count':count}
    return render(request,'card_detail.html',d)


def my_booking(request):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    pro = Passenger.objects.filter(user=user1)
    book = Book_ticket.objects.filter(user=user1)
    d = {'user':user1,'pro':pro,'book':book}
    return render(request,'my_booking.html',d)


def view_ticket(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    book = Book_ticket.objects.get(id=pid)
    d = {'book':book, 'departure': book.passenger.train.departuretime, 'arrival': book.passenger.train.arrivaltime}
    return render(request,'view_ticket.html',d)


def viewbookings(request):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    book = Book_ticket.objects.all()
    d = {'book': book}
    return render(request, 'viewbookings.html', d)


def delte_my_booking(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    error=False
    pro = Passenger.objects.get(id=pid)
    pro.delete()
    error=True
    d = {'error':error}
    return render(request,'my_booking.html',d)

def deletebooking(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    error=False
    pro = Passenger.objects.get(id=pid)
    pro.delete()
    error=True
    d = {'error':error}
    return render(request,'viewbookings.html',d)



def Add_train(request):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    error=False
    if request.method == "POST":
        n = request.POST['busname']
        no = request.POST['bus_no']
        f = request.POST['fcity']
        to= request.POST['tcity']
        de= request.POST['dtime']
        a = request.POST['atime']
        t = request.POST['ttime']
        d = request.POST['dis']
        i = request.FILES['img']
        Add_Train.objects.create(trainname=n,train_no=no,from_city=f,to_city=to,departuretime=de,arrivaltime=a,trevaltime=t,distance=d,img=i)
        error=True
    d={"error":error}
    return render(request,'add_train.html',d)
def view_train(request):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    data=Add_Train.objects.all()
    d={"data":data}
    return render(request,"view_train.html",d)
def add_route(request):
    error=False
    data=Add_Train.objects.all()

    if request.method == "POST":
        b = request.POST['bus']
        r = request.POST['route']
        f= request.POST['fare']
        d = request.POST['dis']

        bus1 = Add_Train.objects.filter(id=b).get()
        Add_route.objects.create(train=bus1,route=r,distance=d,fare=f)
        error = True

    d={"data":data,"error":error}

    return render(request,'add_route.html',d)

def Edit_route(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    error=False
    data=Add_route.objects.get(id=pid)
    data2=Add_Train.objects.all()

    if request.method == "POST":
        b = request.POST['bus']
        r = request.POST['route']
        f= request.POST['fare']
        d = request.POST['dis']

        a = Add_Train.objects.filter(id=b).first()
        data.train = a
        data.route = r
        data.fare = f
        data.distance = d
        data.save()
        error=True

    d={"data":data,"data2":data2,"error":error}
    return render(request,'editroute.html',d)


def edit(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    error = False
    data1=Add_Train.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['busname']
        no = request.POST['bus_no']
        de= request.POST['dtime']
        a = request.POST['atime']
        t = request.POST['ttime']
        f = request.POST['fcity']
        to= request.POST['tcity']
        d = request.POST['dis']
        data1.trainname=n
        data1.train_no=no
        data1.from_city=f
        data1.to_city=to
        data1.departuretime=de
        data1.arrivaltime=a
        data1.trevaltime=t
        data1.distance=d
        data1.save()
        error = True
    d = {'data':data1,'error':error}
    return render(request,'edittrain.html',d)

def delete(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    error2=False
    data=Add_Train.objects.get(id=pid)
    data.delete()
    error2=True
    d = {'error2':error2}
    return render(request,"view_train.html",d)


def delete_route(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    error=False
    data=Add_route.objects.get(id=pid)
    data.delete()
    error = True
    d = {'error2':error}
    return render(request,"availableroute.html",d)

def displayroute(request):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    data = Add_route.objects.all()
    data2 = Add_Train.objects.all()
    d = {'data':data,'data2':data2}
    return render(request,"availableroute.html",d)

def admindashboard(request):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    return render(request,'admindashboard.html')

def change_image(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    train = Add_Train.objects.get(id=pid)
    error = ""
    if request.method=="POST":
        try:
            i = request.FILES['newpic']
            train.img = i
            train.save()
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'train':train}
    return render(request, 'change_image.html', d)



def view_regusers(request):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    data=Register.objects.filter(user__is_staff=False)
    d={"data":data}
    return render(request,"view_regusers.html",d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_customer')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_regusers')