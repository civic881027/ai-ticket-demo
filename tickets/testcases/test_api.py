# tickets/testcases/test_api.py
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from tickets.models import Ticket
import pytest
pytestmark = pytest.mark.django_db

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="apiu", password="pw")

def test_api_create_ticket(client, user):
    client.force_authenticate(user)
    data = {
        "title": "API工單",
        "description": "API新增測試",
        "priority": "medium",
        "status": "open",
        "category": "產品諮詢"
    }
    r = client.post("/api/tickets/", data, format="json")
    assert r.status_code in [201, 200]
    assert r.data["title"] == data["title"]

def test_api_patch_ticket_assigned_to(client, user):
    client.force_authenticate(user)
    # 先建立一個工單
    resp = client.post("/api/tickets/", {
        "title": "工單PATCH",
        "description": "desc",
        "priority": "medium",
        "status": "open",
        "category": "技術問題"
    }, format="json")
    #print("DEBUG POST Response:", resp.data)
    tid = resp.data["id"]
    # 指派不存在的 user id
    r2 = client.patch(f'/api/tickets/{tid}/', {"assigned_to": 99988}, format="json")
    assert r2.status_code == 400
    assert "assigned_to" in r2.data


def test_manual_reply_api():
    # 建立兩個使用者，一個建立工單，一個作為回覆客服
    user = User.objects.create_user(username="creator", password="pw")
    staff = User.objects.create_user(username="staff", password="pw", is_staff=True)
    api = APIClient()

    # 建立一個工單
    ticket = Ticket.objects.create(
        title="要被回覆的工單",
        description="test",
        category="帳戶問題",
        priority="medium",
        status="open",
        created_by=user
    )

    # 用 staff 進行人工回覆
    api.force_authenticate(user=staff)
    url = f"/api/tickets/{ticket.id}/reply/"
    data = {"response_text": "您好～這是人工回覆！"}
    resp = api.post(url, data, format="json")
    assert resp.status_code == 201
    assert resp.data["response_text"] == "您好～這是人工回覆！"
    assert resp.data["is_ai_generated"] is False
    assert resp.data["created_by"]["id"] == staff.id

    # 檢查工單的 response 數量=1
    ticket.refresh_from_db()
    assert ticket.responses.count() == 1

def test_ai_reply_api(monkeypatch):
    user = User.objects.create_user(username="creator", password="pw")
    api = APIClient()

    # 建立工單
    ticket = Ticket.objects.create(
        title="AI 回覆測試工單",
        description="請幫我AI回覆",
        category="技術問題",
        priority="medium",
        status="open",
        created_by=user
    )

    # 為避免真的呼叫 Ollama，可 monkeypatch AI 回覆
    def fake_generate_response(self, ticket):
        return "AI測試自動產生內容"
    from tickets.services import OllamaService
    monkeypatch.setattr(OllamaService, "generate_response", fake_generate_response)

    # 用 user 產生 AI 回覆
    api.force_authenticate(user=user)
    url = f"/api/tickets/{ticket.id}/ai-response/"
    resp = api.post(url, {}, format="json")
    assert resp.status_code == 201
    assert resp.data["response_text"] == "AI測試自動產生內容"
    assert resp.data["is_ai_generated"] is True
    assert resp.data["created_by"]["id"] == user.id

    # 檢查工單的 response 數量=1
    ticket.refresh_from_db()
    assert ticket.responses.count() == 1

def test_list_tickets_limited_to_user(client, user):
    client.force_authenticate(user=user)
    # 建立不屬於 user 的工單
    other_user = User.objects.create(username="other")
    Ticket.objects.create(title="其他人的工單", description="...", created_by=other_user)
    # 建立 user 自己的工單
    Ticket.objects.create(title="我的工單", description="...", created_by=user)

    response = client.get("/api/tickets/")
    assert response.status_code == 200
    # 回傳資料應該只包含 user 自己的工單
    for ticket in response.data['results']:
        assert ticket["created_by"]["id"] == user.id
