from django.utils.deprecation import MiddlewareMixin

class NotificationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and not request.session.get('reset_notifications', False):
            user_profile = request.user.userprofile
            notifications_count = user_profile.notifications.count()
            if 'notifications_count' not in request.session or request.session['notifications_count'] != notifications_count:
                request.session['notifications_count'] = notifications_count
                request.session.modified = True
