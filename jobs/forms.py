from django import forms
from .models import Job, Location,Application
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

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter':forms.Textarea(attrs={'class':'form-control', 'rows':4,'placeholder':'Write your cover letter...'})
        }
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        if resume:
            if not resume.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")

        #if resume size mater
        # if resume.size > 2*1024*1024:
        #     raise forms.ValidationError("Resume file size must be under 2MB.")

        return resume