from .models import Cart


def cart_count(request):
    """Add cart item count to context"""
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.get_total_items()
        except Cart.DoesNotExist:
            pass
    return {'cart_count': count}
