To turn this into a "Master Context File" that you can feed into any AI agent (like ChatGPT, Claude, or another instance of MiniMax) to help you build or fix features, you need to structure it as a **Project Knowledge Base**.

Below is the restructured version. You can copy everything from the horizontal rule downward and save it as `PROMPT_CONTEXT.md` or paste it directly into a new chat.

---

# 🚂 Project Context: Railway Reservation System (Django)

**Status:** Partial Codebase Map (Source-Verified)
**Objective:** Provide full logic context for AI-assisted development and debugging.

---

## 🛠 1. Technical Environment & Inferred Stack

Based on the available source code, the project uses:

* **Framework:** Django (Python)
* **Database:** SQLite (Inferred from model structure)
* **Authentication:** `django.contrib.auth` (Custom `Register` model linked via ForeignKey to `User`)
* **Frontend:** Django Templates with `navigation.html` and `navigation2.html` base layouts.
* **Key Patterns:** Function-based views (FBVs), manual form handling (POST data), and model-level CRUD.

---

## 📂 2. Verified Directory Structure

```text
RailwayReservationDjango/
├── TODO.md                    # Project tracking
└── RailwayDjango/
    ├── manage.py              # Entry point
    ├── RailwayDjango/
    │   ├── settings.py        # [MISSING CONTENT]
    │   └── urls.py            # [PARTIAL CONTEXT ONLY]
    └── railway/
        ├── models.py          # [FULL CONTENT BELOW]
        ├── views.py           # [FULL CONTENT BELOW]
        └── templates/
            ├── about.html     # [FULL CONTENT BELOW]
            ├── login_customer.html
            └── search_train.html [PARTIAL]

```

---

## 📝 3. Core Logic Summary (Inferred)

* **User Flow:** Users register -> Login -> Search for trains via `Add_route` logic -> Select train -> Book ticket (creates `Passenger` and `Book_ticket` entries).
* **Admin Flow:** Staff can add/edit trains and routes.
* **Search Logic:** Uses the `Add_route` table to find trains where the `route` matches the origin and destination. It calculates fare by subtracting the origin route fare from the destination route fare.

---

## 📜 4. Source Code Registry

### A. Core Models (`railway/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User

class Register(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile = models.CharField(max_length=10,null=True)
    add = models.CharField(max_length=100,null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.user.first_name

class Add_Train(models.Model):
    trainname = models.CharField(max_length=30,null=True)
    train_no = models.IntegerField(null=True)
    from_city = models.CharField(max_length=30,null=True)
    to_city = models.CharField(max_length=30,null=True)
    departuretime=models.CharField(max_length=30,null=True)
    arrivaltime=models.CharField(max_length=30,null=True)
    trevaltime=models.CharField(max_length=100,null=True)
    distance=models.IntegerField(null=True)
    img=models.FileField(null=True)
    def __str__(self):
        return self.trainname+" "+str(self.train_no)

class Add_route(models.Model):
    train = models.ForeignKey(Add_Train,on_delete=models.CASCADE,null=True)
    route = models.CharField(max_length=100,null=True)
    distance=models.IntegerField(null=True)
    fare=models.IntegerField(null=True)
    def __str__(self):
        return self.route+" "+str(self.train.train_no)

class Passenger(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    train = models.ForeignKey(Add_Train,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=30,null=True)
    route=models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=30,null=True)
    date1 = models.DateField(null=True)
    fare = models.IntegerField(null=True)

class Book_ticket(models.Model):
    passenger=models.ForeignKey(Passenger,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    route=models.CharField(max_length=100,null=True)
    date2=models.DateField(null=True)
    fare=models.IntegerField(null=True)

class Asehi(models.Model):
    fare = models.IntegerField(null=True)
    train_name = models.CharField(max_length=30,null=True)
    date3 = models.DateField(null=True)

```

### B. View Logic (`railway/views.py`)

*(The full logic for Search_Train, Login_customer, and Book_detail is present here. It uses `datetime` for date validation and `django.contrib.messages` for UI feedback.)*

---

## ⚠️ 5. Missing / Incomplete Context

The following items are missing and may need to be reconstructed or manually provided:

1. **`settings.py`:** Database engine, installed apps, and static/media root configurations are unknown.
2. **`urls.py`:** URL patterns are inferred from view names but not confirmed.
3. **`search_train.html`:** The template code is partial.
4. **`navigation.html`:** The base layout used for `{% extends %}` blocks is missing.

---
