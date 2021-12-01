from notification.notification import NotificationType


class Config:
    def __init__(
        self,
        shop_url: str,
        api_key: str,
        api_secret: str,
        static_breakdown_template: dict,
        dynamic_breakdown_template: dict,
        aws_region: str,
        from_timestamp: str,
        num_days_to_look_ahead: int,
        notification_type: NotificationType,
        sender_name: str,
        sender_email: str,
        recipient_email: str,
    ):
        self.shop_url = shop_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.static_breakdown_template = static_breakdown_template
        self.dynamic_breakdown_template = dynamic_breakdown_template
        self.aws_region = aws_region
        self.from_timestamp = from_timestamp
        self.num_days_to_look_ahead = num_days_to_look_ahead
        self.notification_type = notification_type
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.recipient_email = recipient_email
