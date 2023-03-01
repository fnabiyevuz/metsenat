from rest_framework import serializers
from .models import *


class SponsorsSerializer(serializers.ModelSerializer):
    donated = serializers.ReadOnlyField(source='donation')

    class Meta:
        model = Sponsors
        fields = ['id', 'fish', 'phone', 'summa', 'donated', 'created_at', 'status']


class SponsorsMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsors
        fields = ['id', 'fish']


class OTMsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTMs
        fields = '__all__'


class StudentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'


class StudentsReadSerializer(serializers.ModelSerializer):
    donated = serializers.ReadOnlyField(source='donation')
    otm = OTMsSerializer(read_only=True)

    class Meta:
        model = Students
        fields = ['id', 'fish', 'type', 'otm', 'contract', 'donated', 'phone']


class DonationsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = '__all__'


class DonationsReadSerializer(serializers.ModelSerializer):
    sponsor = SponsorsMiniSerializer(read_only=True)

    class Meta:
        model = Donations
        fields = '__all__'
