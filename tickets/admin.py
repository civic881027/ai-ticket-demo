from django.contrib import admin
from .models import Ticket, TicketResponse

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'priority', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'priority', 'category']
    search_fields = ['title', 'description', 'category']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TicketResponse)
class TicketResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'is_ai_generated', 'created_by', 'created_at']
    search_fields = ['response_text']
    readonly_fields = ['created_at']
