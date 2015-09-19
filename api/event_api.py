from rest_framework import serializers, viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event


class EventSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.published()
    serializer_class = EventSerializer

@api_view(['POST', 'OPTIONS'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes((IsAuthenticated,))
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
