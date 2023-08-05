from datetime import datetime, timedelta
from rest_framework.test import APITestCase, APIClient

from risefor_lobbying.models import ActionGroup, Theme
from risefor_lobbying.tests.models import User


class ActionGroupTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def setUpLoggedInUser(self):
        self.user = User(email='test@mactest.co.uk', first_name='Test', last_name='Mactest', username='test',
                         password='glass onion')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def setUpActionGroups(self):
        date_30_days_ago = datetime.now() - timedelta(days=30)
        date_today = datetime.now()
        date_30_days_from_now = datetime.now() + timedelta(days=30)
        theme = Theme(name='Test Theme')
        theme.save()

        self.ag_30_days_ago = ActionGroup(actiondate=date_30_days_ago, theme=theme)
        self.ag_30_days_ago.save()
        self.ag_today = ActionGroup(actiondate=date_today, theme=theme)
        self.ag_today.save()
        self.ag_30_days_from_now = ActionGroup(actiondate=date_30_days_from_now, theme=theme)
        self.ag_30_days_from_now.save()

    # GET action groups convergence - both start date and end date active
    def test_get_action_groups_convergence_both_active(self):
        self.setUpLoggedInUser()
        self.setUpActionGroups()

        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)

        response = self.client.get('/convergent-actions/?start_date=' + str(yesterday.date()) +
                                   '&end_date=' + str(tomorrow.date()))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['ldp:contains']), 1)
        self.assertEqual(response.data['ldp:contains'][0]['@id'],
                         "http://testserver/actiongroups/{}/".format(self.ag_today.pk))

    def test_get_action_groups_convergence_invalid_param(self):
        self.setUpLoggedInUser()
        self.setUpActionGroups()

        yesterday = 'somethinginvalid'

        response = self.client.get('/convergent-actions/?start_date=' + str(yesterday))

        self.assertEqual(response.status_code, 400)
