# Taskly

Django နဲ့ ရေးထားတဲ့ ကိုယ်ပိုင် အလုပ်စာရင်း mini project ဖြစ်ပါတယ်။ အကောင့်ခွဲပြီး ကိုယ့်အလုပ်ကိုပဲ မြင်ရပါတယ်။

## လုပ်ဆောင်ချက်

- အကောင့်ဖွင့်ခြင်း၊ ဝင်ခြင်း၊ ထွက်ခြင်း
- အလုပ် ထည့် / ပြင် / ဖျက် / ပြီးပြီဟု မှတ်ခြင်း
- အရေးကြီးမှု (နိမ့်၊ အလယ်၊ မြင့်) နဲ့ အခြေအနေ (လုပ်ရန်၊ လုပ်နေသည်၊ ပြီးပြီ)
- ရှာဖွေခြင်း၊ စစ်ထုတ်ခြင်း၊ စာမျက်နှာခွဲခြင်း
- ရက်လွန်အလုပ်ကို သီးသန့်ပြခြင်း
- Django admin

## မောင်းနည်း

```bash
cd "/Users/hermesmyanmar/Desktop/mini project"
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

Browser မှာ `http://127.0.0.1:8000/` ကို ဖွင့်ပါ။ ပထမဆုံး အကောင့်ဖွင့်ပြီး အလုပ်ထည့်ပါ။

Admin သုံးချင်ရင် —

```bash
python manage.py createsuperuser
```

ပြီးရင် `http://127.0.0.1:8000/admin/` ကို ဖွင့်ပါ။

Database က project ထဲက `db.sqlite3` (SQLite) ဖြစ်ပါတယ်။ ဒေသစံတော်ချိန်က `Asia/Yangon` ပါ။

## Live server

https://test.hermesmyanmar.com/
