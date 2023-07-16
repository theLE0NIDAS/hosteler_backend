from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from base.middleware import admin_required, student_required, admin_or_student_required
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from .forms import MessForm, MessUpdateForm
from .serializers import MessSerializer
from .models import Mess

# ---------------------------------------------------------------------------------#
# Mess api's
# ---------------------------------------------------------------------------------#
@api_view(['GET'])
def api_mess_detail(request, mess_id):
    if not admin_or_student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    mess = get_object_or_404(Mess, mess_id=mess_id)
    serializer = MessSerializer(mess)
    return Response(serializer.data)

@api_view(['POST'])
def api_mess_create(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    form = MessForm(request.data)
    if form.is_valid():
        mess = form.save(commit=False)
        last_mess = Mess.objects.last()
        if last_mess:
            mess.mess_id = last_mess.mess_id + 1
        else:
            mess.mess_id = 1

        contract_start_date = form.cleaned_data.get('contract_start_date')
        contract_duration_months = form.cleaned_data.get('contract_duration')
        
        if contract_start_date and contract_duration_months:
            contract_end_date = contract_start_date + relativedelta(months=contract_duration_months)
            mess.contract_end_date = contract_end_date
            
        mess.save()
        serializer = MessSerializer(mess)
        return Response(serializer.data, status=201)
    return Response(form.errors, status=400)

@api_view(['PUT'])
def api_mess_update(request, mess_id):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    mess = Mess.objects.get(mess_id=mess_id)
    form = MessUpdateForm(request.data, instance=mess)
    if form.is_valid():
        mess = form.save(commit=False)
        contract_start_date = form.cleaned_data.get('contract_start_date')
        contract_duration_months = form.cleaned_data.get('contract_duration')
        
        if contract_start_date and contract_duration_months:
            contract_end_date = contract_start_date + relativedelta(months=contract_duration_months)
            mess.contract_end_date = contract_end_date
            
        mess.save()
        serializer = MessSerializer(mess)
        return Response(serializer.data, status=202)
    return Response(form.errors, status=400)

@api_view(['DELETE'])
def api_mess_delete(request, mess_id):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    mess = get_object_or_404(Mess, mess_id=mess_id)
    mess.delete()
    return Response(status=204)


# ---------------------------------------------------------------------------------#
# MessMenu api's
# ---------------------------------------------------------------------------------#
# @api_view(['GET'])
# def api_mess_menu(request):
#     mess_menu = MessMenu.objects.first()
#     serializer = MessMenuSerializer(mess_menu, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def api_mess_menu_create(request):
#     serializer = MessMenuSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

# @api_view(['PUT'])
# def api_mess_menu_update(request):
#     mess_menu = MessMenu.objects.first()
#     serializer = MessMenuSerializer(instance=mess_menu, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)