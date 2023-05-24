from django.forms import ModelForm
from .models import Companie
from .models import ReportVulnerability


class CompanieForm(ModelForm):
    class Meta:
        model = Companie
        fields = ['name', 'description', 'is_tested']


class ResportVulnForm(ModelForm):
    class Meta:
        model = ReportVulnerability
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False
