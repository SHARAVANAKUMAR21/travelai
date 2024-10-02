from pyexpat import model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Ensure correct import



from django.shortcuts import render
# Import forms
from .forms import ProductForm, UserProfileForm, CustomUserCreationForm, SupplierForm

from .forms import PasswordChangeForm



# Import models
from .models import (
    Category,
    ChatHistory, 
    Product, 
    UserProfile, 
    Supplier, 
    SupplierOrder,  # Keep this only once
    Order, 
    OrderItem
)

# Import Django ORM functions
from django.db.models import F
from django.conf import settings


from django.core.mail import send_mail


def send_mail_from_website(subject,message,email):
    subject = subject
    message = message
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    print(from_email,'to',to_email)


    send_mail(subject, message, from_email, to_email)
    
    
from django.shortcuts import render
from django.db.models import F
from .models import Product

def adminpage(request):
    # Products that are at reorder level or lower
    products_at_reorder_level = Product.objects.filter(quantity__lte=F('reorderlevel'))
    
    # Fetch all products
    products = Product.objects.all()
    
    context = {
        'products_at_reorder_level': products_at_reorder_level,
        'productdata': products  # Send the products data to the template
    }

    return render(request, 'user.html', context)




def reoder(request):
    products_at_reorder_level = Product.objects.filter(quantity__lte=F('reorderlevel'))
    
    context = {
        'products_at_reorder_level': products_at_reorder_level,
    
    }
    
    return render(request, 'relevelorder.html', context)


def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                url='/adminpage'
                x=f'''
                    <script>
                        alert("wlecome admin");
                        window.location.href = "{url}"; 
                    </script>
                '''
                
                return HttpResponse(x)
        else:
            form = AuthenticationForm()  
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'admin_login.html', {'form': form, 'error_message': error_message})
    
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})



def user_register(request):
    registration_successful = False

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            registration_successful = True
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'user_register.html', {'form': form, 'registration_successful': registration_successful})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            # Clear the password field for security reasons
            form.data = form.data.copy()
            form.data['password'] = ''
    else:
        form = AuthenticationForm()
    
    return render(request, 'user_login.html', {'form': form})




def user_logout(request):
    logout(request)
    # Redirect to the index page after logout

    return redirect('product_list')



from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import PasswordChangeForm

@login_required
def profile_update(request):
    print(request.user)

    if request.method == 'POST':
        print(request.user)
        password_form = PasswordChangeForm(request.user,request.POST ,)
        print('kkko',password_form)

        if password_form.is_valid() :
            user = password_form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_login')  # Redirect to the profile update page
    else:
        password_form = PasswordChangeForm(request.user)
    return render(request, 'profile_update.html', {'password_form': password_form})

#122222@@@AA

from django.shortcuts import render, redirect
from .models import Category  # Import your Category model
from .forms import ProductForm  # Ensure your ProductForm is imported

def admin_add(request):
    # Fetch all categories from the database
    categories = Category.objects.prefetch_related('children').all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save()
            messages.success(request, f'Product "{new_product.name}" added successfully!')
            return redirect('adminpage')  # Redirect after adding the product
        else:
            print(form.errors)  # Debug validation issues
    else:
        form = ProductForm()

    # Pass the form and categories to the template
    return render(request, 'admin_add.html', {'form': form, 'categories': categories})



def index(request):   #user page product view
    products = Product.objects.all()
    return render(request, 'products.html', {'productdata': products})

from django.urls import reverse



def product_list(request): #admin page product view
    products = Product.objects.all()
    return render(request, 'myapp/user.html', {'product': products})


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Product
from .forms import ProductForm

# View for editing a product
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')  # Redirect to your product listing page
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

# View for deleting a product
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')  # Redirect to your product listing page
    return render(request, 'delete_product_confirm.html', {'product': product})




