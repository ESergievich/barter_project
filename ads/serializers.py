from rest_framework import serializers

from .models import Ad, ExchangeProposal


class AdReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        exclude = ['search_vector']


class AdWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']


class ProposalReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = "__all__"


class ExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ['status', 'created_at']
