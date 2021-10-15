from django import forms
from workspace_booking.models import Room, Reservation
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

ATTRS = {
    'class': 'form-control mt-1',

}

BOOK_ROOM_ATTRS = {
    'class': 'form-control mt-1',
    'style': 'margin: auto;',
}

TEXT_AREA_ATTRS = {
    'class': 'form-control mt-1',
    'style': 'max-height: 125px;',

}


class AddRoomForm(forms.Form):
    room_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs=BOOK_ROOM_ATTRS))
    room_capacity = forms.IntegerField(min_value=0, max_value=10000,
                                       widget=forms.NumberInput(attrs=BOOK_ROOM_ATTRS))

    size = forms.CharField(max_length=70, required=False, widget=forms.TextInput(attrs=BOOK_ROOM_ATTRS))
    building_floor = forms.CharField(max_length=70, required=False, widget=forms.TextInput(attrs=BOOK_ROOM_ATTRS))
    image = forms.ImageField(required=False)
    projector_available = forms.BooleanField(label='Is projector available', label_suffix=":", required=False)

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
    projector_available = forms.BooleanField(label='Is projector available', label_suffix=":", required=False,
                                             widget=forms.widgets.CheckboxInput())


class DateInput(forms.DateInput):
    input_type = 'date'


class BookRoomForm(forms.Form):
    date = forms.DateField(widget=DateInput(attrs=ATTRS))
    company = forms.CharField(max_length=255, widget=forms.TextInput(attrs=ATTRS), required=False)
    comment = forms.CharField(widget=forms.widgets.Textarea(attrs=TEXT_AREA_ATTRS))

    def clean_date(self):
        date = self.cleaned_data.get('date')
        date_today = datetime.now().date()

        if date > date_today:
            return date

        raise forms.ValidationError(f"Invalid date, you cannot book for the past date !")


class AddPhoto(forms.Form):
    image = forms.ImageField(required=True)
