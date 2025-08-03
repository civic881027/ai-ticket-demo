from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '緊急'),
    ]
    
    STATUS_CHOICES = [
        ('open', '開啟'),
        ('in_progress', '處理中'),
        ('resolved', '已解決'),
        ('closed', '已關閉'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='標題')
    description = models.TextField(verbose_name='描述')
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        verbose_name='優先級'
    )
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='open',
        verbose_name='狀態'
    )
    category = models.CharField(max_length=100, verbose_name='分類')
    
    # 用戶關聯
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_tickets',
        verbose_name='建立者'
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tickets',
        verbose_name='負責人'
    )
    
    # 時間戳記
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    
    # AI相關欄位
    ai_suggested_priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        null=True, 
        blank=True,
        verbose_name='AI建議優先級'
    )
    ai_suggested_category = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name='AI建議分類'
    )
    
    class Meta:
        verbose_name = '工單'
        verbose_name_plural = '工單'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.id} - {self.title}"

class TicketResponse(models.Model):
    ticket = models.ForeignKey(
        Ticket, 
        on_delete=models.CASCADE, 
        related_name='responses',
        verbose_name='工單'
    )
    response_text = models.TextField(verbose_name='回覆內容')
    is_ai_generated = models.BooleanField(default=False, verbose_name='AI生成')
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='回覆者'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='回覆時間')
    
    class Meta:
        verbose_name = '工單回覆'
        verbose_name_plural = '工單回覆'
        ordering = ['created_at']
    
    def __str__(self):
        return f"回覆 - {self.ticket.title}"
