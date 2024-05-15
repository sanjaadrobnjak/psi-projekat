from app.models import Okrsaj

class GameIdConverter:
    regex = '\\d+'

    def to_python(self, value):
        return Okrsaj.objects.get(pk=int(value))
    
    def to_url(self, value):
        return value.id