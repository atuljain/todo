# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from models import Task


class TaskResourceTest(ResourceTestCaseMixin, TestCase):
    # Using ``fixtures`` as normal.
    fixtures = ['test-task.json']
    # Setup for test
    def setUp(self):
        super(TaskResourceTest, self).setUp()

        # Create a user.
        self.username = 'atul-test'
        self.password = 'atul0000test'
        self.user = User.objects.create_user(self.username, 'atul@test.com', self.password)

        # Fetch the ``Task`` object we'll use in testing.
        # Note that we aren't using PKs because they can change depending
        # on what other tests are running.
        self.task_1 = Task.objects.get(pk=1)

        # We also build a detail URI, since we will be using it all over.
        self.detail_url = '/api/task/{0}/'.format(self.task_1.pk)

        # The data we'll send on POST requests. Again, because we'll use it
        # frequently (enough).
        self.post_data = {
            'user': '/api/user/{0}/'.format(self.user.pk),
            'title': 'Second Post!',
            'created': '2012-05-01T22:05:12',
            'due_date': '2012-05-01T22:05:12',
        }

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/task/', format='json'))

    def test_get_list_json(self):
        resp = self.api_client.get('/api/task/', format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)
        # Here, we're checking an entire structure for the expected data.
        data = {
            'id': self.task_1.id,
            'title': 'sad',
            'due_date': '2018-04-23',
            'created_at': '2018-04-23T10:25:40.827000',
            'resource_uri': '/api/task/{0}/'.format(self.task_1.pk),
            'updated_at': '2018-04-23T10:26:43.852000',
            'state': 'pending'
        }
        self.assertEqual(self.deserialize(resp)['objects'][0], data)


    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get(self.detail_url, format='json'))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)
        # We use ``assertKeys`` here to just verify the keys, not all the data.
        self.assertKeys(self.deserialize(resp), ['due_date', 'title', 'created_at', 'updated_at', 'state','id', 'resource_uri'])

    
    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/task/', format='json', data=self.post_data))

    def test_post_list(self):
        #  send a post request to create a record
        self.assertHttpCreated(self.api_client.post('/api/task/', format='json', data=self.post_data, authentication=self.get_credentials()))

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.put(self.detail_url, format='json', data={}))

    def test_put_detail(self):
        # Grab the current data & modify it slightly.
        # import pdb; pdb.set_trace()
        original_data = self.deserialize(self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials()))
        new_data = original_data.copy()
        new_data['title'] = 'Updated: First Post'
        new_data['created'] = '2012-05-01T20:06:12'

        self.assertHttpAccepted(self.api_client.put(self.detail_url, format='json', data=new_data, authentication=self.get_credentials()))

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.delete(self.detail_url, format='json'))

    def test_delete_detail(self):
        # import pdb; pdb.set_trace()
        self.assertHttpAccepted(self.api_client.delete(self.detail_url, format='json', authentication=self.get_credentials()))
