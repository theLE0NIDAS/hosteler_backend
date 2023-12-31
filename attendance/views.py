from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from base.middleware import admin_required, student_required, admin_or_student_required
from django.db.models import Q
from datetime import datetime, date
from django.utils import timezone
from .models import Attendance, Leave, Rebate
from room.models import Room
from student.models import Student
from mess.models import Mess
from .forms import LeaveForm, AttendanceForm, LeaveUpdateForm
from .serializers import AttendanceSerializer, LeaveSerializer, RebateSerializer
from decimal import Decimal

# ---------------------------------------------------------------------------------#
# Attendance Api's
# ---------------------------------------------------------------------------------#
@api_view(['GET'])
def api_attendance_list(request, date):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)

    # date = datetime.strptime(date, '%Y-%m-%d').date()
    # print(date)
    attendances = Attendance.objects.filter(date=date)
    if attendances.exists():
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    return Response({'message': 'No attendance found'}, status=404)

@api_view(['GET'])
def api_attendance_detail(request, roll_number, date):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    attendance = Attendance.objects.filter(student=roll_number, date=date)
    if attendance.exists():
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)
    return Response({'message': 'No attendance found'}, status=404)

@api_view(['GET'])
def api_attendance_search(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    q = request.GET.get('q', '')
    attendances = Attendance.objects.filter(
        Q(student__icontains=q) | 
        Q(date__icontains=q) |
        Q(status__icontains=q)
    )
    if attendances:
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    return Response({'message': 'No attendance found'}, status=404)

@api_view(['GET'])
def api_attendance_create(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    rooms = Room.objects.filter(occupancy_status='OCCUPIED')
    leaves = Leave.objects.filter(status='APPROVED')

    attendance_data = []
    
    for room in rooms:
        student = room.student
        now = datetime.now().date()
        
        # Check if the student is on leave for today
        is_on_leave = any(leave.student == student and leave.leave_from <= now <= leave.leave_to for leave in leaves)
        
        attendance_status = 'LEAVE' if is_on_leave else 'ABSENT'
        
        attendance_data.append({
            'student': student,
            'date': now,
            'status': attendance_status
        })
    attendance_serializer = AttendanceSerializer(data=attendance_data, many=True)
    if attendance_serializer.is_valid():
        attendance_serializer.save()
        return Response(attendance_serializer.data, status=201)
    return Response(attendance_serializer.errors, status=400)

@api_view(['PUT'])
def api_attendance_update(request, roll_number):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    student = get_object_or_404(Student, roll_number=roll_number)
    attendance = Attendance.objects.get(date=date.today(), student=student)
    form = AttendanceForm(request.data, instance=attendance)
    if form.is_valid():
        # attendance = form.save(commit=False)
        attendance.status = form.cleaned_data['status']
        attendance.save()
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=201)
    return Response(form.errors, status=400)

# @api_view(['DELETE'])
# def api_attendance_delete(request, attendance_id):
#     attendance = get_object_or_404(Attendance, id=attendance_id)
#     attendance.delete()
#     return Response(status=204)




# ---------------------------------------------------------------------------------#
# Leave Api's
# ---------------------------------------------------------------------------------#
@api_view(['GET'])
def api_leave_list(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    try:
        leaves = Leave.objects.all()
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)
    except Leave.DoesNotExist:
        return Response({'error': 'No leaves found'}, status=404)


@api_view(['GET'])
def api_myleave(request, roll_number):
    if not student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    leaves = Leave.objects.filter(student=roll_number)
    if leaves:
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)
    return Response({'message': 'No leaves found'}, status=404)

# @api_view(['GET'])
# def api_leave_detail(request, leave_id):
#     leave = Leave.objects.get(id=leave_id)
#     serializer = LeaveSerializer(leave)
#     return Response(serializer.data)

@api_view(['POST'])
def api_leave_create(request):
    if not student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    form = LeaveForm(request.data)
    if form.is_valid():
        
        leave = form.save(commit=False)
        leave.created_at = timezone.now()
        last_leave = Leave.objects.first()  # Get the last leave object
        print(last_leave)
        if last_leave:
            leave.leave_id = last_leave.leave_id + 1  # Increment the leave_id
        else:
            leave.leave_id = 1  # Set the initial leave_id if no leave objects exist yet
        leave.save()
        serializer = LeaveSerializer(leave)
        return Response(serializer.data, status=201)
    return Response(form.errors, status=400)

