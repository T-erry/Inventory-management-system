from django.shortcuts import get_object_or_404, render, redirect
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm, UpdateInventoryForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from .tokens import account_activation_token







# Create your views here.
# @user_not_authenticated

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')   
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('/inventory/')


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('inventory_system/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            #user needs to have an activated email address
            user.is_active= False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/inventory/')  # Redirect to inventory page
        else:
            # Log the form errors
            for error in list(form.errors.values()):
                print(error)
    else:
        form = UserRegistrationForm()

    context ={
            "form":form
        }


    return render(request, "inventory_system/sign_up.html", context)



@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    context ={
        "title" : "Inventory list",
        "inventories": inventories

    }
    return render(request, "inventory/inventory_list.html", context=context)


@login_required
def per_product_view(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    context = {
        'inventory': inventory,
    }

    return render(request, "inventory/per_product.html", context=context)


@login_required
def add_inventory(request):
    if request.method == "POST":
        # Populate the form with POST data
        add_form = AddInventoryForm(data=request.POST)  
        # Check if all fields are valid
        if add_form.is_valid():
            # Create an unsaved instance
            new_inventory = add_form.save(commit=False)
            # Calculate the total sales
            new_inventory.sales = float(add_form.cleaned_data['cost_per_item']) * float(add_form.cleaned_data['quantity_sold'])
            new_inventory.save()
            messages.success(request, "Successfully Added Inventory" )
            return redirect("/inventory/")
    else:
        # Create an empty form for GET requests
        add_form = AddInventoryForm()


    return render(request, "inventory/add_inventory.html", {"form": add_form})

@login_required
def delete_inventory(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    inventory.delete()
    messages.error(request, "Inventory Deleted")
    return redirect("/inventory/")

@login_required
def update_inventory(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    
    if request.method == 'POST':
        update_form = UpdateInventoryForm(data=request.POST)
        if update_form.is_valid():
            inventory.name = update_form.cleaned_data['name']
            inventory.cost_per_item = update_form.cleaned_data['cost_per_item']
            inventory.quantity_in_stock = update_form.cleaned_data['quantity_in_stock']
            inventory.quantity_sold = update_form.cleaned_data['quantity_sold']
            inventory.sales = float(update_form.cleaned_data['cost_per_item']) * float(update_form.cleaned_data['quantity_sold'])
            inventory.save()
            messages.success(request, "Inventory Updated")
            return redirect(f"/inventory/per_product/{id}")
    else:
         # Initialize form with inventory data for GET request
        update_form = UpdateInventoryForm(instance=inventory) 

    context = {"form": update_form}
    return render(request, "inventory/update_inventory.html", context=context)

