from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, TemplateView

from customer.models import Orders
from owner.models import Books
from owner.forms import BookForm, OrderEditForm, LoginForm


class OwnerSignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'signin.html',{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                print("login success")
                login(request,user)
                return redirect('ownerhome')
            else:
                print("login failed")
            return render(request,'signin.html',{'form':form})

def ownersignout(request):
    logout(request)
    return redirect('ownersignin')

class OwnerIndexView(TemplateView):
    template_name = "ownerhome.html"



class AddBook(CreateView):
    model=Books
    form_class=BookForm
    template_name = "book_add.html"
    success_url = reverse_lazy("allbooks")

class BooklistView(ListView):
    model=Books
    template_name = "book_list.html"
    context_object_name = "books"

class BookDetailView(DetailView):
    model = Books
    template_name = "book_detail.html"
    context_object_name = "book"
    pk_url_kwarg = "id"

class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        qs=Books.objects.get(id=kwargs.get("id"))
        qs.delete()
        return redirect("allbooks")

class ChangeBook(UpdateView):
    model=Books
    template_name = 'book_change.html'
    form_class = BookForm
    success_url = reverse_lazy('allbooks')
    pk_url_kwarg = "id"

class DashBoardView(TemplateView):
    template_name = "dashboard.html"
    def get(self,request,*args,**kwargs):
        new_orders=Orders.objects.filter(status="order_placed")
        return render(request,self.template_name,{"new_orders":new_orders})




class OrderDetailView(DetailView):
    model=Orders
    template_name = "order_detail.html"
    context_object_name = "order"
    pk_url_kwarg = "id"

class OrderChangeView(UpdateView):
    model=Orders
    template_name = "order_change.html"
    form_class = OrderEditForm
    pk_url_kwarg = "id"
    def get(self,request,*args,**kwargs):
        order=Orders.objects.get(id=kwargs["id"])
        return render(request,self.template_name,{"order":order,"form":self.form_class})

    def post(self,request,*args,**kwargs):
        order=Orders.objects.get(id=kwargs["id"])
        form=OrderEditForm(request.POST,instance=order)
        if form.is_valid():
            delivery_date=str(form.cleaned_data.get("expected_delivery_date"))
            form.save()
            send_mail(
                'order notification',
                'your order will be delivered on .'+delivery_date,
                'preethipsaro@gmail.com',
                ['kvnithinkumar@gmail.com'],
                fail_silently=False,
            )
            return redirect("dashboard")