@api_view(['PUT'])
def api_leave_update(request, leave_id):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    leave = Leave.objects.get(leave_id=leave_id)
    form = LeaveUpdateForm(request.data, instance=leave)
    if form.is_valid():
        # leave = form.save(commit=False)
        leave.status = form.cleaned_data['status']
        if leave.status == 'APPROVED':
            date1 = leave.leave_from
            date2 = leave.leave_to
            delta = date2 - date1
            num_of_days = delta.days
            mess = Mess.objects.first()
            if 3 <= num_of_days <= 7:
                rebate_amount = (mess.rebate_percentage / 100) * mess.cost_per_day * num_of_days
            elif num_of_days > 7:
                rebate_amount = (mess.rebate_percentage / 100) * mess.cost_per_day * 7
            else:
                rebate_amount = 0.0

            if rebate_amount >= 0:
                leave.rebate_associated = rebate_amount
        leave.save()
        serializer = LeaveSerializer(leave)
        return Response(serializer.data, status=201)
    return Response(form.errors, status=400)

@api_view(['DELETE'])
def api_leave_delete(request, leave_id):
    if not student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    leave = Leave.objects.get(leave_id=leave_id)
    leave.delete()
    return Response(status=204)



# ---------------------------------------------------------------------------------#
# Rebate Api's
# ---------------------------------------------------------------------------------#
@api_view(['GET'])
def api_rebate_list(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    rebates = Rebate.objects.all()
    if rebates:
        serializer = RebateSerializer(rebates, many=True)
        return Response(serializer.data)
    return Response({'message': 'No rebates found'}, status=404)

@api_view(['GET'])
def api_total_rebate_amount(request, roll_number):
    if not admin_or_student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    rebates = Rebate.objects.filter(student=roll_number)
    initial_rebate_amount = 0.0
    total_rebate_amount = Decimal(initial_rebate_amount)
    for rebate in rebates:
        total_rebate_amount = total_rebate_amount + rebate.rebate_amount
    return Response(total_rebate_amount)

# @api_view(['GET'])
# def api_rebate_detail(request, rebate_id):
#     rebate = Rebate.objects.get(id=rebate_id)
#     serializer = RebateSerializer(rebate)
#     return Response(serializer.data)
    
@api_view(['POST'])
def api_rebate_create(request): 
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    leaves = Leave.objects.filter(status='APPROVED')
    for leave in leaves:
        date1 = leave.leave_from
        date2 = leave.leave_to
        delta = date2 - date1
        num_of_days = delta.days
        mess = Mess.objects.first()

        last_rebate = Rebate.objects.last()  # Get the last rebate object
        if last_rebate:
            rebate_id = last_rebate.rebate_id + 1  # Increment the rebate_id
        else:
            rebate_id = 1  # Set the initial rebate_id if no rebate objects exist yet

        if 3 <= num_of_days <= 7:
            rebate_amount = (mess.rebate_percentage / 100) * mess.cost_per_day * num_of_days
        elif num_of_days > 7:
            rebate_amount = (mess.rebate_percentage / 100) * mess.cost_per_day * 7
        else:
            rebate_amount = 0.0

        if rebate_amount >= 0:
            rebate = Rebate.objects.create(rebate_id=rebate_id, total_contiguous_leaves=num_of_days, rebate_amount=rebate_amount, student=leave.student, leave_id=leave)
            rebate_serializer = RebateSerializer(rebate)
            return Response(rebate_serializer.data, status=201)
    
    return Response({'error': 'no rebate'}, status=400)


# @api_view(['PUT'])
# def api_rebate_update(request, rebate_id):
#     rebate = Rebate.objects.get(id=rebate_id)
#     serializer = RebateSerializer(instance=rebate, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)

# @api_view(['DELETE'])
# def api_rebate_delete(request, rebate_id):
#     rebate = Rebate.objects.get(id=rebate_id)
#     rebate.delete()
#     return Response(status=204)