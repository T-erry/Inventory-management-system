from django import forms 
from .models import Inventory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create the form class.
class AddInventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']


class UpdateInventoryForm(forms.ModelForm):
    
    class Meta:
        model = Inventory
        fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="A valid email address, please.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)  # Call the parent class's save method
        user.email = self.cleaned_data['email']  # Assign the email from form data
        if commit:
            user.save()  # Save to the database
        return user   

