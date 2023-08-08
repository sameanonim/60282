from rest_framework.serializers import ValidationError

class EvenYoutubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    url = item.get(self.field)
                    if url is not None and url != "" and not url.startswith("https://www.youtube.com/watch?v="):
                        raise ValidationError("Можно только ссылки на Youtube.")
                else:
                    raise ValidationError("Неверный формат данных.")
        else:
            if value is not None and value != "" and not value[self.field].startswith("https://www.youtube.com/watch?v="):
                raise ValidationError("Можно только ссылки на Youtube.")