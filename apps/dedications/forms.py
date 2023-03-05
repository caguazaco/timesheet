from django import forms
from django.forms.models import ModelForm
from .models import Occupation

class OccupationForm(ModelForm):
    class Meta:
        model = Occupation
        fields = ['users', 'date', 'tasks', 'start_time', 'end_time', 'description']
        widgets = {
            'users': forms.HiddenInput(),
            'date': forms.DateInput(attrs = {'type': 'date', 'class': 'calendar'}),
            'start_time': forms.TimeInput(attrs = {'type': 'time'}),
            'end_time': forms.TimeInput(attrs = {'type': 'time'}),
            'description': forms.TextInput(attrs = {'type': 'text'})
        }
        error_messages = {
            'date': {'required': 'Fill date field'},
            'tasks': {'required': 'Fill task field'},
            'start_time': {'required': 'Fill start time field'},
            'end_time': {'required': 'Fill end time field'}
        }
    
    def clean(self):
        super(OccupationForm, self).clean() # Data from the form is fetched using the super function

        user = self.cleaned_data.get('users')
        date = self.cleaned_data.get('date')
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')

        # To validate if it is a create or update action
        if self.instance.id is not None:
            # Excludes the current instance from overlap validation
            id = self.instance.id
            occupations = Occupation.objects.filter(users = user, date = date).exclude(id = id).values()
        else:
            occupations = Occupation.objects.filter(users = user, date = date).values()
        
        errors = 0

        # Process to avoid overlaps
        if start_time and end_time:
            if start_time >= end_time:
                self.errors['end_time'] = self.error_class(['Error. End time less than or equal to start time'])
            
            # Overlapping cases
            for row in occupations:
                if start_time <= row['start_time'] and end_time >= row['end_time']:
                    errors += 1
                if start_time >= row['start_time'] and end_time <= row['end_time']:
                    errors += 1
                if start_time <= row['start_time'] and end_time >= row['start_time']:
                    errors += 1
                if start_time <= row['end_time'] and end_time >= row['end_time']:
                    errors += 1
        
        if errors > 0:
            self._errors['start_time'] = self.error_class(['Error. Overlapping with other dedications'])
        
        # Returns the errors found
        return self.cleaned_data