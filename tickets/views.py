from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Ticket, TicketResponse
from .serializers import TicketSerializer, TicketCreateSerializer, TicketResponseSerializer, UserSerializer
from .services import OllamaService
from .permissions import IsOwnerOrAdmin

# API Views
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class TicketListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(
            Q(assigned_to=self.request.user) | Q(created_by=self.request.user)
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCreateSerializer  
        return TicketSerializer  # 一般列表用完整序列化器

    def perform_create(self, serializer):
        ollama_service = OllamaService()
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']

        # 前端可能帶入欄位
        category_input = serializer.validated_data.get('category', None)
        priority_input = serializer.validated_data.get('priority', None)
        status = serializer.validated_data.get('status', 'open')
        assigned_to = serializer.validated_data.get('assigned_to', None)

        # 嘗試從 Ollama 得到 AI 建議（這步可以包成條件，例如只在缺欄位才呼叫）
        ai_analysis = {}
        if not category_input or not priority_input:
            ai_analysis = ollama_service.categorize_ticket(title, description)
        else:
            ai_analysis = {}

        # 確認最終存入的 category 與 priority
        final_category = category_input or ai_analysis.get('category', '一般諮詢')
        final_priority = priority_input or ai_analysis.get('priority', 'medium')

        # AI 建議肯定存，但前端輸入不覆蓋 AI 建議欄位
        ai_suggested_category = ai_analysis.get('category')
        ai_suggested_priority = ai_analysis.get('priority')

        serializer.save(
            created_by=self.request.user,
            category=final_category,
            priority=final_priority,
            status=status,
            assigned_to=assigned_to,
            ai_suggested_category=ai_suggested_category,
            ai_suggested_priority=ai_suggested_priority,
        )

    def create(self, request, *args, **kwargs):
        """
        覆寫 create 以保證回傳序列化的完整物件，包含 id 等欄位
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 重新用完整的 TicketSerializer 序列化剛存的物件
        ticket = serializer.instance
        full_serializer = TicketSerializer(ticket, context={'request': request})
        headers = self.get_success_headers(full_serializer.data)
        return Response(full_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Ticket.objects.all()

class TicketResponseCreateView(generics.CreateAPIView):
    serializer_class = TicketResponseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        response_text = request.data.get('response_text')
        if not response_text or not response_text.strip():
            return Response({"response_text": ["回覆內容不得為空。"]}, status=status.HTTP_400_BAD_REQUEST)

        response_obj = TicketResponse.objects.create(
            ticket=ticket,
            response_text=response_text.strip(),
            is_ai_generated=False,
            created_by=request.user
        )
        serializer = TicketResponseSerializer(response_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_ai_response(request, ticket_id):
    """
    為特定工單生成AI回覆建議
    """
    try:
        if request.user.is_staff:
            ticket = get_object_or_404(Ticket, id=ticket_id)
        else:
            
            ticket = get_object_or_404(Ticket, id=ticket_id, assigned_to=request.user)
            
        
        ollama_service = OllamaService()
        ai_response = ollama_service.generate_response(ticket)
       
        if not ai_response or "抱歉，AI助手暫時無法提供回覆建議，請稍後再試。" in ai_response:
            
            # 偵測到 AI 回覆為不可用/服務異常
            return Response(
                {"detail": "AI助手暫時無法提供回覆建議，請稍後再試。"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # 創建AI回覆記錄
        response_obj = TicketResponse.objects.create(
            ticket=ticket,
            response_text=ai_response,
            is_ai_generated=True,
            created_by=request.user
        )
        
        serializer = TicketResponseSerializer(response_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'生成AI回覆失敗: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

#Web Views (Traditional Django Views)
# @login_required
# def ticket_list(request):
#     """工單列表頁面"""
#     if request.user.is_staff:
#         tickets = Ticket.objects.all()
#     else:
#         tickets = Ticket.objects.filter(created_by=request.user)
    
#     return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

# @login_required
# def ticket_create(request):
#     """建立工單頁面"""
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
        
#         if title and description:
#             # 使用AI自動分類
#             ollama_service = OllamaService()
#             ai_analysis = ollama_service.categorize_ticket(title, description)
            
#             ticket = Ticket.objects.create(
#                 title=title,
#                 description=description,
#                 created_by=request.user,
#                 category=ai_analysis.get('category', '一般諮詢'),
#                 ai_suggested_priority=ai_analysis.get('priority', 'medium'),
#                 ai_suggested_category=ai_analysis.get('category', '一般諮詢')
#             )
            
#             messages.success(request, f'工單已成功建立！AI建議分類：{ticket.category}')
#             return redirect('ticket_detail', ticket_id=ticket.id)
#         else:
#             messages.error(request, '請填寫完整的工單資訊')
    
#     return render(request, 'tickets/ticket_create.html')

# @login_required
# def ticket_detail(request, ticket_id):
#     """工單詳情頁面"""
#     if request.user.is_staff:
#         ticket = get_object_or_404(Ticket, id=ticket_id)
#     else:
#         ticket = get_object_or_404(Ticket, id=ticket_id, created_by=request.user)
    
#     return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})
