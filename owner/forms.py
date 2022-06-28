from django import forms

from customer.models import Orders
from owner.models import Books

class BookForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"
        widgets={
            "book_name":forms.TextInput(attrs={"class":"form-control"}),
            "author":forms.TextInput(attrs={"class":"form-control"}),
            "amount":forms.NumberInput(attrs={"class":"form-control"}),
            "copies":forms.NumberInput(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"})
             }


class OrderEditForm(forms.ModelForm):
    options = (
        ("order_placed", "order_placed"),
        ("dispatched", "dispatched"),
        ("in_transit", "in_transit"),
        ("delivered", "delivered"),
    )
    status=forms.ChoiceField(choices=options,widget=forms.Select(attrs={"class":"form-select"})
        )

    class Meta:
        model=Orders
        fields=[
            "expected_delivery_date","status"
        ]
        widgets={
            "expected_delivery_date":forms.DateInput(attrs={"class":"form-control","type":"date"}),
            "status":forms.Select(attrs={"class":"form-select"})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned_data=super().clean()
        newpassword=cleaned_data.get('newpassword')
        confirmpassword=cleaned_data.get("confirmpassword")
        if newpassword != confirmpassword:
            msg="password mismatch"
            self.add_error("newpassword",msg)