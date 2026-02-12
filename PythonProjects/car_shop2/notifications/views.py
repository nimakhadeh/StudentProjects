from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .services import LocationService
from .models import UserDevice


@method_decorator(csrf_exempt, name='dispatch')
class RegisterDeviceView(View):
    """ثبت توکن FCM"""
    
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        try:
            data = json.loads(request.body)
            token = data.get('token')
            device_type = data.get('device_type', 'android')
            
            device, created = UserDevice.objects.update_or_create(
                user=request.user,
                device_token=token,
                defaults={'device_type': device_type, 'is_active': True}
            )
            
            return JsonResponse({'success': True, 'created': created})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateLocationView(View):
    """بروزرسانی موقعیت"""
    
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        try:
            data = json.loads(request.body)
            lat = float(data.get('lat'))
            lng = float(data.get('lng'))
            
            request.user.last_lat = lat
            request.user.last_lng = lng
            request.user.location_updated_at = timezone.now()
            request.user.save()
            
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'error': 'Invalid data'}, status=400)