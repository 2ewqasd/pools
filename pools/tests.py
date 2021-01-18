import time
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Pool


class PoolTests(APITestCase):
    def test_show_pool_list(self):
        """
        Ensure we can retrieve list of pools.
        """
        url = reverse('pool-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        Pool.objects.create(name="Test", end_date=timezone.now()+timedelta(days=1))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_active_pool_list(self):
        """
        Ensure we can retrieve only active list of pools.
        """
        url = reverse('pool-list')
        Pool.objects.create(name="Test", end_date=timezone.now()+timedelta(seconds=10))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        time.sleep(10)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
