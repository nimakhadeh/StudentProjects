import random
import string
import time
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from orders.models import Order
from cart.models import Cart
from .models import Payment


@login_required
def payment_process(request, order_id):
    """Payment processing (simulated)"""
    order = get_object_or_404(Order, id=order_id, user=request.user, status='pending')
    
    if request.method == 'POST':
        gateway = request.POST.get('gateway', 'zarinpal')
        
        # Validate card info (simulated)
        card_number = request.POST.get('card_number', '')
        cvv = request.POST.get('cvv', '')
        
        if len(card_number) < 16 or len(cvv) < 3:
            messages.error(request, 'لطفاً اطلاعات کارت را صحیح وارد کنید')
            return render(request, 'payment/process.html', {'order': order})
        
        # Simulate processing delay
        time.sleep(2)
        
        # 80% success rate (simulated)
        is_success = random.random() < 0.8
        
        if is_success:
            # Generate tracking code
            tracking_code = ''.join(random.choices(string.digits, k=10))
            
            with transaction.atomic():
                # Update order status
                order.status = 'processing'
                order.save()
                
                # Create payment record
                Payment.objects.create(
                    order=order,
                    amount=order.total_price,
                    gateway=gateway,
                    status='success',
                    tracking_code=tracking_code,
                    paid_at=datetime.now()
                )
                
                # Reduce stock
                for item in order.items.all():
                    item.car.stock -= item.quantity
                    item.car.save()
                
                # Clear cart
                Cart.objects.filter(user=request.user).delete()
            
            messages.success(request, f'پرداخت موفق! کد رهگیری: {tracking_code}')
            return redirect('payment:success', order_id=order.id, tracking_code=tracking_code)
        else:
            # Random error messages
            errors = [
                'موجودی کافی نیست',
                'خطای ارتباط با بانک',
                'رمز کارت اشتباه است',
                'کارت مسدود شده است',
                'تراکنش توسط بانک رد شد'
            ]
            error_msg = random.choice(errors)
            
            # Create failed payment record
            Payment.objects.create(
                order=order,
                amount=order.total_price,
                gateway=gateway,
                status='failed',
                error_message=error_msg
            )
            
            messages.error(request, f'پرداخت ناموفق: {error_msg}')
            return redirect('payment:failed', order_id=order.id)
    
    return render(request, 'payment/process.html', {'order': order})


@login_required
def payment_success(request, order_id, tracking_code):
    """Payment success page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment = get_object_or_404(Payment, order=order, tracking_code=tracking_code)
    
    return render(request, 'payment/success.html', {
        'order': order,
        'payment': payment,
        'tracking_code': tracking_code
    })


@login_required
def payment_failed(request, order_id):
    """Payment failed page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    latest_payment = order.payments.filter(status='failed').first()
    
    return render(request, 'payment/failed.html', {
        'order': order,
        'payment': latest_payment
    })
