# Generated for OT Setup

import django.db.models.deletion
import uuid

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emr", "0082_remove_encounter_encounter_class_history"),
        ("facility", "0486_mobileotp_failed_attempts_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OTRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "external_id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        unique=True,
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                    ),
                ),
                (
                    "modified_date",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                    ),
                ),
                (
                    "deleted",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                    ),
                ),
                ("history", models.JSONField(default=dict)),
                ("meta", models.JSONField(default=dict)),
                (
                    "description",
                    models.TextField(blank=True, default=""),
                ),
                (
                    "equipment_details",
                    models.JSONField(blank=True, default=list),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("available", "Available"),
                            ("occupied", "Occupied"),
                            ("maintenance", "Maintenance"),
                            ("inactive", "Inactive"),
                        ],
                        default="available",
                        max_length=20,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "facility",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ot_rooms",
                        to="facility.facility",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ot_room_configurations",
                        to="emr.facilitylocation",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "emr_ot_room",
                "ordering": ["location__name"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("facility", "location"),
                        name="unique_ot_location_per_facility",
                    )
                ],
            },
        ),
    ]
