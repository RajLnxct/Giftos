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
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
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
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'home/cart.html', context)

# ------------- Adding cart ---------------
def addcart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shop:viewcart')

# ------------- Removeing cart ---------------

def removecart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('shop:viewcart')

