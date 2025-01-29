from django.shortcuts import get_object_or_404, render, redirect
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm, UpdateInventoryForm, UserRegistrationForm, SetPasswordForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django_pandas.io import read_frame
import plotly
from plotly.utils import PlotlyJSONEncoder
import plotly.express as px
import json

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
    
    return redirect('/inventory')


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
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'inventory_system/password_reset_confirm.html', {'form': form})


@login_required
def inventory_list(request):
    if request.user.is_superuser:
        inventories = Inventory.objects.all()
    else:
        inventories = Inventory.objects.filter(user=request.user)
    context ={
        "title" : "Inventory list",
        "inventories": inventories

    }
    return render(request, "inventory/inventory_list.html", context=context)




@login_required
def per_product_view(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    if request.user.is_superuser or inventory.user == request.user:  # Allow admins or the owner to view
        context = {
            'inventory': inventory,
        }

        return render(request, "inventory/per_product.html", context=context)
    else:
        messages.error(request, "You do not have permission to view this inventory.")
        return redirect("/inventory/")

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
            #Associate the inventory with the logged-in user
            new_inventory.user = request.user
            new_inventory.save()
            messages.success(request, "Successfully Added Inventory" )
            return redirect("/inventory/")
    else:
        # Create an empty form for GET requests
        add_form = AddInventoryForm()


    return render(request, "inventory/add_inventory.html", {"form": add_form})

@login_required
def delete_inventory(request, id):
    if request.user.is_superuser or inventory.user == request.user:  # Allow admins or the owner to delete
        inventory.delete()
        messages.success(request, "Inventory Deleted")
    else:
        messages.error(request, "You do not have permission to delete this inventory.")

    return redirect("/inventory")

@login_required
def update_inventory(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    if not (request.user.is_superuser or inventory.user == request.user):  # Restrict access
        messages.error(request, "You do not have permission to update this inventory.")
        return redirect("/inventory")

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

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("inventory_system/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        Password reset sent
                    
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('/inventory/')
        
        
    form = PasswordResetForm()

    return render(request, "inventory_system/password_reset.html", {"form": form})


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and log in now.")
                return redirect('/login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'inventory_system/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, try again')
    return redirect("/login")

@login_required
def dashboard(request):
    if request.user.is_superuser:
    # Fetch all inventory records from the database
        inventories = Inventory.objects.all()
    else:
        inventories = Inventory.objects.filter(user=request.user)  # Users can only see their own inventories
    # Convert the QuerySet/data to a Pandas DataFrame
    df = read_frame(inventories)

    # Group data by 'last_sale_date' and sum up the sales
    sales_graph = df.groupby(by="last_sale_date", as_index=False, sort=False)['sales'].sum()
    # Create a Plotly line chart
    sales_graph = px.line(sales_graph, x="last_sale_date", y="sales", title="Sales Trend")
    # Convert the Plotly figure to JSON for rendering in the template
    sales_graph = json.dumps(sales_graph, cls=PlotlyJSONEncoder)

    best_performing_product_df = df.groupby(by="name").sum().sort_values(by="quantity_sold")
    best_performing_product = px.bar(best_performing_product_df,
                                     x=best_performing_product_df.index,
                                     y=best_performing_product_df.quantity_sold,
                                     title="Best Performing Product")

    best_performing_product = json.dumps(best_performing_product, cls=PlotlyJSONEncoder)


    most_product_in_stock_df = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    most_product_in_stock = px.pie(most_product_in_stock_df, 
                                   names = most_product_in_stock_df.index,
                                   values= most_product_in_stock_df.quantity_in_stock,  
                                   title = "Most Product In stock"
                                       )
    most_product_in_stock = json.dumps(most_product_in_stock, cls=PlotlyJSONEncoder)

    # Pass the graphs to the template
    context = {
        "sales_graph": sales_graph,
        "best_performing_product": best_performing_product,
        "most_product_in_stock" : most_product_in_stock
    }

    return render(request, "inventory/dashboard.html", context=context)