from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from base.middleware import admin_required, student_required, admin_or_student_required
from django.db.models import Q
from .forms import ComplaintForm, ComplaintUpdateForm
from .models import Complaint
from .serializers import ComplaintSerializer
import cloudinary.uploader

@api_view(['GET'])
def api_complaint_list(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    complaints = Complaint.objects.all()
    print(complaints,'fffffffffffffffffff')
    if complaints:
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data)
    return Response({'message': 'No complaints found'}, status=404)

@api_view(['GET'])
def api_mycomplaint(request, student_id):
    if not student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    complaints = Complaint.objects.filter(student_id=student_id)
    if complaints:
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data)
    return Response({'message': 'No complaints found'}, status=404)

@api_view(['GET'])
def api_complaint_search(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    q = request.data.get('q')
    complaints = Complaint.objects.filter(
        Q(category__icontains=q) | 
        Q(status__icontains=q)
    )
    if complaints:
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data)
    return Response({'message': 'No complaints found'}, status=404)

@api_view(['POST'])
def api_complaint_create(request):
    if not student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    form = ComplaintForm(request.data)
    if form.is_valid():
        complaint = form.save(commit=False)
        photo = request.FILES.get('image',None)
        if photo is not None:
            upload = cloudinary.uploader.upload(photo)
            print(upload['url'])
            complaint.photo = upload['url']
        last_complaint = Complaint.objects.order_by('-complaint_id').first() 
        if last_complaint:
            complaint.complaint_id = last_complaint.complaint_id + 1  
        else:
            complaint.complaint_id = 1  
        complaint.save()
        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data, status=201)
    return Response(form.errors, status=400)

@api_view(['PUT'])
def api_complaint_update(request, complaint_id):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    form = ComplaintUpdateForm(request.data)
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
    if form.is_valid():
        # complaint = form.save(commit=False)
        # complaint.save()
        complaint.status = form.cleaned_data.get('status')
        complaint.remarks = form.cleaned_data.get('remarks')
        complaint.save()
        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data)
    return Response(form.errors, status=400)

@api_view(['DELETE'])
def api_complaint_delete(request, complaint_id):
    if not student_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
    complaint.delete()
    return Response(status=204)