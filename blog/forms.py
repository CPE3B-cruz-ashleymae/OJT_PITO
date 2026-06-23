from django import forms
from .models import Post
from .models import UserProfile

 
from django import forms
 
 
class PDSLocationForm(forms.Form):
    """
    Mix these fields into your existing PDS ModelForm/Form.
    The JS fills the <select> options at runtime via the PSGC API.
    Django simply receives the submitted PSGC codes as strings.
    """
 
    province = forms.CharField(
        label="Province",
        max_length=10,
        widget=forms.Select(attrs={
            "id": "id_province",
            "class": "location-select",
        }),
    )
 
    municipality = forms.CharField(
        label="Municipality / City",
        max_length=10,
        widget=forms.Select(attrs={
            "id": "id_municipality",
            "class": "location-select",
        }),
    )
 
    barangay = forms.CharField(
        label="Barangay",
        max_length=10,
        widget=forms.Select(attrs={
            "id": "id_barangay",
            "class": "location-select",
        }),
    )
 
    zip_code = forms.CharField(
        label="ZIP Code",
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            "id": "id_zip_code",
            "readonly": True,
            "placeholder": "Auto-filled",
        }),
    )
 
    def clean(self):
        cleaned = super().clean()
        province     = cleaned.get("province")
        municipality = cleaned.get("municipality")
        barangay     = cleaned.get("barangay")
 
        if municipality and not province:
            self.add_error("municipality", "Please select a province first.")
 
        if barangay and not municipality:
            self.add_error("barangay", "Please select a municipality/city first.")
 
        return cleaned

class PDSForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

        province = forms.CharField(
        max_length=10,
        widget=forms.Select(attrs={"id": "id_province"}),
    )
    municipality = forms.CharField(
        max_length=10,
        widget=forms.Select(attrs={"id": "id_municipality"}),
    )
    barangay = forms.CharField(
        max_length=10,
        widget=forms.Select(attrs={"id": "id_barangay"}),
    )
    zip_code = forms.CharField(
        max_length=4, required=False,
        widget=forms.TextInput(attrs={
            "id": "id_zip_code", "readonly": True
        }),
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 py-2 px-3',
                'placeholder': 'Enter title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-light border-0 py-2 px-3',
                'placeholder': 'Enter content',
                'rows': 5
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }