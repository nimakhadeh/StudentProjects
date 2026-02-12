from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cars.models import Car
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    """Display cart contents"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required
def add_to_cart(request, car_id):
    """Add car to cart"""
    car = get_object_or_404(Car, id=car_id, is_active=True)
    
    # Check stock
    if car.stock <= 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'این خودرو ناموجود است'})
        messages.error(request, 'این خودرو ناموجود است')
        return redirect('cars:detail', pk=car_id)
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create cart item - THIS IS THE FIX!
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        car=car,
        defaults={'quantity': 1}
    )
    
    if not item_created:
        # Update quantity if item exists
        if cart_item.quantity < car.stock:
            cart_item.quantity += 1
            cart_item.save()
            message_text = f'{car} به سبد اضافه شد'
        else:
            message_text = 'موجودی کافی نیست'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': message_text})
            messages.warning(request, message_text)
            return redirect('cars:list')
    else:
        message_text = f'{car} به سبد اضافه شد'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_total_items(),
            'message': message_text
        })
    
    messages.success(request, message_text)
    return redirect('cars:list')


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'آیتم از سبد حذف شد')
        elif quantity <= cart_item.car.stock:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'سبد به‌روزرسانی شد')
        else:
            messages.error(request, 'موجودی کافی نیست')
            
    except ValueError:
        messages.error(request, 'مقدار نامعتبر')
    
    return redirect('cart:detail')


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    car_name = str(cart_item.car)
    cart_item.delete()
    messages.success(request, f'{car_name} از سبد حذف شد')
    return redirect('cart:detail')


@login_required
def clear_cart(request):
    """Clear entire cart"""
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, 'سبد خرید خالی شد')
    return redirect('cart:detail')
