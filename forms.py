from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Column, Layout, Row, Submit
from django import forms
from locations.models import CameraStation, MacroSite

from .models import Upload


class AnnotationForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}), required=False)

    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}), required=False)

    macrosites = forms.ModelChoiceField(queryset=MacroSite.objects.all(), required=True)

    camera_stations = forms.ModelChoiceField(queryset=CameraStation.objects.all(), required=False)

    criteria = [
        ("species", "Annotate Species"),
        ("human", "Annotate Human Activity"),
        ("animal", "Annotate Animal Activity"),
        ("blank", "Annotate Blanks"),
    ]

    annotation_choices = forms.ChoiceField(choices=criteria, widget=forms.RadioSelect, label="Annotation Criteria")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("start_date", css_class="form-group col-md-6"),
                Column("end_date", css_class="form-group col-md-6"),
            ),
            Row(
                Column("macrosites", css_class="form-group col-12"),
            ),
            Row(
                Column("camera_stations", css_class="form-group col-12"),
            ),
            Row(
                Column("annotation_choices", css_class="form-group col-12"),
            ),
            Row(
                Column(Submit("submit", "Annotate", css_class="form-group btn-primary")),
                css_class="text-center",
            ),
        )
        self.helper.form_show_errors = True
