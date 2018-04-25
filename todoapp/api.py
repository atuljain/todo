from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer

from models import Task

class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        list_allowed_methods = ['get', 'post', ]
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            'title': ['startswith', 'contains', 'exact', 'regex'],
            'due_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'state':['exact']
        }
        # serializer = Serializer(formats=['json', 'xml'])