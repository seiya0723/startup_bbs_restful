from rest_framework import status,views,response
from django.shortcuts import render,redirect,get_object_or_404

from django.http.response import JsonResponse
from django.template.loader import render_to_string

from .models import Topic
from .serializer import TopicSerializer

import json 

class BbsView(views.APIView):
    def get(self,request,*args,**kwargs):

        data        = Topic.objects.all()
        context     = {"data":data}
        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        serializer      = TopicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data        = Topic.objects.all()
        context     = {"data":data}
        content_data_string     = render_to_string('bbs/comment.html', context ,request)
        json_data               = { "content" : content_data_string }

        return JsonResponse(json_data)

index   = BbsView.as_view()

class BbsDeleteView(views.APIView):

    def delete(self, request, pk, *args, **kwargs):

        topic           = get_object_or_404(Topic,pk=pk)
        topic.delete()

        data        = Topic.objects.all()
        context     = {"data":data}
        content_data_string     = render_to_string('bbs/comment.html', context ,request)
        json_data               = { "content" : content_data_string }

        return JsonResponse(json_data)

delete  = BbsDeleteView.as_view()
