from django.shortcuts import render
from django.views.generic import FormView
from .models import Office
from .forms import AddRoomForm
from django.contrib import messages
from django.shortcuts import redirect


def view_rooms(request):
    """Displaying all rooms available"""

    title = "All Rooms"

    rooms = Office.objects.all().order_by('room_capacity')
    if not rooms:
        messages.info(request, 'All Rooms are vacant !')

    return render(request, 'offices_available.html', {'offices': rooms, 'title': title})


class AddRoom(FormView):
    """Adding an Office to the database"""

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
            room = Office.objects.create(room_name=room_name, room_capacity=room_capacity,
                                         projector_available=projector_available)
            messages.success(request, f'Room "{room.room_name}" has been added to the database.')

            return redirect(view_rooms)

        return render(request, 'add_room.html', {'title': self.title, 'form': form})


def room_details(request, pk):
    """Displaying room details"""

    title = "Room details"

    room = Office.object.get(id=pk)


# TODO: Implement edit_room
class EditRoomView(FormView):

    def get(self, request, pk):
        pass


# TODO: Implement delete_room
def delete_room(request, pk):
    """Delete room by the given id"""

    room_to_delete = Office.objects.get(id=pk)
    room_to_delete.delete()
    messages.success(request, f'Room name "{room_to_delete.room_name}" has been deleted from the database.')
    return redirect(view_rooms)


# TODO: Implement book_room
def book_room(request, pk):
    pass
