from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Office
from .forms import AddRoomForm
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.


def view_rooms(request):
    """Displaying all rooms available"""

    title = "All Offices"

    rooms = Office.objects.all()
    if not rooms:
        messages.info(request, 'All Offices are vacant !')

    return render(request, 'offices_available.html', {'offices': rooms, 'title': title})


class AddRoom(TemplateView):
    """Adding an Office to database"""

    title = "Add Office"

    def get(self, request):
        form = AddRoomForm()
        return render(request, 'add_room.html', {'form': form})

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







