from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View,CreateView,ListView,DetailView

from customer.decorators import signin_required
from customer.forms import UserRegistrationForm, LoginForm, OrderForm, ReviewForm
from customer.models import Carts, Orders, Reviews
from owner.models import Books

@method_decorator(signin_required,name="dispatch")
class CustomerIndex(ListView):
    model=Books
    template_name = "custhome.html"
    context_object_name = "books"


class SignUpView(CreateView):
    model=User
    form_class = UserRegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("signin")

class SignInView(View):
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
                return redirect('custhome')
            else:
                print("login failed")
            return render(request,'signin.html',{'form':form})
@signin_required
def signout(request):
    logout(request)
    return redirect('signin')

@method_decorator(signin_required,name="dispatch")
class PasswordResetview(View):
    def get(self,request,*args):
        form=PasswordResetForm()
        return render(request,'password_reset.html',{"form":form})
    def post(self,request):
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get('oldpassword')
            newpassword=form.cleaned_data.get('newpassword')
            user=authenticate(request,username=request.user,password=oldpassword)
            if user:
                user.set_password(newpassword)
                user.save()
                return redirect('custhome')
            else:
                return render(request, 'password_reset.html', {"form": form})
        else:
            return render(request, 'password_reset.html', {"form": form})

@signin_required
def add_to_cart(request,*args,**kwargs):
    book=Books.objects.get(id=kwargs["id"])
    user=request.user
    cart=Carts(product=book,user=user)
    cart.save()
    messages.success(request,"item has been added to cart")
    return redirect("custhome")


@method_decorator(signin_required,name="dispatch")
class ViewMyCart(ListView):
    model = Carts
    template_name = "mycart.html"
    context_object_name = "carts"
    def get(self,request,*args,**kwargs):
        carts=Carts.objects.filter(user=self.request.user).exclude(status="cancelled").order_by("-date")
        total=Carts.objects.filter(user=request.user).exclude(status="cancelled").aggregate(Sum("product__amount"))
        gtotal = total.get("product__amount__sum")
        context={"carts":carts,"total":gtotal}
        return render(request,"mycart.html",context)

def remove_from_cart(request,*args,**kwargs):
    cart=Carts.objects.get(id=kwargs["id"])
    cart.status="cancelled"
    cart.save()
    messages.error(request,"your item has been removed from cart")
    return redirect("custhome")


class OrderCreateView(CreateView):
    form_class = OrderForm
    template_name="order_create.html"
    model=Orders
    def post(self,request,*args,**kwargs):
        cart_id=kwargs.get("c_id")
        product_id=kwargs.get("p_id")
        form=OrderForm(request.POST)
        if form.is_valid():
            order=form.save(commit=False)
            product=Books.objects.get(id=product_id)
            user=request.user
            order.product=product
            order.user=request.user
            order.save()
            cart=Carts.objects.get(id=cart_id)
            cart.status="orderplaced"
            cart.save()
            messages.success(request,"your order has been placed")
        return redirect("custhome")

class OrdersListView(ListView):
    model=Orders
    template_name = "order_list.html"
    context_object_name = "orders"
    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user).order_by("-date")

class CreateReview(CreateView):
    model=Reviews
    form_class = ReviewForm
    template_name = "post_review.html"
    def post(self,request,*args,**kwargs):
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.posted_by=self.request.user
            product=Books.objects.get(id=kwargs["id"])
            review.product=product
            review.save()
            messages.success(request,"your review has been posted")
            return redirect("custhome")
        else:
            return render(request,self.template_name,{"form":form})

class ProductDetailView(DetailView):
    model=Books
    template_name = "detail_view.html"
    context_object_name ="book"
    pk_url_kwarg = "id"