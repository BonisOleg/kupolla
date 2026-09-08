import logging
from datetime import datetime

import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Lead

logger = logging.getLogger('src')


@receiver(post_save, sender=Lead)
def send_to_crm(sender, instance, created, **kwargs):
    if not created:
        return

    from src.core.crm import build_lead_payload, get_crm_webhook_url, is_configured_crm_webhook

    webhook_url = get_crm_webhook_url()
    if not is_configured_crm_webhook(webhook_url):
        return

    payload = build_lead_payload(instance)

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'KUPOLLA-Website/1.0',
            },
        )
        response.raise_for_status()
        Lead.objects.filter(pk=instance.pk).update(
            crm_sent=True,
            crm_sent_at=timezone.now(),
        )
        logger.info('Lead #%s sent to CRM successfully', instance.pk)
    except requests.HTTPError as exc:
        body = ''
        if exc.response is not None:
            body = exc.response.text[:500]
        logger.error(
            'CRM webhook HTTP error for Lead #%s: %s — response: %s',
            instance.pk,
            exc,
            body,
        )
    except requests.RequestException as exc:
        logger.error('CRM webhook failed for Lead #%s: %s', instance.pk, exc)
