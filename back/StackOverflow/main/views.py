from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .funcs.permissions import IsAuthenticatedOrReadOnly
from .models import Topic, Message
from .serializers import TopicSerializer, MessageSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(username=user.username)
        else:
            raise ValidationError("User is not authenticated.")

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(username=user.username)
        else:
            raise ValidationError("User is not authenticated.")
        
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def react(self, request, pk=None):
        message = self.get_object()
        user = request.user

        reaction = request.data.get('reaction')

        if reaction not in ['up', 'down']:
            return Response({'detail': 'Invalid reaction.'}, status=status.HTTP_400_BAD_REQUEST)

        if message.users_reacted.filter(id=user.id).exists():
            current_reaction = 'up' if message.reactions > 0 else 'down'
            
            if current_reaction == reaction:
                if reaction == 'up':
                    message.reactions -= 1
                else:
                    message.reactions += 1
                
                message.users_reacted.remove(user)
                message.save()
                return Response({'reactions': message.reactions, 'detail': 'Reaction removed.'})
            
            else:
                if reaction == 'up':
                    message.reactions += 2  
                else:
                    message.reactions -= 2  
                
                message.users_reacted.add(user)
                message.save()
                return Response({'reactions': message.reactions, 'detail': 'Reaction changed.'})
        
        if reaction == 'up':
            message.reactions += 1
        elif reaction == 'down':
            message.reactions -= 1

        message.users_reacted.add(user)
        message.save()

        return Response({'reactions': message.reactions, 'detail': 'Reaction added.'})

class LatestTopicView(RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_object(self):
        return self.queryset.order_by("id").last()
    
class MessagesByTopicTitleView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        title = self.kwargs['title']
        print(f"Title received: {title}")
        if 'questions' in self.request.path:
            message_type = Message.QUESTION
        elif 'answers' in self.request.path:
            message_type = Message.ANSWER
        else:
            message_type = None

        queryset = Message.objects.filter(topic__title=title)

        if message_type:
            queryset = queryset.filter(message_type=message_type)

        return queryset
    
class IncrementTopicViews(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id):
        try:
            topic = Topic.objects.get(id=id)
            topic.views += 1
            topic.save()
            return Response({'status': 'views incremented'}, status=status.HTTP_200_OK)
        except Topic.DoesNotExist:
            return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)
