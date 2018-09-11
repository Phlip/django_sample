from django.test import TestCase
from insurance import models
from django.contrib.auth import models as auth_models
from django import test
from django import urls
import rest_framework

  #  Note:  Generate the ERM diagram by installing django_extensions, then running:
  #           python3 manage.py graph_models insurance > insurance.dot
  #           dot -Tpng insurance.dot -o insurance.png

client = test.Client()

class InsuranceTestCase(TestCase):
    
    #  Note:  Automated test suites for a real project would include many more short tests, with more assertions.
    
    def test_insure_the_grand_prize(self):
        user = auth_models.User(username='Vu Nguyen')
        user.save()
        prize_risk_type = models.RiskType(name='prize')
        prize_risk_type.save()
        custom_prize_amount_field = models.CustomField(name='Prize Amount', 
                                                       risk_type=prize_risk_type, 
                                                       format='Currency')
        custom_prize_amount_field.save()
        self.assertTrue(custom_prize_amount_field.validate('1'))
        self.assertTrue(custom_prize_amount_field.validate('10.00'))
        self.assertFalse(custom_prize_amount_field.validate('not a number'))
        custom_establishment_name_field = models.CustomField(name='Establishment Name', 
                                                             risk_type=prize_risk_type, 
                                                             format='String')
        custom_establishment_name_field.save()
        self.assertTrue(custom_establishment_name_field.validate('Moulin Rouge'))
        self.assertFalse(custom_establishment_name_field.validate(''))
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
        
        #  Note:  The <input> fields all need name attributes.
        
        self.assertEqual('<input value="1000000.00" type="number" min="0" step="0.01">', custom_prize_amount_value.edit())
        self.assertEqual('1000000.00', custom_prize_amount_value.display())
        self.assertEqual('<input value="New Orleans Casino &quot;Grand Prize&quot;" type="text">', custom_establishment_name_value.edit())
        self.assertEqual('New Orleans Casino &quot;Grand Prize&quot;', custom_establishment_name_value.display())
        
    def test_insure_a_house(self):
        user = auth_models.User(username='Moe Joe')
        user.save()
        house_risk_type = models.RiskType(name='house')
        house_risk_type.save()
        custom_address_field = models.CustomField(name='Address',
                                                  risk_type=house_risk_type,
                                                  format='Address')
        custom_address_field.save()
        self.assertTrue(custom_address_field.validate('1164 Morning Glory Circle'))
        self.assertTrue(custom_address_field.validate('1164 Morning Glory Circle\nBurbank, CA'))
        self.assertFalse(custom_address_field.validate(''))
        custom_phone_number_field = models.CustomField(name='Phone Number',
                                                       risk_type=house_risk_type,
                                                       format='PhoneNumber')
        custom_phone_number_field.save()
        self.assertTrue(custom_phone_number_field.validate('800-555-1212'))
        self.assertFalse(custom_phone_number_field.validate('Goal Delux'))
        custom_house_type_field = models.CustomField(name='House Type',
                                                     risk_type=house_risk_type,
                                                     format='Enum',
                                                     values='House\n' +  #  Note:  This could have been a child model.
                                                            'Duplex\n' +
                                                            'Apartment\n' +
                                                            'Condominium'
                                                     )
        self.assertTrue(custom_house_type_field.validate('Condominium'))
        self.assertFalse(custom_house_type_field.validate('Garage'))        
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
        self.assertEqual('<textarea>211 Pine Street</textarea>', custom_address_value.edit())
        self.assertEqual('<address>211 Pine Street</address>', custom_address_value.display())
        self.assertEqual('<input type="tel" value="867 5309">', custom_phone_number_value.edit())
        self.assertEqual('<a href="tel:+867 5309">867 5309</a>', custom_phone_number_value.display())
        edit_enum = custom_house_type_value.edit()
        self.assertIn('<select>', edit_enum)
        self.assertIn('<option >House</option>', edit_enum)
        self.assertIn('<option selected>Apartment</option>', edit_enum)
        self.assertEqual('Apartment', custom_house_type_value.display())
        self.assertEqual(1, user.accounts.count())
        self.assertEqual(2, account.custom_values.count())
        
    def test_RiskTypeSerializer(self):
        self.test_insure_the_grand_prize()  #  A test suite for a real project would use fixtures.
        prize_risk_type = models.RiskType.objects.get(name='prize')
        
        serializer = models.RiskTypeSerializer(prize_risk_type)
        
        self.assertEqual(prize_risk_type.pk, serializer.data['pk'])
        self.assertEqual('prize', serializer.data['name'])
        cf = serializer.data['custom_fields'][0]
        self.assertEqual('Prize Amount', cf['name'])
        self.assertEqual('Currency', cf['format'])
        cf = serializer.data['custom_fields'][1]
        self.assertEqual('Establishment Name', cf['name'])
        self.assertEqual('String', cf['format'])
        
    def test_get_risk_type(self):
        self.test_insure_the_grand_prize()
        prize_risk_type = models.RiskType.objects.get(name='prize')
        url = urls.reverse('get_risk_type', kwargs={ 'pk': prize_risk_type.pk })
        response = client.get(url)
        serializer = models.RiskTypeSerializer(prize_risk_type)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual('prize', response.data['name'])
        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)
                
    def test_get_risk_types(self):
        self.test_insure_the_grand_prize()
        self.test_insure_a_house()
        prize_risk_type = models.RiskType.objects.get(name='prize')
        house_risk_type = models.RiskType.objects.get(name='house')
        url = urls.reverse('get_risk_types')
        response = client.get(url)
        serializer = models.RiskTypeSerializer(prize_risk_type)
        self.assertEqual(serializer.data, response.data[0])
        self.assertEqual('prize', response.data[0]['name'])
        serializer = models.RiskTypeSerializer(house_risk_type)
        self.assertEqual(serializer.data, response.data[1])
        self.assertEqual('house', response.data[1]['name'])
        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)
                
                                 
        