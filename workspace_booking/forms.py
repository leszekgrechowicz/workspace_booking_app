from django import forms
from workspace_booking.models import Room
from django.core.exceptions import ObjectDoesNotExist

ATTRS = {
    'class': 'form-control mt-1',
}


class AddRoomForm(forms.Form):
    room_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs=ATTRS))
    room_capacity = forms.IntegerField(min_value=0, max_value=10000, widget=forms.NumberInput(attrs=ATTRS))
    projector_available = forms.BooleanField(label='Is projector available', label_suffix=" :  ", required=False,
                                             widget=forms.widgets.CheckboxInput())

    def clean_room_name(self, *args, **kwargs):

        room_name = self.cleaned_data.get("room_name")

        try:
            Room.objects.get(room_name__iexact=room_name)

        except ObjectDoesNotExist:
            return room_name

        raise forms.ValidationError(f"Room '{room_name}' already exist in the data base !")


class EditRoomForm(forms.Form):
    room_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs=ATTRS))
    room_capacity = forms.IntegerField(min_value=0, max_value=10000, widget=forms.NumberInput(attrs=ATTRS))
    projector_available = forms.BooleanField(label='Is projector available', label_suffix=" :  ", required=False,
                                             widget=forms.widgets.CheckboxInput())


class BookRoomForm(forms.Form):
    comment = forms.Textarea()
    date = forms.DateInput()
