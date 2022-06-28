from django.urls import path
from owner import views

urlpatterns = [
path("",views.OwnerSignInView.as_view(),name="ownersignin"),
path("home",views.OwnerIndexView.as_view(),name="ownerhome"),
path("add", views.AddBook.as_view(), name="addbook"),
path('all', views.BooklistView.as_view(), name="allbooks"),
path('<int:id>', views.BookDetailView.as_view(), name="bookdetails"),
path('remove/<int:id>', views.BookDeleteView.as_view(), name="bookdelete"),
path('change/<int:id>', views.ChangeBook.as_view(), name="changebook"),
path('books/dashboard',views.DashBoardView.as_view(), name="dashboard"),
path('books/order/<int:id>',views.OrderDetailView.as_view(), name="orderdetail"),
path('order/change/<int:id>',views.OrderChangeView.as_view(), name="updateorder"),
path('signout',views.ownersignout,name="logout")

]
