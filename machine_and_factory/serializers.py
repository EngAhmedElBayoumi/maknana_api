# filepath: d:\windows_backup-13-01-2025\Abd_elrahman\maknana_api\machine_and_factory\serializers.py
from rest_framework import serializers
from .models import factory, machine, malfunction_request, malfunction_report, malfunction_invoice, automation_request , malfunction_type
from .models import market_category, market_product, market_order_request , Contarct , shipping_detials

class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = factory
        fields = '__all__'
        
    
class MalfunctionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = malfunction_type
        fields = '__all__'



class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = machine
        fields = '__all__'


    # to represntation diplay all factory distals for this machine
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['factory'] = FactorySerializer(instance.factory).data
        return representation

class MalfunctionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = malfunction_request
        fields = '__all__'

class MalfunctionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = malfunction_report
        fields = '__all__'

class MalfunctionInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = malfunction_invoice
        fields = '__all__'

class AutomationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = automation_request
        fields = '__all__'

class MarketCategorySerializer(serializers.ModelSerializer):
    machine_count = serializers.SerializerMethodField()
    used_machine_count = serializers.SerializerMethodField()
    new_machine_count = serializers.SerializerMethodField()

    class Meta:
        model = market_category
        fields = '__all__'

    # total machine count for each category
    def get_machine_count(self, obj):
        return obj.market_product_set.count()

    # total used machine count for each category
    def get_used_machine_count(self, obj):
        return obj.market_product_set.filter(type="used").count()

    # total new machine count for each category
    def get_new_machine_count(self, obj):
        return obj.market_product_set.filter(type="new").count()



class MarketProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = market_product
        fields = '__all__'

class MarketOrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = market_order_request
        fields = '__all__'
        
        
    # represnet all market orders in the request not just the id
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = MarketProductSerializer(instance.product).data
        return representation


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contarct
        fields = ['id', 'client', 'code', 'type', 'end_date', 'status', 'duration', 
                 'start_from', 'machine_number', 'factory', 'signature', 'description', 
                 'file', 'create_at', 'update_at']
        read_only_fields = ['create_at', 'update_at']


class ShippingDetialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = shipping_detials
        fields = '__all__'

         