def delete_product(request, product_id):
    product_to_delete = get_object_or_404(Product, pk=product_id)  # Assuming product is the name of model

    if request.method == 'POST':
        confirmation = request.POST.get('confirmation', None)
        if confirmation == 'confirmed':
            #product_to_delete.is_active = False  # Set the product as inactive
            product_to_delete.delete()
            return redirect('adminpage')  # Redirect to the user page after deletion
        else:
            return redirect('adminpage')  # Redirect without deleting if not confirmed

    return render(request, 'confirmation_page.html', {'product': product_to_delete})
    


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query, is_active=True)
    return render(request, 'search_results.html', {'products': products, 'query': query})

def search_view(request):
    query = request.GET.get('query', '')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = []

    context = {
        'query': query,
        'products': products,
    }

    return render(request, 'search_results.html', context)



from django.http import JsonResponse
import json

def checkout_view(request):
    cart_iteam=Cart.objects.filter(user=request.user)
    print(cart_iteam)
    total_amount=0
    for iteam in cart_iteam:
        total_amount+=iteam.quantity*iteam.product.price

    if request.method == 'POST':
        fullname = request.POST.get('Fullname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        
        # Handle dynamic person details
        persons = []
        person_count = 0
        while True:
            name = request.POST.get(f'person_name_{person_count}')
            age = request.POST.get(f'person_age_{person_count}')
            gender = request.POST.get(f'person_gender_{person_count}')
            
            if not name or not age or not gender:
                break
            
            persons.append({
                'name': name,
                'age': age,
                'gender': gender,
            })
            person_count += 1
        
        # For debugging or processing
        
        
        print('Persons:', persons)
        params = {
            'fullname': fullname,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'total_amount': total_amount,
            'Persons':persons,
        }
        

        redirect_url = reverse('order_summary')
        # query_string = f"?fullname={fullname}&address={address}&city={city}&postal_code={postal_code}&total_amount={total_amount}&Person={persons}"
        request.session['order_data'] = {
            'fullname': fullname,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'total_amount': 1000,  # Example total amount
            'persons': persons,
        }

        return HttpResponseRedirect(reverse('order_summary'))
        
    return render(request, 'checkout.html', {'total_amount': total_amount})






def order_summary_view(request):
    order_data = request.session.get('order_data', None)

    if order_data:
        fullname = order_data['fullname']
        address = order_data['address']
        city = order_data['city']
        postal_code = order_data['postal_code']
        total_amount = order_data['total_amount']
        persons = order_data['persons']
    
    cart_product = Cart.objects.filter(user=request.user)

    print(persons)
    print(cart_product)
    context = {
        'fullname': fullname,
        'address': address,
        'city': city,
        'postal_code': postal_code,
        'total_amount': total_amount,
        'cart_products': cart_product,
        'persons':persons,
        
    }
    print(persons)

    print('level01212')
    order = Order.objects.create(
                user=request.user,
                fullname=fullname,
                address=address,
                city=city,
                postal_code=postal_code,
                total_amount=total_amount,
            )
            
            # Retrieve and clear cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)
    for cart_item in cart_items:
        order.items.create(product=cart_item.product, quantity=cart_item.quantity)
    
    # cwhart_item.delete()
            
    


    
    return render(request, 'order_summary.html', context)



from .models import Cart
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required(login_url=user_login)
def add_to_cart(request, product_id):

    product = Product.objects.get(pk=product_id)
    # print(isinstance(request.user,UserProfile)
    if request.method=='POST':
        if product.quantity > 0:
            cart_item = Cart(user=request.user, product=product, quantity=1)  # Adjust quantity as needed
            cart_item.save()
            # Decrease product quantity by 1
            product.quantity -= 1
            product.save()
            # Redirect to the cart page or product detail page
            return redirect('cart')  # Redirect to cart page or wherever you manage cart items
        else:
            # Handle out of stock case
            return render(request, 'out_of_stock.html', {'product': product})
        
    else:
        return redirect('product_detail', product_id=product_id)

def decrease_to_cart(request, product_id):
    cart_items = Cart.objects.filter(product_id=product_id,user=request.user).first()
    print('============')
    print("items",cart_items)

    cart_items.delete()
    return redirect('cart')




def remove_from_cart(request, product_id):
    print('--------')
    cart_items = Cart.objects.filter(product_id=product_id,user=request.user).all()
    print('============')
    print("items",cart_items)
    cart_items.delete()
    return redirect('cart')




from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Product
@login_required(login_url=user_login)
def cart(request):
    upcart_items = Cart.objects.filter(user=request.user)
    
    
    # <QuerySet [<Cart: Cart for alvin: Apple VX max>, <Cart: Cart for alvin: Apple VX max>]>
    cart_items={}
    for item in upcart_items:
        # print(item.product.name)
        
        if item.product.name in cart_items:
            cart_items[item.product.name]['quantity']+=1
            cart_items[item.product.name]['total_price']+=cart_items[item.product.name]['price']
            
        else:
            cart_items[item.product.name]={
                'id':item.product.id,
                'name':item.product.name,
                'price':item.product.price,
                'quantity':item.quantity,
                'price':item.product.price,
                'total_price':item.product.price,
                'image':item.product.image
            }
            # print(cart_items)

    total_price = sum(item['total_price'] for item in cart_items.values())

    
    context= {
        'cart_items': cart_items,
        'total_price': total_price
        }
    
    return render(request, 'cart.html',context)
 
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        # Handle adding product to cart
        if product.quantity > 0:
            # Decrement quantity and add to cart logic here
            product.quantity -= 1
            product.save()
            # Add to cart logic here
            return redirect('cart')  # Redirect to cart page after adding to cart
        else:
            # Product is out of stock, handle this case as needed
            return render(request, 'product_detail.html', {'product': product, 'message': 'Out of Stock'})
    else:
        return render(request, 'product_detail.html', {'product': product})
#wishlist
@login_required(login_url=user_login)
def add_to_wishlist(request, product_id):
    if 'wishlist' not in request.session:  
        request.session['wishlist'] = []  

    wishlist = request.session['wishlist'] 
    if product_id not in wishlist:  
        wishlist.append(product_id)
        request.session['wishlist'] = wishlist 
        message='Item added to your wishlist!'
    else:
        message='Item already in wishlist'

    url='/'
    return HttpResponse(pop_message(url,message))
#return HttpRespone
    
@login_required(login_url=user_login)
def remove_to_wishlist(request, product_id):
    wishlist = request.session['wishlist']   
    wishlist.remove(product_id)
    request.session['wishlist']=wishlist
    return redirect('index')





@login_required(login_url=user_login)
def view_to_wishlist(request):
    if 'wishlist' not in request.session:  
        context={
            'product':'',
        }
    else:
        wishlist = request.session['wishlist'] 
        data=Product.objects.filter(id__in=wishlist)
        
        context={
            'data':data
        }

    return render(request,'wishlist.html',context)



#custom popup message

def pop_message(url,message):
    url=url
    x=f'''
        <script>
            alert("{message}");
            window.location.href = "{url}"; 
        </script>
    '''
    return(x)



@login_required
def admin_order_view(request):
    # Admin view to display all orders
    orders = Order.objects.all()

    context = {'orders': orders}

    return render(request, 'order_list_and_detail.html', context)

@login_required
def order_detail_view(request, order_id):
    # Admin view to display order details

    order = Order.objects.get(id=order_id)
    get_image=OrderItem.objects.filter(order=order_id)[:1]#just want to call one element
    for i in get_image:
        get_image=i.product.image
        break
    print(get_image)

    items = order.items.all()
    product_count={}
    for item in items:
        if item.product in product_count.keys():
            product_count[item.product] += 1
        else:
            product_count[item.product] = 1
    

    context = {
                'order': order,
                'get_image':get_image,
                'product_count': product_count}
    return render(request, 'order_detail.html', context)

@login_required
def update_status(request, order_id):
    # Update order status view
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully.')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
    return redirect('order_list_and_detail')  # Redirect to orders list
def order_list_and_detail(request):
    if request.user.is_superuser:
        orders = Order.objects.filter()
    else:
        orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)

