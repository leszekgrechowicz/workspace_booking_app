from django.shortcuts import render
from django.views.generic import FormView
from .models import Room, Reservation
from .forms import AddRoomForm, BookRoomForm, AddPhotoForm, EditRoomForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db import IntegrityError
from datetime import datetime


class RoomsView(FormView):
    """Displaying all rooms available"""
    template_name = 'show_rooms.html'
    title = "All Rooms"

    def get(self, request):
        rooms = Room.objects.all().order_by('room_capacity')
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = datetime.now().date() in reservation_dates
        if not rooms:
            messages.info(request, 'All Rooms are vacant !')

        return render(request, self.template_name, {'rooms': rooms,
                                                    'title': self.title})


class AddRoomView(FormView):
    """Adding the Room to the database"""
    template_name = 'add_room.html'
    title = "Add Room"

    def get(self, request):
        form = AddRoomForm()
        return render(request, self.template_name, {'title': self.title, 'form': form})

    def post(self, request):
        form = AddRoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = Room.objects.create(room_name=form.cleaned_data['room_name'],
                                       room_capacity=form.cleaned_data['room_capacity'],
                                       projector_available=form.cleaned_data['projector_available'],
                                       size=form.cleaned_data['size'],
                                       building_floor=form.cleaned_data['building_floor'],
                                       image=form.cleaned_data['image']
                                       )
            messages.success(request, f'Room "{room.room_name}" has been added to the database.')

            return redirect('offices')

        return render(request, self.template_name, {'title': self.title, 'form': form})


class EditRoomView(FormView):
    """Edits Room details"""
    template_name = 'edit_room.html'
    title = 'Edit Room'

    def get(self, request, pk):

        room_to_edit = Room.objects.get(id=pk)

        pre_data = {
            'room_name': room_to_edit.room_name,
            'room_capacity': room_to_edit.room_capacity,
            'size': room_to_edit.size,
            'building_floor': room_to_edit.building_floor,
            'image': room_to_edit.image,
        }
        form = EditRoomForm(initial=pre_data)

        return render(request, self.template_name, {'title': self.title, 'form': form, 'office': room_to_edit})

    def post(self, request, pk):
        room_to_edit = Room.objects.get(id=pk)
        form = EditRoomForm(request.POST, request.FILES, instance=room_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Room details updated !')
            return redirect('offices')

        else:
            return render(request, self.template_name, {'title': self.title, 'form': form})


def delete_room(request, pk):
    """Deletes room by the given id"""

    room_to_delete = Room.objects.get(id=pk)
    room_to_delete.image.delete()
    room_to_delete.delete()
    messages.success(request,
                     f'Room name "{room_to_delete.room_name}" has been successfully removed from the database.')
    return redirect('offices')


class BookRoomView(FormView):
    template_name = 'book_room.html'
    title = 'Book Room'

    def get(self, request, pk):
        todays_date = datetime.now().date()
        room_to_book = Room.objects.get(id=pk)

        form = BookRoomForm()
        return render(request, self.template_name, {'date': todays_date,
                                                    'room': room_to_book,
                                                    'title': self.title,
                                                    'form': form})

    def post(self, request, pk):
        form = BookRoomForm(request.POST or None)
        room_to_book = Room.objects.get(id=pk)
        if form.is_valid():
            date = form.cleaned_data['date']
            company = form.cleaned_data['company']
            comment = form.cleaned_data['comment']

            try:
                Reservation.objects.create(room=room_to_book, date=date, company_name=company, comment=comment)
            except IntegrityError:
                messages.warning(request, f'Room "{room_to_book.room_name}" is already booked at {date}')
                return render(request, self.template_name, {'room': room_to_book, 'title': self.title, 'form': form})

            messages.success(request, f'Room "{room_to_book.room_name}" has been booked for {date} with {company}. ')
            return redirect('offices')
        # messages.warning(request, f'{form.errors}')
        return render(request, self.template_name, {'room': room_to_book, 'title': self.title, 'form': form})
