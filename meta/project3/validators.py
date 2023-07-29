from rest_framework.serializers import ValidationError

class EvenYoutubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value is not None and value != "" and not value.startswith("https://www.youtube.com/watch?v="):
            raise ValidationError("Можно только ссылки на Youtube.")