from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def user_order_view(request):
    # Fetch orders associated with the logged-in user
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)


def product_list(request, category_id=None):
    # Fetch category based on the provided ID
    category = Category.objects.filter(id=category_id).first() if category_id else None
    if category:
        products = Product.objects.filter(category=category)
        if not products.exists():  # Check if there are no products
            message = "No products available in this category."
        else:
            message = None  # No message if products are available
    else:
        products = Product.objects.all()
        message = None

    return render(request, 'product_list.html', {'products': products, 'message': message})


from django.shortcuts import render
from .models import Category

# def admin_add_product(request):
#     categories = Category.objects.all()  # Fetch all categories from the database
#     return render(request, 'admin_add_product.html', {'categories': categories})


from django.shortcuts import render
from .models import Product, Category

def home(request):
    categories = Category.objects.all()
    selected_category = None
    products = Product.objects.all()

    if 'category' in request.GET:
        category_id = request.GET['category']
        if category_id:
            selected_category = Category.objects.get(pk=category_id)
            products = Product.objects.filter(category=selected_category)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'products': products,
    }
    return render(request, 'home.html', context)

from django.shortcuts import render
from django.db.models import Count
from .models import Product

def products(request):
    # Get all unique categories along with their counts
    categories = Product.objects.values('category').annotate(count=Count('category'))
    
    # Check if category filter is applied
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    # Check if products are available
    products_available = products.exists()  # Returns True if there are products

    return render(request, 'products.html', {
        'productdata': products,
        'categories': categories,
        'products_available': products_available
    })

