from .models import Campaign
from rest_framework import serializers



class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add any additional fields or transformations here if needed
        return representation