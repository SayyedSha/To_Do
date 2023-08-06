from django.urls import path
from .views import *

urlpatterns = [
    
    path('reg',register),
    path('',auth),
    path('todo',todo_list),
    path('add_todo',add_todo_page),
    path('logout',Logout),
    path('update/<int:id>/',update),
    path('comp/<int:id>/',completed),
    path('del/<int:id>/',delete)
]