from rest_framework import permissions


class AdIsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование/удаление только автору объявления.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class ProposalIsParticipantOrSenderOnly(permissions.BasePermission):
    """
    Разрешает чтение только участникам обмена.
    Разрешает редактирование/удаление только отправителю.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return obj.ad_sender.user == user or obj.ad_receiver.user == user

        return obj.ad_sender.user == user
