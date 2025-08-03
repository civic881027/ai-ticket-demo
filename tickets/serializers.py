from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket, TicketResponse

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class TicketResponseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = TicketResponse
        fields = ['id', 'response_text', 'is_ai_generated', 'created_by', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False
    )

    responses = TicketResponseSerializer(many=True, read_only=True)
    category = serializers.CharField(read_only=False) 
    priority = serializers.CharField(read_only=False)
    status = serializers.CharField(read_only=False)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'priority', 'status', 'category',
            'created_by', 'assigned_to', 'created_at', 'updated_at',
            'ai_suggested_priority', 'ai_suggested_category', 'responses'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at',
            'ai_suggested_priority', 'ai_suggested_category', 'responses'
        ]
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


    def validate_priority(self, value):
        """
        驗證 priority 欄位是否在允許清單內
        """
        allowed_priorities = {'low', 'medium', 'high', 'urgent'}
        if value.lower() not in allowed_priorities:
            raise serializers.ValidationError(f"優先級必須是以下之一：{', '.join(allowed_priorities)}")
        return value.lower()

    def validate_status(self, value):
        """
        驗證 status 欄位是否在允許清單內
        """
        allowed_statuses = {'open', 'in_progress', 'resolved', 'closed'}
        if value.lower() not in allowed_statuses:
            raise serializers.ValidationError(f"狀態必須是以下之一：{', '.join(allowed_statuses)}")
        return value.lower()


class TicketCreateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Ticket
        fields = [
            'title', 'description', 'category',
            'priority', 'status', 'assigned_to'
        ]
        extra_kwargs = {
            'category': {'required': False, 'allow_blank': True},
            'priority': {'required': False, 'allow_blank': True},
            'status': {'required': False, 'allow_blank': True},
        }


        

