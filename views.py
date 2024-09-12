from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.conf import settings
import paypalrestsdk
from My_app.models import Product, Image, Cart, CartItem
from .forms import UploadImageForm
from django.http import JsonResponse, HttpResponseForbidden
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .forms import CheckoutForm
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Order
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Configure logging
import logging
logger = logging.getLogger(__name__)

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # "sandbox" or "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def HomePage(request):
    products = Product.objects.all()
    uploaded_images = Image.objects.all()  # Fetch images from the Image model
    return render(request, 'home.html', {'products': products, 'uploaded_images': uploaded_images})

def LoginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def SignupPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout


@login_required
# In views.py
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.total_price for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def add_to_cart(request, item_id):
    if request.method == "POST":
        item_type = request.POST.get("item_type")
        if item_type == "product":
            item = get_object_or_404(Product, id=item_id)
            image = None
        elif item_type == "image":
            item = get_object_or_404(Image, id=item_id)
            image = item
            item = None
        else:
            return redirect('home')

        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item, image=image)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('view_cart')
    else:
        return redirect('home')

@login_required
def payment_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    try:
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            logger.info("Payment executed successfully")
            return redirect('home')
        else:
            logger.error(f"Payment execution failed: {payment.error}")
            return redirect('payment_cancel')
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return redirect('payment_cancel')

@login_required
def payment_cancel(request):
    return render(request, 'payment_cancel.html', {"message": "Your payment was canceled."})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def test_paypal_api(request):
    try:
        payment = paypalrestsdk.Payment.all({"count": 1})
        return JsonResponse({'payment': payment}, safe=False)
    except Exception as e:
        logger.error(f"PayPal API error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UploadImageForm()
    return render(request, 'upload_image.html', {'form': form})

@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()
    return redirect('home')

@login_required
def delete_image(request, image_id):
    if request.method == 'POST':
        try:
            image = Image.objects.get(id=image_id)
            image.delete()
            return redirect('home')
        except Image.DoesNotExist:
            return redirect('home')
    else:
        return HttpResponseForbidden("Invalid request method.")
def checkout(request):
    if request.method == 'POST':
        # Handle form submission
        address = request.POST.get('address')
        card = request.POST.get('card')

        # Calculate the total price
        cart_items = CartItem.objects.filter(cart__user=request.user)
        total_price = sum(item.total_price for item in cart_items)

        # Create an Order object
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            payment_status=False  # or True if payment is successful
        )

        # Here, handle your payment and order logic (e.g., save address and card details)
        # Example: Save address and card to a separate model or process payment

        # Redirect to the order success page with the order_id
        return redirect('order_success', order_id=order.id)

    # Calculate total price of cart items
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
@login_required
@require_POST
def remove_from_cart(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    except Cart.DoesNotExist:
        messages.error(request, "No active cart found.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")
    
    return redirect('view_cart')
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {
        'order': order,
    })
 

def generate_order_slip_pdf(request, order_id):
    # Retrieve the order object
    order = get_object_or_404(Order, id=order_id)

    # Retrieve cart items related to the order, if applicable
    cart_items = CartItem.objects.filter(cart__user=order.user)

    # Create a PDF response
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Draw the order details
    p.drawString(100, height - 100, f"Order ID: {order.id}")
    p.drawString(100, height - 120, f"User: {order.user.username}")
    p.drawString(100, height - 140, f"Total Price: ${order.total_price}")
    # Note: Ensure you have an address field in your Order model or modify accordingly
    p.drawString(100, height - 160, f"Address: {order.address}")

    # Draw cart items
    y = height - 200
    for item in cart_items:
        if item.product:
            p.drawString(100, y, f"Product: {item.product.name} x {item.quantity} - ${item.total_price}")
            y -= 20
        elif item.image:
            p.drawString(100, y, f"Image: {item.image.name} x {item.quantity} - ${item.total_price}")
            y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order_id}_slip.pdf"'
    return response
