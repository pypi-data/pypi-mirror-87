from collections import OrderedDict

from djangoldp.factories import UserFactory
from test_plus import APITestCase

from djangoldp_notification.models import Subscription


class TestSubscription(APITestCase):
    user1 = None
    user2 = None
    circle_user1_url = "http://localhost:8000/circles/1"
    circle_user2_url = "http://localhost:8000/circles/2"

    def setUp(self):
        self.user1 = UserFactory(username="karl_marx", password="password")
        Subscription.objects.create(object=self.circle_user1_url, inbox="http://testserver/users/karl_marx/inbox/")

        self.user2 = UserFactory(username="piotr_kropotkine", password="password")
        Subscription.objects.create(object=self.circle_user2_url,
                                    inbox="http://testserver/users/piotr_kropotkine/inbox/")

    def test_not_logged_fails(self):
        response = self.get("/subscriptions/")
        self.assert_http_403_forbidden(response)
        self.assertEqual(response.data.get("detail"), "Authentication credentials were not provided.")

    def test_logged_in_succeeds(self):
        with self.login(self.user1):
            result = self.get("/subscriptions/").data.get("ldp:contains")
            expected = [OrderedDict({
                "@id": "http://localhost:8000/subscriptions/1/",
                "object": self.circle_user1_url,
                "inbox": "http://testserver/users/karl_marx/inbox/",
                "permissions": [{'mode': {'@type': 'view'}}, {'mode': {'@type': 'delete'}}]
            })]
            self.assertSequenceEqual(result, expected)

        with self.login(self.user2):
            result = self.get("/subscriptions/").data.get("ldp:contains")
            expected = [OrderedDict({
                "@id": "http://localhost:8000/subscriptions/2/",
                "object": self.circle_user2_url,
                "inbox": "http://testserver/users/piotr_kropotkine/inbox/",
                "permissions": [{'mode': {'@type': 'view'}}, {'mode': {'@type': 'delete'}}]
            })]
            self.assertSequenceEqual(result, expected)
