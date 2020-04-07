from typing import List
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedRelatedField
from csv_to_genie2.models import File, Standard


class StandardSerializer(serializers.HyperlinkedModelSerializer):
    file_set: HyperlinkedRelatedField = serializers.HyperlinkedRelatedField(
        view_name='genie2:file-detail', many=True, read_only=True
    )

    class Meta:
        model: type = Standard
        fields: List[str] = [
            'numdos',
            'refdoc',
            'datoff',
            'ancart',
            'file_set',
        ]


class FileSerializer(serializers.HyperlinkedModelSerializer):
    standard: HyperlinkedRelatedField = serializers.HyperlinkedRelatedField(
        view_name='genie2:standard-detail', read_only=True
    )

    class Meta:
        model: type = File
        fields: List[str] = [
            'numdos',
            'numdosvl',
            'format',
            'verling',
            'standard',
        ]
