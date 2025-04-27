from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from .utils import CategoryChoices, ConditionChoices, ProposalStatusChoices


class Ad(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=30, choices=CategoryChoices.choices, default=CategoryChoices.OTHER)
    condition = models.CharField(max_length=30, choices=ConditionChoices.choices, default=ConditionChoices.USED)
    created_at = models.DateTimeField(auto_now_add=True)
    search_vector = SearchVectorField(null=True)

    def get_absolute_url(self):
        return reverse('ads:ad_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['condition']),
            GinIndex(fields=["search_vector"]),
        ]


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.TextField()
    status = models.CharField(max_length=30, choices=ProposalStatusChoices.choices,
                              default=ProposalStatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.ad_sender == self.ad_receiver:
            raise ValidationError("Нельзя обмениваться товарами с самим собой.")

    def __str__(self):
        return f"{self.ad_sender} → {self.ad_receiver} ({self.status})"

    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]
