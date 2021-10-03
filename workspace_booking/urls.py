from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_rooms, name='offices'),
    path('add-room/', views.AddRoom.as_view(), name='add-office'),
    path('room-details/<int:pk>', views.room_details, name='room-details'),
    path('edit-room/<int:pk>', views.EditRoomView.as_view(), name='edit-room'),
    path('delete-room/<int:pk>', views.delete_room, name='delete-room'),
    path('book-room/<int:pk>', views.BookRoomView.as_view(), name='book-room'),
]
