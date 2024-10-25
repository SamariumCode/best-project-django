import datetime
from datetime import timezone
from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

User = get_user_model()

class TicketOptions(Enum):
    # status
    PENDING = "pending"
    PENDING_LABEL = _("Pending")
    ANSWERED = "answered"
    ANSWERED_LABEL = _("Answered")
    CLOSED = "closed"
    CLOSED_LABEL = _("Closed")

    # section
    MANAGEMENT = "management"
    MANAGEMENT_LABEL = _("Management")
    FINANCES = "finances"
    FINANCES_LABEL = _("Finances")
    SUPPORT = "support"
    SUPPORT_LABEL = _("Support")

    # priority
    LOW = "low"
    LOW_LABEL = _("Low")
    MEDIUM = "medium"
    MEDIUM_LABEL = _("Medium")
    HIGH = "high"
    HIGH_LABEL = _("High")

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    title = models.CharField(max_length=255, verbose_name=_("Title Ticket"))

    status = models.CharField(max_length=255, choices=[
        (TicketOptions.PENDING.value, _(TicketOptions.PENDING_LABEL.value)),
        (TicketOptions.ANSWERED.value, _(TicketOptions.ANSWERED_LABEL.value)),
        (TicketOptions.CLOSED.value, _(TicketOptions.CLOSED_LABEL.value))
    ], default=TicketOptions.PENDING.value, verbose_name=_("Status"))

    section = models.CharField(max_length=128, choices=[
        (TicketOptions.MANAGEMENT.value, _(TicketOptions.MANAGEMENT_LABEL.value)),
        (TicketOptions.FINANCES.value, _(TicketOptions.FINANCES_LABEL.value)),
        (TicketOptions.SUPPORT.value, _(TicketOptions.SUPPORT_LABEL.value))
    ], default=TicketOptions.SUPPORT.value, verbose_name=_("Section"))

    priority = models.CharField(max_length=128, choices=[
        (TicketOptions.LOW.value, _(TicketOptions.LOW_LABEL.value)),
        (TicketOptions.MEDIUM.value, _(TicketOptions.MEDIUM_LABEL.value)),
        (TicketOptions.HIGH.value, _(TicketOptions.HIGH_LABEL.value))
    ], default=TicketOptions.LOW.value, verbose_name=_("Priority"))

    seen_by_user = models.BooleanField(default=False, verbose_name=_("Seen by user"))
    seen_by_admin = models.BooleanField(default=False, verbose_name=_("Seen by admin"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"))

    def __str__(self):
        return f"{self.id}:{self.title}"

    def save(self, *args, **kwargs):
        if self.pk:
            last_message = self.ticketmessage_set.order_by("-id").first()
        else:
            last_message = None
        
        if self.status != TicketOptions.CLOSED.value and last_message:
            if last_message.user and last_message.user.is_superuser:
                self.status = TicketOptions.ANSWERED.value
                self.seen_by_admin = True
                now = datetime.datetime.now(timezone.utc)
                if (now - last_message.created).seconds < 5:
                    self.seen_by_user = False
            else:
                self.status = TicketOptions.PENDING.value

        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_("Ticket"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_("User"))
    message = models.TextField(null=False, blank=False, verbose_name=_("Message"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated"))

    def __str__(self):
        return f"{self.id}:{self.message[:20]}"

    class Meta:
        verbose_name = _("Ticket Message")
        verbose_name_plural = _("Ticket Messages")


@receiver(post_save, sender=TicketMessage)
def after_create(sender, instance, created, **kwargs):
    if created and instance.ticket and instance.ticket.status != TicketOptions.CLOSED.value:
        if instance.user and (instance.user.is_superuser or instance.user.is_staff):
            instance.ticket.status = TicketOptions.ANSWERED.value
        else:
            instance.ticket.status = TicketOptions.PENDING.value

    instance.ticket.save()
