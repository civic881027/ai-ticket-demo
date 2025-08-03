# tickets/testcases/test_serializers.py
import pytest
from django.contrib.auth.models import User
from tickets.serializers import TicketSerializer
pytestmark = pytest.mark.django_db

def test_ticket_serializer_valid_assigned_user():
    user = User.objects.create(username="t1")
    data = {
        "title": "測試標題",
        "description": "測試內容",
        "priority": "high",
        "status": "open",
        "category": "技術問題",
        "assigned_to": user.id
    }
    ser = TicketSerializer(data=data, context={"request": None})
    assert ser.is_valid(), ser.errors

def test_ticket_serializer_invalid_assigned_user():
    data = {
        "title": "無效負責人",
        "description": "內容",
        "priority": "low",
        "status": "open",
        "category": "一般諮詢",
        "assigned_to": 99999  # 不存在的使用者
    }
    ser = TicketSerializer(data=data)
    assert not ser.is_valid()
    assert "assigned_to" in ser.errors

def test_ticket_serializer_priority_choices():
    data = {
        "title": "優先級錯誤",
        "description": "內容",
        "priority": "wrong",
        "status": "open",
        "category": "一般諮詢"
    }
    ser = TicketSerializer(data=data)
    assert not ser.is_valid()
    assert "priority" in ser.errors

def test_ticket_serializer_status_choices():
    data = {
        "title": "狀態錯誤",
        "description": "內容",
        "priority": "low",
        "status": "wrong_status",
        "category": "一般諮詢"
    }
    ser = TicketSerializer(data=data)
    assert not ser.is_valid()
    assert "status" in ser.errors
