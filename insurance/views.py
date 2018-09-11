from django import shortcuts
from django.contrib.auth import models as auth_models
from insurance import models
from rest_framework import response
from rest_framework.decorators import api_view
import rest_framework

def home_page(request):
    
    users = auth_models.User.objects.all()
    
    if users.count() < 2:
        provide_sample_data()
        users = auth_models.User.objects.all()
    
    return shortcuts.render(request, 'home_page.html', { 'users': users })

@api_view(['GET'])
def get_risk_type(request, pk):
    try:
        risk_type = models.RiskType.objects.get(pk=pk)
    except models.RiskType.DoesNotExist:
        return Response(status=rest_framework.status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = models.RiskTypeSerializer(risk_type)
        return response.Response(serializer.data)
    
@api_view(['GET'])
def get_risk_types(request):
    risk_types = models.RiskType.objects.all()
    
    if request.method == 'GET':
        serializer = models.RiskTypeSerializer(risk_types, many=True)
        return response.Response(serializer.data)
    
def provide_sample_data():
    user = auth_models.User(username='Vu Nguyen')
    user.save()
    prize_risk_type = models.RiskType(name='prize')
    prize_risk_type.save()
    custom_prize_amount_field = models.CustomField(name='Prize Amount', 
                                                   risk_type=prize_risk_type, 
                                                   format='Currency')
    custom_prize_amount_field.save()
    custom_establishment_name_field = models.CustomField(name='Establishment Name', 
                                                         risk_type=prize_risk_type, 
                                                         format='String')
    custom_establishment_name_field.save()
    account = models.Account(user=user, risk_type=prize_risk_type)
    account.save()
    custom_prize_amount_value = models.CustomValue(custom_field=custom_prize_amount_field, 
                                                    value='1000000.00',
                                                    account=account)
    custom_prize_amount_value.save()
    custom_establishment_name_value = models.CustomValue(custom_field=custom_establishment_name_field, 
                                                         value='New Orleans Casino "Grand Prize"', 
                                                         account=account)
    custom_establishment_name_value.save()
    user = auth_models.User(username='Moe Joe')
    user.save()
    house_risk_type = models.RiskType(name='house')
    house_risk_type.save()
    custom_address_field = models.CustomField(name='Address',
                                              risk_type=house_risk_type,
                                              format='Address')
    custom_address_field.save()
    custom_phone_number_field = models.CustomField(name='Phone Number',
                                                   risk_type=house_risk_type,
                                                   format='PhoneNumber')
    custom_phone_number_field.save()
    custom_house_type_field = models.CustomField(name='House Type',
                                                 risk_type=house_risk_type,
                                                 format='Enum',
                                                 values='House\n' +
                                                        'Duplex\n' +
                                                        'Apartment\n' +
                                                        'Condominium'
                                                 )
    account = models.Account(user=user, risk_type=house_risk_type)
    account.save()
    custom_address_value = models.CustomValue(custom_field=custom_address_field, 
                                                value='211 Pine Street',
                                                account=account)
    custom_address_value.save()
    custom_phone_number_value = models.CustomValue(custom_field=custom_phone_number_field, 
                                                    value='867 5309', 
                                                    account=account)
    custom_phone_number_value.save()
    custom_house_type_value = models.CustomValue(custom_field=custom_house_type_field,
                                                    value='Apartment',
                                                    account=account)

    