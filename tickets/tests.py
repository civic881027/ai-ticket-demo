from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ticket

class TicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.ticket = Ticket.objects.create(
            title='單元測試',
            description='自動化測試工單',
            created_by=self.user,
            category='技術問題'
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.title, '單元測試')
        self.assertEqual(self.ticket.category, '技術問題')
