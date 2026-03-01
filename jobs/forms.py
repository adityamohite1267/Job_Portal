from django import forms
from .models import Job, Location
from accounts.models import Skill

class JobForm(forms.ModelForm):
    city = forms.CharField(max_length=125,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}))
    state = forms.CharField(max_length=125,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter State'}))
    class Meta:
        model = Job
        fields = [
            'title', 'company_name', 'description',
            'skills_required', 'job_type', 'salary', 'is_active',
        ]
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'skills_required': forms.SelectMultiple(attrs={'class':'form-select select2'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills_required'].queryset = Skill.objects.all().order_by('name')
        self.fields['skills_required'].required = True