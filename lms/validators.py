from rest_framework.exceptions import ValidationError


class LMSLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        approved_links = ['youtube.com', 'www.youtube.com', 'youtu.be']

        link = value.get(self.field)

        if link:
            if not any(item in link for item in approved_links):
                raise ValidationError('Можно использовать только ссылки на YouTube')