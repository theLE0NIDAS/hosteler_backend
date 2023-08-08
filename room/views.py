from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from base.middleware import admin_required, student_required, admin_or_student_required
from django.db.models import Q
from .forms import RoomForm
from .serializers import RoomSerializer
from .models import Room

@api_view(['GET'])
def api_room_list(request):
    if not admin_or_student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    rooms = Room.objects.all()
    if rooms:
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    return Response({'message': 'No rooms found'}, status=404)

@api_view(['GET'])
def api_room_search(request):
    if not admin_or_student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    q = request.data.get('q') 
    rooms = Room.objects.filter(
        Q(room_number__icontains=q) |
        Q(occupancy_status__icontains=q)
    )
    if rooms:
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    return Response({'message': 'No rooms found'}, status=404)

@api_view(['GET'])
def api_room_detail(request, room_number):
    if not admin_or_student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    room = get_object_or_404(Room, room_number=room_number)
    serializer = RoomSerializer(room)
    return Response(serializer.data)

@api_view(['GET'])
def api_room_detail_by_student(request, roll_number):
    if not admin_or_student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    room = get_object_or_404(Room, student=roll_number)
    serializer = RoomSerializer(room)
    return Response(serializer.data)

@api_view(['POST'])
def api_room_create_floor(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    num_rooms = int(request.data.get('num_rooms'))
    floor_number = int(request.data.get('floor_number'))
    rooms = []
    # last_room = Room.objects.last()
    # if last_room:
    #     last_room_number = last_room.room_number
    #     last_room_floor_number = int(last_room_number[:2])
    # else:
    #     last_room_floor_number = 1

    # if last_room_number
    for i in range(num_rooms):
        room_number = f"{floor_number}{i+1:02d}"
        room = Room.objects.create(
            room_number=room_number,
            floor_number=floor_number
        )
        room.save()
        rooms.append(room)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data, status=201)

@api_view(['PUT'])
def api_room_student_register(request, room_number):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    room = get_object_or_404(Room, room_number=room_number)
    form = RoomForm(request.data, instance=room)
    if form.is_valid():
        room = form.save(commit=False)
        room.occupancy_status = 'OCCUPIED'
        room.save()
        room_serializer = RoomSerializer(room)
        return Response(room_serializer.data, status=201)
    return Response(form.errors, status=400)
    
@api_view(['PUT'])
def api_room_student_deregister(request, room_number):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    room = get_object_or_404(Room, room_number=room_number)
    room.student = None
    room.check_in_date = None
    room.occupancy_status = 'VACANT'
    room.save()
    room_serializer = RoomSerializer(room)
    return Response(room_serializer.data, status=201)

# @api_view(['PUT'])
# def api_room_update(request, room_number):
#     room = Room.objects.get(room_number=room_number)
#     room_serializer = RoomSerializer(room, data=request.data)
#     if room_serializer.is_valid():
#         room_serializer.save()
#         return Response(room_serializer.data, status=201)
#     return Response(status=400)


@api_view(['DELETE'])
def api_room_delete(request, room_number):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    room = get_object_or_404(Room, room_number=room_number)
    room.delete()
    return Response(status=204)
