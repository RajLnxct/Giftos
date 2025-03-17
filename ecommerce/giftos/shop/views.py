from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings    
from .forms import *
from .models import *

# ------------- Home Func ---------------
def home(request):
    product =Product.objects.all()[:10:3]
    slider = Slider.objects.all()
    data = {
        'slider':slider,
        'product':product
    }
    return render(request,'home/index.html',data)

# ------------- Contact Func ---------------
def contact(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact_data = Contact(name=name,email=email,phone=phone,message=message)
        contact_data.save()
        send_mail(
            "Thank YOU",
            f"Dear {name},\n\nThank you for reaching out to us! We appreciate you taking the time to contact us and we are happy to help.\n\n Regards,\nGiftos",
            "raj.pitroda.lnxct@gmail.com",
            [email]
        )
        return redirect('shop:contactus')
    return render(request,'home/contact.html')

# ------------- Shoping Func ---------------
def shop(request):
    category = Category.objects.all()
    products = Product.objects.all()
   
    # Search
    if 'search' in request.GET:
        search = request.GET['search']
        products = Product.objects.filter(name__icontains=search) | Product.objects.filter(category__name__icontains=search)
    else:
        products = Product.objects.all()

    # Filter by category and price
    selected_categories = request.GET.getlist('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if selected_categories:
        products = products.filter(category__id__in=selected_categories)
    
    if max_price == '20000':
        products = Product.objects.filter(price__gte=min_price)  # Only filter by min price if max price is 20000+
    else:   
        if min_price and max_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            products = products.filter(price__gte=min_price)
        elif max_price:
            products = products.filter(price__lte=max_price)

    context = {
        'category': category,
        'product': products,
    }
    return render(request,'home/shop.html',context)

# ------------- Testimonial Func ---------------
def testimonial(request):
    return render(request,'home/testimonial.html')


# ------------- Whyus Func ---------------
def why(request):
    return render(request,'home/why.html')

# ------------- Login Func ---------------
def Login(request):
    if request.method=='POST':
        form  = ReCaptcha(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            User = authenticate(email=email,password=password)
            if User is not None:
                login(request,User)
                return redirect('/')
            else:
                messages.error(request,"Email and Password is incorrect!")

    else:
        form = ReCaptcha()    
    return render(request,'login.html',{'form':form})

# ------------- Registration Func ---------------   
def signup(request):
    if request.method == 'POST':
        Register_form = RegisterUser(request.POST)
        if Register_form.is_valid():
            Register_form.save()
            return redirect('shop:login')
    else:
        Register_form = RegisterUser()
    return render(request,'signup.html', {'Register_form': Register_form})

# ------------- Logout Func ---------------
def Logout(request):
    logout(request)
    return redirect('/')

# ------------- Showing Cart  ---------------
def viewCart(request):
    if request.user.is_authenticated:
        cart, created  = Cart.objects.get_or_create(user=request.user)
        # User is logged in, retrieve the cart from the database
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if created:
            pass
    else:
        # User is not logged in, retrieve cart items from the session
        cart_items = request.session.get('cart', [])
        # Convert session cart items to objects for display
        cart_items = [
            {
                'product': get_object_or_404(Product, id=item['product_id']),
                'quantity': item['quantity']
            }
            for item in cart_items
        ]
    
    # Calculate total price for authenticated users
    if request.user.is_authenticated:
        total_price = sum(item.product.price * item.quantity for item in cart_items)
    else:
        # For unauthenticated users, we need to calculate the total price based on session data
        total_price = sum(item['product'].price * item['quantity'] for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'home/cart.html', context)

# ------------- Adding cart ---------------
def addcart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # User is logged in, use the database cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            # If the item already exists in the cart, increase the quantity
            cart_item.quantity += 1
            cart_item.save()
        else:
            pass
    else:
        # User is not logged in, use the session cart
        cart = request.session.get('cart', [])
        
        # Ensure cart is a list
        if not isinstance(cart, list):
            cart = []  # Reset to an empty list if it's not a list

        # Check if the product is already in the session cart
        for i, item in enumerate(cart):
            if item.get('product_id') == product_id:
                cart[i]['quantity'] += 1
                break
        else:
            # If the product is not in the cart, add it
            cart.append({'product_id': product_id, 'quantity': 1})
        
        # Save the updated cart back to the session
        request.session['cart'] = cart
    # Redirect to the view cart page
    return redirect('shop:viewcart')
# ------------- Removeing cart ---------------

def removecart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('shop:viewcart')

def increment(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart = request.session.get('cart', [])
        for item in cart:
            if item['product_id'] == item_id:
                item['quantity'] += 1
                break
        request.session['cart'] = cart
    return redirect('shop:viewcart')

def decrement(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    else:
        cart = request.session.get('cart', [])
        for item in cart:                                                     
            if item['product_id'] == item_id:                             
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                else:
                    cart.remove(item)
                break
        request.session['cart'] = cart
    return redirect('shop:viewcart')

