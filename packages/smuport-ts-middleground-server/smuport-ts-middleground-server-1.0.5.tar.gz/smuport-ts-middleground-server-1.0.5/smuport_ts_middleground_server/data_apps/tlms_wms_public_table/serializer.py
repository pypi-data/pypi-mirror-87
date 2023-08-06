from .import models
from rest_framework import serializers


class CargoSerializer(serializers.ModelSerializer):
    image_path = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    # cargo_type = CargoTypeSerializer(read_only=True)
    # cargo_type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Cargo
        fields = "__all__"


class ConsignorSerializer(serializers.ModelSerializer):
    """
    委托公司序列化
    """
    class Meta:
        model = models.Consignor
        fields = "__all__"


class DecMethodSerializer(serializers.ModelSerializer):
    """
    申报方式
    """
    class Meta:
        model = models.DecMethod
        fields = "__all__"


class WorkRouteSerializer(serializers.ModelSerializer):
    """
    作业路线
    """
    class Meta:
        model = models.WorkRoute
        fields = "__all__"


class CtnSizeSerializer(serializers.ModelSerializer):
    """
    箱尺寸
    """
    class Meta:
        model = models.CtnSize
        fields = "__all__"


class CtnTypeSerializer(serializers.ModelSerializer):
    """
    箱类型
    """
    class Meta:
        model = models.CtnType
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    """
    供应商
    """
    class Meta:
        model = models.Supplier
        fields = "__all__"


class UnPackTypeSerializer(serializers.ModelSerializer):
    """
    装卸方式
    """
    class Meta:
        model = models.UnPackType
        fields = "__all__"


class ForkliftSerializer(serializers.ModelSerializer):
    """
    叉车车辆
    """
    class Meta:
        model = models.Forklift
        fields = "__all__"

