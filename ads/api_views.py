from django.db.models import Q
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Ad, ExchangeProposal
from .permissions import AdIsOwnerOrReadOnly, ProposalIsParticipantOrSenderOnly
from .serializers import AdReadSerializer, AdWriteSerializer, ExchangeProposalSerializer


class AdViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    queryset = Ad.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), AdIsOwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AdReadSerializer
        return AdWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = AdReadSerializer(serializer.instance, context=self.get_serializer_context())
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого объявления.")
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = AdReadSerializer(serializer.instance, context=self.get_serializer_context())
        return Response(read_serializer.data)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого объявления.")
        instance.delete()


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated, ProposalIsParticipantOrSenderOnly]
    filterset_fields = ['status', 'ad_sender', 'ad_receiver']

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(Q(ad_sender__user=user) | Q(ad_receiver__user=user))

    def perform_create(self, serializer):
        ad_sender = serializer.validated_data['ad_sender']
        ad_receiver = serializer.validated_data['ad_receiver']
        user = self.request.user

        if ad_receiver.user == user:
            raise PermissionDenied("Нельзя обмениваться товарами с самим собой.")

        if ad_sender.user != user:
            raise PermissionDenied("Вы не можете создать заявку на обмен не своего объявления")

        serializer.save(status='pending')
