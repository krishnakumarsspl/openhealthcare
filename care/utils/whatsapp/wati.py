import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class WATIClient:
    """
    Client for communicating with the WATI WhatsApp API.
    """

    def __init__(self):
        self.base_url = settings.WATI_BASE_URL.rstrip("/")
        self.access_token = settings.WATI_ACCESS_TOKEN

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def send_template_message(
        self,
        phone_number,
        template_name,
        parameters=None,
        broadcast_name="OHC",
    ):
        """
        Send a WhatsApp template message using WATI.
        """

        phone_number = "".join(
            ch for ch in str(phone_number) if ch.isdigit()
        )

        if len(phone_number) < 10:
            return {
                "success": False,
                "error": "Invalid phone number",
            }

        if not self.access_token:
            return {
                "success": False,
                "error": "WATI access token is not configured",
            }

        url = f"{self.base_url}/sendTemplateMessage"

        payload = {
            "template_name": template_name,
            "broadcast_name": broadcast_name,
            "parameters": parameters or [],
            "channel_number": settings.WATI_CHANNEL_NUMBER,
        }

        try:
            response = requests.post(
                url,
                params={"whatsappNumber": phone_number},
                json=payload,
                headers=self._headers(),
                timeout=20,
            )

            try:
                result = response.json()
            except ValueError:
                result = {"response": response.text}

            if not response.ok:
                logger.error(
                    "WATI API failed: status=%s response=%s",
                    response.status_code,
                    result,
                )

            return {
                "success": response.ok,
                "phone": phone_number,
                "status": response.status_code,
                "result": result,
            }

        except requests.RequestException as exc:
            logger.exception("WATI request failed")

            return {
                "success": False,
                "phone": phone_number,
                "error": str(exc),
            }

    def send_report_available(
        self,
        phone,
        name,
        report_url,
        sender_name,
    ):
        """
        Send the treatment report URL using the approved WATI template.
        """

        if not report_url or not report_url.startswith("https://"):
            return {
                "success": False,
                "error": "Report URL must start with https://",
            }

        template_name = getattr(
            settings,
            "WATI_TEMPLATE_NAME",
            "treatment_report",
        )

        parameters = [
            {"name": "1", "value": str(name)},
            {"name": "2", "value": report_url},
            {"name": "3", "value": str(sender_name)},
        ]

        return self.send_template_message(
            phone_number=phone,
            template_name=template_name,
            parameters=parameters,
            broadcast_name="Report Available",
        )
