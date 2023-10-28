document.addEventListener("DOMContentLoaded", function () {
    const notifications = document.querySelectorAll('.notificationCard');
    const markAll = document.getElementById('mark-as-read');

    notifications.forEach((notification) => {
        notification.addEventListener('click', () => {
            if (notification.classList.contains('unread')) {
                notification.classList.remove('unread');
                markNotificationAsRead(notification.getAttribute('data-notification-id'));
            }
        });
    });

    markAll.addEventListener('click', () => {
        notifications.forEach((notification) => {
            notification.classList.remove('unread');
            markNotificationAsRead(notification.getAttribute('data-notification-id'));
        });
    });

    function markNotificationAsRead(notificationId) {
        // You can make an AJAX request to your server to mark the notification as read.
        // You can use the notificationId to identify and update the notification.
    }
});
