from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class AuthorizationViewTest(APITestCase):
    def setUp(self) -> None:
        self.base_url = reverse("authentication")

    def test_test(self):
        print('intra')