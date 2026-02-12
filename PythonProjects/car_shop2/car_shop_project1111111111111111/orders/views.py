from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem


@login_required
def order_list(request):
    """List user's orders"""
    orders = request.user.orders.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
@transaction.atomic
def create_order(request):
    """Create order from cart"""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'سبد خرید شما خالی است')
        return redirect('cart:detail')
    
    if cart.items.count() == 0:
        messages.error(request, 'سبد خرید شما خالی است')
        return redirect('cart:detail')
    
    # Check stock availability
    for item in cart.items.all():
        if item.quantity > item.car.stock:
            messages.error(request, f'موجودی {item.car} کافی نیست')
            return redirect('cart:detail')
    
    if request.method == 'POST':
        # Get delivery info
        full_name = request.POST.get('full_name', request.user.get_full_name())
        phone = request.POST.get('phone', request.user.phone or '')
        address = request.POST.get('address', request.user.address or '')
        postal_code = request.POST.get('postal_code', '')
        
        # Validate
        if not all([full_name, phone, address]):
            messages.error(request, 'لطفاً همه فیلدها را پر کنید')
            return render(request, 'orders/checkout.html', {'cart': cart})
        
        # Create order
        total_price = cart.get_total_price()
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            full_name=full_name,
            phone=phone,
            address=address,
            postal_code=postal_code
        )
        
        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                car=item.car,
                quantity=item.quantity,
                price=item.car.price
            )
        
        # Don't delete cart yet - wait for payment
        messages.success(request, 'سفارش با موفقیت ایجاد شد. لطفاً پرداخت کنید.')
        return redirect('payment:process', order_id=order.id)
    
    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
