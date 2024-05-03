from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from posts.models import Post
from questions.models import Qustion
from answers.models import Answer
from .serializers import PostSerializer,CreatePostSerializer

class PostListApiView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Post items for given requested user
        '''
        #posts = Post.objects.all().order_by('updated_at')
        posts = Post.objects.prefetch_related("default_response", "bot_response").all().order_by('updated_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Post with given Post data
        '''
        bot_response = None
        message = request.data.get('message')

        if request.data.get('question_id'):
            answerResponse = Answer.objects.get(question_id=request.data.get('question_id'))
            bot_response = answerResponse.id
            questionResponse = Qustion.objects.get(id=request.data.get('question_id'))
            message = questionResponse.question

        data = {
            'message': message, 
            'bot_response': bot_response
        }
        serializer = CreatePostSerializer(data=data)
        
        if serializer.is_valid():
            postInsert = serializer.save()
            post = Post.objects.prefetch_related("default_response", "bot_response").get(id=postInsert.id)
            serializerResponse = PostSerializer(post)
            return Response(serializerResponse.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)