from django import forms
from .models import Job, Location
from accounts.models import Skill

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company_name', 'location', 'description',
            'skills_required', 'job_type', 'salary', 'is_active',
        ]
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'skills_required': forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': True}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all().order_by('city')
        self.fields['skills_required'].queryset = Skill.objects.all().order_by('name')
        self.fields['skills_required'].required = True