def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpage')
    else:
        form = SupplierForm()
        print(form)

    context={
        'form':form


    }
    return render(request,'supplier_add.html',context)

def send_request(request,product_id):
    print(product_id)
    if request.method=='POST':
        selected_supplier=request.POST.get('supplier')
        quantity_needed=request.POST.get('quantity')
        date_of_delivery=request.POST.get('DATE')
        stock=Product.objects.get(id=product_id)
        supplier_detail=Supplier.objects.get(id=selected_supplier)
        subject ='REQUEST OF PRODUCT FROM SKULLCANDY'
        St=Supplier_order(
            supplier_id = supplier_detail,
            product_id = stock,
            quantity = quantity_needed,
            delivery_date = date_of_delivery
            

        )
        St.save()
        print(St.id)

        message = f'''
Dear {supplier_detail.name},

We request you to supply the products mentioned below:

<table>
    <tr>
        <th>Product Name</th>
        <th>Quantity</th>
        <th>Date of Delivery</th>
    </tr>
    <tr>
        <td>{stock.name}</td>
        <td>{quantity_needed}</td>
        <td>{date_of_delivery}</td>
    </tr>
</table>

Click the link below to reorder:

[Insert link here]

Best regards,
Roboindia Team
''' 
        message = f'''
Dear {supplier_detail.name},

We request you to supply the products mentioned below:

        Product Name:{stock.name}
        Quantity:{quantity_needed}
        Date of Deliv:{date_of_delivery}

        Click the link below to reorder:
        ---------------------------
        http://127.0.0.1:8000/supplier/{St.id}
        ----------------------------
        
        


Best regards,
Skullcandy Team
'''




        send_mail_from_website(subject,message,supplier_detail.email)
        print(message)
        
    
        return HttpResponse(pop_message('/adminpage','Requested for product'))  # Replace with your success URL

    suplier=Supplier.objects.all()
    context={
        'suppliers':suplier
    }
    
    return render(request,'send_suopplier_request.html',context)

def supplier_replay(request,id):
    print(id)
    order_detail=Supplier_order.objects.get(id=id)
    print(order_detail.supplier_id.name)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        date_of_delivery = request.POST.get('date_of_delivery')
        status = request.POST.get('status')
        
        if quantity:
            order_detail.quantity = quantity
        if date_of_delivery:
            order_detail.date_of_delivery = date_of_delivery
        if status:
            order_detail.status = status
        order_detail.save()
        context={
        'order_detail':order_detail

        }
        
        return render(request,'supplier_success.html',context)
        

    context={        

        'order_detail':order_detail

    }
    return render(request,'supplier.html',context)


# views.py
from django.shortcuts import render
from .models import SupplierOrder

