from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from base.middleware import admin_required, student_required, admin_or_student_required
from django.db.models import Q
from .forms import ResourceForm, ResourceUpdateForm
from .models import Resource
from .serializers import ResourceSerializer

@api_view(['GET'])
def api_resource_list(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    resources = Resource.objects.all()
    if resources:
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)
    return Response({'message': 'No resources found'}, status=404)

@api_view(['GET'])
def api_resource_search(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    q = request.data.get('q')
    resources = Resource.objects.filter(
        Q(name__icontains=q) | 
        Q(resource_id__icontains=q) |
        Q(resource_type__icontains=q)
    )
    if resources:
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)
    return Response({'message': 'No resources found'}, status=404)

@api_view(['GET'])
def api_resource_detail(request, resource_id):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    resource = get_object_or_404(Resource, resource_id=resource_id)
    serializer = ResourceSerializer(resource)
    return Response(serializer.data)

@api_view(['POST'])
def api_resource_create(request):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    form = ResourceForm(request.data)
    if form.is_valid():
        resource = form.save(commit=False)
        if resource.resource_type == 'ELECTRICAL':
            resource.resource_id = 'ELE-' + str(Resource.objects.filter(resource_type='ELECTRICAL').count() + 1)
        elif resource.resource_type == 'PLUMBING':
            resource.resource_id = 'PLU-' + str(Resource.objects.filter(resource_type='PLUMBING').count() + 1)
        elif resource.resource_type == 'CARPENTRY':
            resource.resource_id = 'CAR-' + str(Resource.objects.filter(resource_type='CARPENTRY').count() + 1)
        elif resource.resource_type == 'SANITATION':
            resource.resource_id = 'SAN-' + str(Resource.objects.filter(resource_type='SANITATION').count() + 1)
        else:
            resource.resource_id = 'OTH-' + str(Resource.objects.filter(resource_type='OTHERS').count() + 1)

        resource.total_count = resource.correct_count + resource.damaged_count
        resource.save()
        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=201)
    return Response(form.errors, status=400)

@api_view(['PUT'])
def api_resource_update(request, resource_id):   
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    resource = get_object_or_404(Resource, resource_id=resource_id)
    form = ResourceUpdateForm(request.data, instance=resource)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.total_count = resource.correct_count + resource.damaged_count
        resource.save()
        resource_serializer = ResourceSerializer(resource)
        return Response(resource_serializer.data, status=201)
    return Response(form.errors, status=400)

@api_view(['DELETE'])
def api_resource_delete(request, resource_id):
    if not admin_required(request):
        return Response({'message': 'Unauthorized'}, status=401)
    resource = Resource.objects.get(resource_id=resource_id)
    resource.delete()
    return Response(status=204)

