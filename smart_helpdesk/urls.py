from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)
from tickets import views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Tickets API
    path('api/tickets/', views.TicketListCreateView.as_view(), name='ticket-list-create'),
    path('api/tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),

    # 人工回復API
    path('api/tickets/<int:ticket_id>/reply/', views.TicketResponseCreateView.as_view(), name='ticket-manual-reply'),
    # AI 回覆產生 API
    path('api/tickets/<int:ticket_id>/ai-response/', views.generate_ai_response, name='ticket-ai-response'),
    
    # JWT Auth routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 取得 Token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 更新 Token
]