def supplier_replies(request):
    orders = Supplier_order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'supplier_replies.html', context)

def supplier_replay(request, id):
    order_detail = SupplierOrder.objects.get(id=id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        date_of_delivery = request.POST.get('date_of_delivery')
        status = request.POST.get('status')
        
        if quantity:
            order_detail.quantity = quantity
        if date_of_delivery:
            order_detail.date_of_delivery = date_of_delivery
        if status:
            order_detail.status = status
        order_detail.save()
        
        context = {'order_detail': order_detail}
        return render(request, 'supplier_success.html', context)

    context = {'order_detail': order_detail}
    return render(request, 'supplier.html', context)


def welcome(request):
    return render(request, 'welcome.html')



#recommendation views

from django.shortcuts import render
import google.generativeai as genai

# Set up the Google Generative AI API key
api_key = 'AIzaSyAVfwfMaAKqxThTKMaBqGSHCSbdyUOMxAE'
genai.configure(api_key=api_key)

# View to display the form and collect user input



def recommendation_form(request):
    return render(request, 'recommendation_from.html') 


# View to handle the form submission and generate the recommendation
from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from google.generativeai import GenerativeModel  # Ensure you have the correct import for the AI model

# Set up the Google Generative AI API key
API_KEY = 'AIzaSyAVfwfMaAKqxThTKMaBqGSHCSbdyUOMxAE'
genai.configure(api_key=API_KEY)


def generate_recommendation(request):
    if request.method == 'POST':
        # Collect user preferences from the form
        climate = request.POST.get('climate')
        activities = request.POST.get('activities')
        location_preference = request.POST.get('location_preference')
        accommodation = request.POST.get('accommodation')
        cuisine = request.POST.get('cuisine')
        transportation = request.POST.get('transportation')
        group_preference = request.POST.get('group_preference')
        budget = request.POST.get('budget')
        attractions = request.POST.get('attractions')
        vacation_pace = request.POST.get('vacation_pace')

        # Formulate the prompt for the Generative AI model
        prompt = (
            "Based on the following preferences, recommend the best travel destination:\n"
            f"Preferred Climate: {climate}\n"
            f"Preferred Activities: {activities}\n"
            f"Location Preference: {location_preference}\n"
            f"Accommodation: {accommodation}\n"
            f"Cuisine: {cuisine}\n"
            f"Transportation: {transportation}\n"
            f"Group Preference: {group_preference}\n"
            f"Budget: {budget}\n"
            f"Attractions: {attractions}\n"
            f"Vacation Pace: {vacation_pace}\n"
        )

        try:
            # Generate a recommendation using the Generative AI model
            model = GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            recommendation = response.text

            return render(request, 'recommendation_results.html', {'recommendation': recommendation})

        except Exception as e:
            return render(request, 'recommendation_results.html', {'recommendation': f"An error occurred: {e}"})

    # Render the initial form for collecting preferences
    return render(request, 'recommendation_form.html')



 

import google.generativeai as genai

# Configure your Google API key
GOOGLE_Gemini_API_KEY = 'AIzaSyAwDVSbu5KE3hw_x3jdg2DcUrfidfsaEuo'
genai.configure(api_key=GOOGLE_Gemini_API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-pro')


@login_required
def chat_home(request):
    # Fetch chat history for the logged-in user
    chat_history = ChatHistory.objects.filter(user=request.user).order_by('created_at')

    if request.method == 'POST':
        user_input = request.POST.get('userInput').strip()

        if user_input:
            try:
                # Generate response using Google Generative AI
                response = model.generate_content(user_input)
                bot_response = response.text

                # Save user input and bot response to the database
                ChatHistory.objects.create(
                    user=request.user,
                    message_input=user_input,
                    bot_response=bot_response
                )

            except Exception as e:
                messages.warning(request, f"An error occurred: {str(e)}")
        
        return redirect('chat_home')

    context = {
        'get_history': chat_history,
        'messages': messages.get_messages(request)
    }

    return render(request, 'chat.html', context)



def dashboard(request):
    return render(request, 'dashboard.html')

