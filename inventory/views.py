from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from .models import Inventory
from django.views.decorators.csrf import csrf_exempt
import json
from . import helper
import csv
import datetime as dt


with open('./locations.json') as f:
    location_data = json.load(f)
    location_list = [x for x in location_data]

@csrf_exempt
def read_create_inventory(request):
    if request.method == 'POST':
        create_inventory(request)
        return JsonResponse({'message': 'inventory item successfully created'}, status=201)
    elif request.method == 'GET':
        data = list_inventory()
        return render(request, "inventory/index.html", {"data": data})
    else:
        return JsonResponse({'error': 'method not found'}, status=405)

def create_inventory(request):
    body = json.loads(request.body.decode('utf-8'))
    name = body['name']
    quantity = body['quantity']
    located_at = body['location']
    new_inventory = Inventory(name=name, quantity=quantity, located_at=located_at)
    new_inventory.save()

def list_inventory():
    data = []
    items = Inventory.objects.all()
    for item in items:
        loc = location_data[item.located_at]
        data.append({
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'location': item.located_at,
            'weather': helper.get_weather_data(loc['lat'], loc['long'])
        })
    
    return data

@csrf_exempt
def modify_inventory(request, id):
    if not inventory_exists(id):
        return JsonResponse({'error': 'inventory item does not exist'}, status=404)
    print("HERE", request.method)
    if request.method == 'PUT':
        body = json.loads(request.body.decode('utf-8'))
        name = body['name']
        quantity = body['quantity']
        located_at = body['location']
        inventory_item = Inventory.objects.get(pk=id)
        
        inventory_item.name = name
        inventory_item.quantity = quantity
        inventory_item.located_at = located_at
        inventory_item.edited_at = dt.datetime.now()
        inventory_item.save()
        return JsonResponse({'message': 'inventory item successfully modified'}, status=200)
    elif request.method == 'DELETE':
        delete_inventory(id)
        return JsonResponse({'message': 'inventory item successfully deleted'}, status=200)
    else:
        return JsonResponse({'error': 'method not supported'}, status=405)

def inventory_exists(id):
    try:
        Inventory.objects.get(pk=id)
        return True
    except Inventory.DoesNotExist:
        print("does not exist")
        return False
    

def delete_inventory(id):
    Inventory.objects.filter(pk=id).delete()

def edit_inventory(request, id):
    if request.method == 'GET':
        if not inventory_exists(id):
            return JsonResponse({'error': 'inventory item does not exist'}, status=404)
        
        inventory = Inventory.objects.get(pk=id)
        data = {
            'inventory': {
                'id': id,
                'name': inventory.name,
                'quantity': inventory.quantity,
                'location': inventory.located_at
            },
            'locations': location_list
        }
        return render(request, "inventory/edit.html", {"data": data})
    else:
        return HttpResponseNotFound()

def add_inventory(request):
    data = {
            'locations': location_list
        }
    return render(request, "inventory/add.html", {"data": data})

def export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'quantity', 'added_at', 'edited_at', 'located_at'])

    users = Inventory.objects.all().values_list('name', 'quantity', 'added_at', 'edited_at', 'located_at')
    for user in users:
        writer.writerow(user)

    return response

def not_found():
    return HttpResponseNotFound()