from rest_framework import serializers
from django.contrib.auth.models import Permission, Group

class PermissionSerializer(serializers.ModelSerializer):
    has_perm = serializers.SerializerMethodField("get_has_perm")
    from_group = serializers.SerializerMethodField("get_from_group")

    class Meta:
        model = Permission
        fields = (
            "pk",
            "name",
            "codename",
            "content_type",
            "has_perm",
            "from_group"
        )
        depth = 2

    def get_from_group(self, obj):
        groups = self.context.get(
            "groups",
            Group.objects.none()
        )
        return groups.filter(permissions__pk=obj.pk).exists()


    def get_has_perm(self, obj):
        user = self.context.get("user", None)
        if user:
            return user.has_perm(
                "{}.{}".format(obj.content_type.app_label, obj.codename)
            )
        else:
            return False