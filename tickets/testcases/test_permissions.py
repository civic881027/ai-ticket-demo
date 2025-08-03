# tickets/tests/test_views.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from tickets.models import Ticket

@pytest.mark.django_db
def test_ticket_detail_update_permission():
    # 建立使用者：擁有者user1、非擁有者user2、管理員admin
    user1 = User.objects.create_user(username="user1", password="pass")
    user2 = User.objects.create_user(username="user2", password="pass")
    admin = User.objects.create_user(username="admin", password="pass", is_staff=True)

    # 建立 user1 所擁有的工單
    ticket = Ticket.objects.create(
        title="Test Ticket",
        description="Test Description",
        category="test",
        created_by=user1,
        priority="low",
        status="open"
    )

    url = f"/api/tickets/{ticket.id}/"

    # 建立 APIClient 實例
    client = APIClient()

    # 1. user1(擁有者) 嘗試更新，應成功
    client.force_authenticate(user=user1)
    response = client.patch(url, {"priority": "high"}, format="json")
    assert response.status_code == 200
    assert response.data["priority"] == "high"

    # 2. admin(管理員) 嘗試更新，應成功
    client.force_authenticate(user=admin)
    response = client.patch(url, {"status": "resolved"}, format="json")
    assert response.status_code == 200
    assert response.data["status"] == "resolved"

    # 3. user2(非擁有者、非管理員) 嘗試更新，應拒絕（403）
    client.force_authenticate(user=user2)
    response = client.patch(url, {"priority": "medium"}, format="json")
    assert response.status_code == 403

    # 4. 登出狀態嘗試更新，應拒絕（401 非認證）
    client.force_authenticate(user=None)
    response = client.patch(url, {"priority": "urgent"}, format="json")
    assert response.status_code == 401
