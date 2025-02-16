from django import forms
from .models import Participant, Event, Category

class StyledFormMixin:
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500 hover:border-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}",
                    "rows": 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class":"border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500 hover:border-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            elif isinstance(field.widget, forms.TimeInput):
              field.widget.attrs.update({
              "type": "time",
              "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500 hover:border-blue-500"
               })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    "class": self.default_classes + " bg-white appearance-none"
                })
            else:
                field.widget.attrs.update({'class': self.default_classes})


class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.SelectDateWidget,
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500 hover:border-blue-500'
            }),
            'category': forms.Select(attrs={  
                "class": "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-green-500 hover:border-green-500"
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.order_by('name').distinct()  
        self.apply_styled_widgets()  


class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class ParticipantModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {'email': forms.EmailInput, 'events': forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
