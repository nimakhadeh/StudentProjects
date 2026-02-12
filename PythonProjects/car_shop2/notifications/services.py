import requests
from django.conf import settings
from django.utils import timezone
from math import radians, cos, sin, asin, sqrt

from .models import NotificationLog, Campaign, UserDevice


class NotificationService:
    
    @staticmethod
    def haversine_distance(lat1, lng1, lat2, lng2):
        """محاسبه فاصله (کیلومتر)"""
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        dlng = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * asin(sqrt(a))
        return c * 6371
    
    @classmethod
    def send_sms(cls, user, message, campaign=None):
        """ارسال پیامک با کاوه‌نگار"""
        if not hasattr(user, 'allow_marketing_sms') or not user.allow_marketing_sms:
            return None
        
        if not user.phone:
            return None
        
        log = NotificationLog.objects.create(
            user=user,
            campaign=campaign,
            channel='sms',
            title='SMS',
            message=message[:50],
            status='pending'
        )
        
        try:
            url = f"https://api.kavenegar.com/v1/{settings.KAVENEGAR_API_KEY}/sms/send.json"
            payload = {"receptor": user.phone, "message": message}
            response = requests.post(url, data=payload, timeout=10)
            
            if response.status_code == 200:
                log.status = 'sent'
                log.sent_at = timezone.now()
                log.save()
                return log
            else:
                log.status = 'failed'
                log.error_message = response.text
                log.save()
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.save()
        
        return log
    
    @classmethod
    def process_birthday_campaign(cls):
        """تبریک تولد"""
        from accounts.models import User
        from datetime import date
        
        today = date.today()
        users = User.objects.filter(
            birth_date__month=today.month,
            birth_date__day=today.day,
            allow_marketing_sms=True
        )
        
        count = 0
        for user in users:
            name = user.first_name or 'عزیز'
            message = f"🎉 تولدت مبارک {name}!\n3% تخفیف ویژه خرید خودرو تا 7 روز آینده 🚗\nکد: BDAY{user.id}"
            if cls.send_sms(user, message):
                count += 1
        
        return count


class LocationService:
    """سرویس مدیریت موقعیت"""
    
    @staticmethod
    def update_user_location(user, lat, lng):
        """بروزرسانی موقعیت کاربر"""
        user.last_lat = lat
        user.last_lng = lng
        user.location_updated_at = timezone.now()
        user.save(update_fields=['last_lat', 'last_lng', 'location_updated_at'])
        
        # Check for nearby campaigns
        LocationService.check_nearby_campaigns(user, lat, lng)
    
    @staticmethod
    def check_nearby_campaigns(user, lat, lng):
        """بررسی کمپین‌های نزدیک"""
        active_campaigns = Campaign.objects.filter(
            status='active',
            campaign_type='location',
            target_lat__isnull=False
        )
        
        for campaign in active_campaigns:
            distance = NotificationService.haversine_distance(
                lat, lng, campaign.target_lat, campaign.target_lng
            )
            
            if distance <= campaign.radius_km:
                # Check if not already sent recently (cooldown 24h)
                recent = NotificationLog.objects.filter(
                    user=user,
                    campaign=campaign,
                    sent_at__gte=timezone.now() - timedelta(hours=24)
                ).exists()
                
                if not recent:
                    NotificationService.send_push_fcm(
                        user, 
                        campaign.title, 
                        campaign.message,
                        {'campaign_id': str(campaign.id), 'link': campaign.link}
                    )