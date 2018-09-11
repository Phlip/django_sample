from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import html
import re
from rest_framework import serializers

class RiskType(models.Model):
    name = models.CharField(max_length=42)

class Account(models.Model):
    user = models.ForeignKey(auth_models.User, 
                             on_delete=models.CASCADE, 
                             related_name='accounts')
    risk_type = models.ForeignKey(RiskType, 
                                  on_delete=models.CASCADE, 
                                  related_name='accounts')

class CustomField(models.Model):
    name = models.CharField(max_length=42)
    risk_type = models.ForeignKey(RiskType, 
                                  on_delete=models.CASCADE, 
                                  related_name='custom_fields')
    format = models.CharField(max_length=10)
    values = models.TextField()

    def get_flyweight(self):
        klass = globals()['Custom' + self.format + 'Field']
        return klass()
    
    def validate(self, value):
        return self.get_flyweight().validate(self, value)
    
class CustomFieldSerializer(serializers.ModelSerializer):   #  Note:  A real project would put serializers in their own file.

    class Meta:
        model = CustomField
        fields = ('pk', 'name', 'format', 'values')
    
class RiskTypeSerializer(serializers.ModelSerializer):
    custom_fields = CustomFieldSerializer(many=True)
    
    class Meta:
        model = RiskType
        fields = ('pk', 'name', 'custom_fields')

class CustomValue(models.Model):
    account = models.ForeignKey(Account, 
                                on_delete=models.CASCADE, 
                                related_name='custom_values')
    custom_field = models.ForeignKey(CustomField, 
                                     on_delete=models.CASCADE, 
                                     related_name='custom_values')
    value = models.CharField(max_length=0xFFFF)

    def get_custom_field_flyweight(self):
        return self.custom_field.get_flyweight()
        
    def edit(self):
        return self.get_custom_field_flyweight().edit(self)
        
    def display(self):
        return self.get_custom_field_flyweight().display(self)

class CustomAddressField:
    
    def edit(self, state):
        return '<textarea>%s</textarea>' % html.escape(state.value)
    
    def validate(self, field, value):
        return re.compile(r'\A..+.\Z', re.DOTALL).match(value) != None
        
    def display(self, state):
        return '<address>%s</address>' % html.escape(state.value)
    
class CustomCurrencyField:
    
    def edit(self, state):
        return '<input value="%s" type="number" min="0" step="0.01">' % state.value
    
    def validate(self, field, value):
        return re.compile(r'\A\d[\d\.]*\Z').match(value) != None
        
    def display(self, state):
        return state.value
    
class CustomEnumField:
    
    def edit(self, state):
        select = '<select>'
        values = state.custom_field.values.split('\n')
        for value in values:
            selected = 'selected' if value == state.value else ''
            select += '<option %s>%s</option>' % (selected, value)
        select += '</select>'
        return select
    
    def validate(self, field, value):
        values = field.values.split('\n')
        return value in values    
    
    def display(self, state):
        return state.value
    
class CustomPhoneNumberField:
    
    def edit(self, state):
        return '<input type="tel" value="%s">' % state.value

    def validate(self, field, value):
        return re.compile(r'\A[\d\-\(\)]+\Z').match(value) != None
    
    def display(self, state):
        return '<a href="tel:+%s">%s</a>' % (state.value, state.value)

class CustomStringField:
    def edit(self, state):
        return '<input value="%s" type="text">' % html.escape(state.value)
    
    def validate(self, field, value):
        return re.compile(r'\A\w[\w\s]+\w\Z').match(value) != None
        
    def display(self, state):
        return html.escape(state.value)

    
    