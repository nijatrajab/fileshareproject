from django.forms import ModelForm

from .models import UserFile

class FileModelForm(ModelForm):
    class Meta:
        model = UserFile
        fields = ['browse_file', 'title', 'description']
