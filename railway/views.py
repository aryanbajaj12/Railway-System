from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from .models import *
from django.contrib import messages

# Create your views here.
def warm_up_data():
    if not Add_Train.objects.exists():
        # Data sourced from user-provided CSV — 28 real Indian trains
        trains_data = [
            {"name": "Rajdhani Express",            "no": 12423, "from": "New Delhi",          "to": "Guwahati",             "dep": "16:10", "arr": "19:00", "travel": "26h 50m", "dist": 1890, "fare": 3500},
            {"name": "Shatabdi Express",             "no": 12002, "from": "New Delhi",          "to": "Bhopal",               "dep": "06:00", "arr": "14:10", "travel": "8h 10m",  "dist": 704,  "fare": 1200},
            {"name": "Kalka Shatabdi",               "no": 12005, "from": "New Delhi",          "to": "Kalka",                "dep": "17:15", "arr": "21:15", "travel": "4h 00m",  "dist": 269,  "fare": 650},
            {"name": "Himalayan Queen",              "no": 14095, "from": "Delhi Sarai Rohilla", "to": "Kalka",                "dep": "05:35", "arr": "11:20", "travel": "5h 45m",  "dist": 260,  "fare": 150},
            {"name": "Gorakhdham Express",           "no": 12556, "from": "Hisar",              "to": "Gorakhpur",            "dep": "17:00", "arr": "09:45", "travel": "16h 45m", "dist": 875,  "fare": 450},
            {"name": "Kisan Express",                "no": 14731, "from": "Old Delhi",          "to": "Bathinda",             "dep": "14:00", "arr": "21:30", "travel": "7h 30m",  "dist": 352,  "fare": 140},
            {"name": "Haryana Express",              "no": 14088, "from": "Tilak Bridge",       "to": "Sirsa",                "dep": "18:35", "arr": "02:40", "travel": "8h 05m",  "dist": 285,  "fare": 130},
            {"name": "Netaji Express",               "no": 12311, "from": "Howrah",             "to": "Kalka",                "dep": "21:55", "arr": "03:00", "travel": "29h 05m", "dist": 1713, "fare": 670},
            {"name": "Hisar Coimbatore AC SF",       "no": 22475, "from": "Hisar",              "to": "Coimbatore",           "dep": "13:50", "arr": "14:30", "travel": "48h 40m", "dist": 2814, "fare": 2950},
            {"name": "Bhiwani Kanpur Express",       "no": 14154, "from": "Bhiwani",            "to": "Kanpur Central",       "dep": "20:45", "arr": "08:35", "travel": "11h 50m", "dist": 487,  "fare": 280},
            {"name": "Rohtak Intercity",             "no": 14323, "from": "New Delhi",          "to": "Rohtak",               "dep": "10:45", "arr": "12:20", "travel": "1h 35m",  "dist": 71,   "fare": 60},
            {"name": "Kurukshetra Delhi MEMU",       "no": 64462, "from": "Kurukshetra",        "to": "New Delhi",            "dep": "05:35", "arr": "09:00", "travel": "3h 25m",  "dist": 157,  "fare": 40},
            {"name": "Panipat New Delhi MEMU",       "no": 64470, "from": "Panipat",            "to": "New Delhi",            "dep": "06:00", "arr": "08:25", "travel": "2h 25m",  "dist": 90,   "fare": 30},
            {"name": "Rewari Delhi DEMU",            "no": 74002, "from": "Rewari",             "to": "Old Delhi",            "dep": "17:00", "arr": "19:15", "travel": "2h 15m",  "dist": 82,   "fare": 30},
            {"name": "Faridabad Nizamuddin EMU",     "no": 64073, "from": "Faridabad",          "to": "Hazrat Nizamuddin",    "dep": "08:30", "arr": "09:10", "travel": "0h 40m",  "dist": 21,   "fare": 15},
            {"name": "Ambala Nanded SF Express",     "no": 22710, "from": "Ambala Cantt",       "to": "Hazur Sahib Nanded",   "dep": "06:15", "arr": "12:30", "travel": "30h 15m", "dist": 1740, "fare": 680},
            {"name": "Sirsa Express",                "no": 14085, "from": "Tilak Bridge",       "to": "Sirsa",                "dep": "17:35", "arr": "02:00", "travel": "8h 25m",  "dist": 285,  "fare": 135},
            {"name": "Chandigarh Shatabdi",          "no": 12045, "from": "New Delhi",          "to": "Chandigarh",           "dep": "19:15", "arr": "22:35", "travel": "3h 20m",  "dist": 244,  "fare": 595},
            {"name": "Jaipur Chandigarh Express",    "no": 19717, "from": "Jaipur",             "to": "Chandigarh",           "dep": "20:10", "arr": "07:35", "travel": "11h 25m", "dist": 594,  "fare": 320},
            {"name": "Ajmer Chandigarh Garib Rath",  "no": 12983, "from": "Ajmer",              "to": "Chandigarh",           "dep": "18:00", "arr": "06:40", "travel": "12h 40m", "dist": 683,  "fare": 750},
            {"name": "Vande Bharat Express",         "no": 22436, "from": "New Delhi",          "to": "Varanasi",             "dep": "06:00", "arr": "14:00", "travel": "8h 00m",  "dist": 759,  "fare": 1750},
            {"name": "Mumbai Rajdhani",              "no": 12952, "from": "New Delhi",          "to": "Mumbai Central",       "dep": "16:55", "arr": "08:35", "travel": "15h 40m", "dist": 1386, "fare": 2850},
            {"name": "Kerala Express",               "no": 12626, "from": "New Delhi",          "to": "Trivandrum",           "dep": "20:10", "arr": "22:15", "travel": "50h 05m", "dist": 3035, "fare": 950},
            {"name": "Coromandel Express",           "no": 12841, "from": "Howrah",             "to": "Chennai Central",      "dep": "15:20", "arr": "16:50", "travel": "25h 30m", "dist": 1661, "fare": 680},
            {"name": "Paschim Express",              "no": 12925, "from": "Bandra Terminus",    "to": "Amritsar",             "dep": "11:25", "arr": "19:20", "travel": "31h 55m", "dist": 1882, "fare": 730},
            {"name": "Gitanjali Express",            "no": 12859, "from": "Mumbai CSMT",        "to": "Howrah",               "dep": "06:00", "arr": "12:30", "travel": "30h 30m", "dist": 1968, "fare": 750},
            {"name": "Navjeevan Express",            "no": 12655, "from": "Ahmedabad",          "to": "Chennai Central",      "dep": "21:35", "arr": "16:05", "travel": "42h 30m", "dist": 1891, "fare": 715},
            {"name": "Darjeeling Mail",              "no": 12343, "from": "Sealdah",            "to": "New Jalpaiguri",       "dep": "22:05", "arr": "08:15", "travel": "10h 10m", "dist": 573,  "fare": 355},
            # --- Batch 2: Sirsa region trains ---
            {"name": "Haryana Express",              "no": 14086, "from": "Sirsa",              "to": "New Delhi",            "dep": "02:50", "arr": "10:25", "travel": "7h 35m",  "dist": 311,  "fare": 150},
            {"name": "Kisan Express Return",         "no": 14732, "from": "Sirsa",              "to": "Old Delhi",            "dep": "06:15", "arr": "12:25", "travel": "6h 10m",  "dist": 261,  "fare": 140},
            {"name": "Gorakhdham Express Return",    "no": 12556, "from": "Sirsa",              "to": "Gorakhpur",            "dep": "15:25", "arr": "10:00", "travel": "18h 35m", "dist": 910,  "fare": 470},
            {"name": "SGNR Delhi Express",           "no": 14029, "from": "Sirsa",              "to": "Old Delhi",            "dep": "06:35", "arr": "15:40", "travel": "9h 05m",  "dist": 261,  "fare": 140},
            {"name": "Ajmer Amritsar Express",       "no": 19611, "from": "Sirsa",              "to": "Amritsar",             "dep": "03:45", "arr": "14:40", "travel": "10h 55m", "dist": 423,  "fare": 260},
            {"name": "Sirsa Kota Express",           "no": 19814, "from": "Sirsa",              "to": "Kota",                 "dep": "16:10", "arr": "05:15", "travel": "13h 05m", "dist": 550,  "fare": 320},
            {"name": "Tripura Sundari Express",      "no": 14620, "from": "Sirsa",              "to": "New Delhi",            "dep": "16:45", "arr": "23:30", "travel": "6h 45m",  "dist": 261,  "fare": 145},
            {"name": "SVDK Sabarmati Express",       "no": 19416, "from": "Sirsa",              "to": "Sabarmati",            "dep": "02:15", "arr": "21:20", "travel": "19h 05m", "dist": 950,  "fare": 480},
            {"name": "Bhatinda Jaipur Express",      "no": 14733, "from": "Sirsa",              "to": "Jaipur",               "dep": "23:00", "arr": "09:15", "travel": "10h 15m", "dist": 420,  "fare": 240},
            {"name": "Rewari Bathinda Passenger",    "no": 54782, "from": "Sirsa",              "to": "Bathinda",             "dep": "14:25", "arr": "16:45", "travel": "2h 20m",  "dist": 76,   "fare": 40},
            {"name": "Fazilka Rewari Express",       "no": 14730, "from": "Sirsa",              "to": "Rewari",               "dep": "14:25", "arr": "20:50", "travel": "6h 25m",  "dist": 276,  "fare": 140},
            {"name": "Mut Sgnr Express",             "no": 14030, "from": "Sirsa",              "to": "Shri Ganganagar",      "dep": "18:10", "arr": "23:35", "travel": "5h 25m",  "dist": 152,  "fare": 95},
            {"name": "Sirsa Bathinda Passenger",     "no": 4784,  "from": "Sirsa",              "to": "Bathinda",             "dep": "07:50", "arr": "10:00", "travel": "2h 10m",  "dist": 76,   "fare": 30},
            {"name": "Rewari Fazilka Express",       "no": 14729, "from": "Sirsa",              "to": "Fazilka",              "dep": "09:50", "arr": "15:45", "travel": "5h 55m",  "dist": 225,  "fare": 120},
            # --- Batch 3: Mixed routes ---
            {"name": "Ajmer Shatabdi",               "no": 12015, "from": "New Delhi",          "to": "Ajmer",                "dep": "06:10", "arr": "12:40", "travel": "6h 30m",  "dist": 443,  "fare": 800},
            {"name": "Ala Hazrat Express",            "no": 14321, "from": "Bareilly",           "to": "Bhuj",                 "dep": "06:35", "arr": "08:50", "travel": "26h 15m", "dist": 1110, "fare": 520},
            {"name": "Garib Rath Express",            "no": 12216, "from": "Bandra Terminus",    "to": "Delhi Sarai Rohilla",  "dep": "12:00", "arr": "11:00", "travel": "23h 00m", "dist": 1431, "fare": 1050},
            {"name": "Ashram Express",                "no": 12916, "from": "New Delhi",          "to": "Ahmedabad",            "dep": "15:20", "arr": "03:15", "travel": "11h 55m", "dist": 934,  "fare": 480},
            {"name": "Chetak Express",                "no": 20473, "from": "Delhi Sarai Rohilla", "to": "Udaipur",              "dep": "19:35", "arr": "07:50", "travel": "12h 15m", "dist": 673,  "fare": 380},
            {"name": "August Kranti Rajdhani",        "no": 12954, "from": "Hazrat Nizamuddin",  "to": "Mumbai Central",       "dep": "17:15", "arr": "10:05", "travel": "16h 50m", "dist": 1377, "fare": 2700},
            {"name": "Golden Temple Mail",            "no": 12904, "from": "Amritsar",           "to": "Mumbai Central",       "dep": "18:55", "arr": "23:45", "travel": "28h 50m", "dist": 1893, "fare": 730},
            {"name": "Punjab Mail",                   "no": 12138, "from": "Firozpur Cantt",     "to": "Mumbai CSMT",          "dep": "21:45", "arr": "07:35", "travel": "33h 50m", "dist": 1930, "fare": 740},
            {"name": "Kanpur Shatabdi",               "no": 12034, "from": "New Delhi",          "to": "Kanpur Central",       "dep": "15:50", "arr": "20:50", "travel": "5h 00m",  "dist": 440,  "fare": 950},
            {"name": "Lucknow Swran Shatabdi",        "no": 12004, "from": "New Delhi",          "to": "Lucknow",              "dep": "06:10", "arr": "12:40", "travel": "6h 30m",  "dist": 512,  "fare": 1100},
            {"name": "Gomti Express",                 "no": 12420, "from": "New Delhi",          "to": "Lucknow",              "dep": "12:20", "arr": "21:30", "travel": "9h 10m",  "dist": 512,  "fare": 195},
            {"name": "Shram Shakti Express",          "no": 12452, "from": "New Delhi",          "to": "Kanpur Central",       "dep": "23:55", "arr": "06:00", "travel": "6h 05m",  "dist": 440,  "fare": 270},
            {"name": "Tejas Express",                 "no": 82502, "from": "New Delhi",          "to": "Lucknow",              "dep": "15:40", "arr": "22:05", "travel": "6h 25m",  "dist": 512,  "fare": 1500},
            {"name": "Lucknow Mail",                  "no": 12230, "from": "New Delhi",          "to": "Lucknow",              "dep": "22:00", "arr": "06:45", "travel": "8h 45m",  "dist": 493,  "fare": 320},
            {"name": "Howrah Rajdhani",               "no": 12302, "from": "New Delhi",          "to": "Howrah",               "dep": "16:50", "arr": "09:55", "travel": "17h 05m", "dist": 1451, "fare": 3100},
            {"name": "Poorva Express",                "no": 12304, "from": "New Delhi",          "to": "Howrah",               "dep": "17:40", "arr": "17:00", "travel": "23h 20m", "dist": 1441, "fare": 630},
            {"name": "SBC Rajdhani",                  "no": 22692, "from": "Hazrat Nizamuddin",  "to": "KSR Bengaluru",        "dep": "19:50", "arr": "05:20", "travel": "33h 30m", "dist": 2365, "fare": 3900},
            {"name": "Grand Trunk Express",           "no": 12616, "from": "New Delhi",          "to": "Chennai Central",      "dep": "16:10", "arr": "04:30", "travel": "36h 20m", "dist": 2181, "fare": 800},
            {"name": "Tamil Nadu Express",            "no": 12622, "from": "New Delhi",          "to": "Chennai Central",      "dep": "21:05", "arr": "06:15", "travel": "33h 10m", "dist": 2181, "fare": 810},
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
    today = date.today().isoformat()  # e.g. '2026-06-18'
    coun = 0
    error = False
    error_date = False  # True when user picks a past date
    fare3 = 0
    route1 = []
    route = ""

    if request.method == "POST":
        f = request.POST["fcity"]
        t = request.POST["tcity"]
        da = request.POST["date"]

        # --- Date validation: reject past dates ---
        from datetime import datetime
        try:
            selected_date = datetime.strptime(da, "%Y-%m-%d").date()
        except ValueError:
            selected_date = date.today()

        if selected_date < date.today():
            error_date = True
        else:
            data1 = Add_route.objects.filter(route=f)
            data2 = Add_route.objects.filter(route=t)
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
            train_name = "Indian Rail"
            if route1:
                train_name = route1[0][0].trainname

            ase_obj = Asehi.objects.create(fare=fare3, train_name=train_name, date3=da)
            coun = ase_obj.id
            error = True

    d = {"data2": data, 'route1': route1, 'fare3': fare3, "error": error,
         'error_date': error_date, 'coun': coun, 'route': route, 'today': today}
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