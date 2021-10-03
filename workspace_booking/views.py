from django.shortcuts import render
from django.views.generic import FormView
from .models import Room
from .forms import AddRoomForm, EditRoomForm, BookRoomForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db import IntegrityError


def view_rooms(request):
    """Displaying all rooms available"""

    title = "All Rooms"

    rooms = Room.objects.all().order_by('room_capacity')
    if not rooms:
        messages.info(request, 'All Rooms are vacant !')

    return render(request, 'offices_available.html', {'offices': rooms, 'title': title})


class AddRoom(FormView):
    """Adding an Room to the database"""

    title = "Add Room"

    def get(self, request):
        form = AddRoomForm()
        return render(request, 'add_room.html', {'title': self.title, 'form': form})

    def post(self, request):
        form = AddRoomForm(request.POST or None)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            room_capacity = form.cleaned_data['room_capacity']
            projector_available = form.cleaned_data['projector_available']
            room = Room.objects.create(room_name=room_name, room_capacity=room_capacity,
                                       projector_available=projector_available)
            messages.success(request, f'Room "{room.room_name}" has been added to the database.')

            return redirect(view_rooms)

        return render(request, 'add_room.html', {'title': self.title, 'form': form})


def room_details(request, pk):
    """Displaying room details"""

    title = "Room details"
    room = Room.object.get(id=pk)


class EditRoomView(FormView):
    template_name = 'add_room.html'
    title = 'Edit Room'

    def get(self, request, pk):

        room_to_edit = Room.objects.get(id=pk)

        pre_data = {
            'room_name': room_to_edit.room_name,
            'room_capacity': room_to_edit.room_capacity,

        }
        form = EditRoomForm(initial=pre_data)

        return render(request, self.template_name, {'title': self.title, 'form': form})

    def post(self, request, pk):
        form = EditRoomForm(request.POST or None)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            room_capacity = form.cleaned_data['room_capacity']
            projector_available = form.cleaned_data['projector_available']
            try:
                Room.objects.filter(id=pk).update(room_name=room_name, room_capacity=room_capacity,
                                                  projector_available=projector_available)
            except IntegrityError:
                messages.warning(request, f'Room "{room_name}" already exist in the database')
                return render(request, self.template_name, {'title': self.title, 'form': form})

            messages.success(request, 'Room details updated !')
            return redirect(view_rooms)
        else:
            return render(request, self.template_name, {'title': self.title, 'form': form})


def delete_room(request, pk):
    """Deletes room by the given id"""

    room_to_delete = Room.objects.get(id=pk)
    room_to_delete.delete()
    messages.success(request,
                     f'Room name "{room_to_delete.room_name}" has been successfully removed from the database.')
    return redirect(view_rooms)



class BookRoomView(FormView):
    template_name = 'book_room.html'
    title = 'Book Room'

    def get(self, request, pk):
        form = BookRoomForm()
        return render(request, self.template_name, {'title': self.title, 'form': form})
