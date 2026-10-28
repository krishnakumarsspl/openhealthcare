from django.db import models

from care.emr.models.base import EMRBaseModel


class OTRoom(EMRBaseModel):
    facility = models.ForeignKey(
        "facility.Facility",
        on_delete=models.PROTECT,
        related_name="ot_rooms",
    )

    # Link to the existing room in Location Master.
    location = models.ForeignKey(
        "emr.FacilityLocation",
        on_delete=models.PROTECT,
        related_name="ot_room_configurations",
    )

    description = models.TextField(blank=True, default="")

    equipment_details = models.JSONField(
        default=list,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("available", "Available"),
            ("occupied", "Occupied"),
            ("maintenance", "Maintenance"),
            ("inactive", "Inactive"),
        ],
        default="available",
    )

    class Meta:
        db_table = "emr_ot_room"
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "location"],
                name="unique_ot_location_per_facility",
            )
        ]
        ordering = ["location__name"]

    def __str__(self):
        return f"{self.location.name} - {self.get_status_display()}"


class SurgeryProcedure(EMRBaseModel):
    facility = models.ForeignKey(
        "facility.Facility",
        on_delete=models.PROTECT,
        related_name="surgery_procedures",
    )

    procedure_name = models.CharField(max_length=255)

    procedure_code = models.CharField(max_length=100)

    department = models.ForeignKey(
        "emr.FacilityOrganization",
        on_delete=models.PROTECT,
        related_name="surgery_procedures",
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    description = models.TextField(blank=True, default="")

    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
        ],
        default="active",
    )

    class Meta:
        db_table = "emr_surgery_procedure"
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "procedure_code"],
                name="unique_surgery_procedure_code_per_facility",
            )
        ]
        ordering = ["procedure_name"]

    def __str__(self):
        return f"{self.procedure_code} - {self.procedure_name}"

class Anaesthesia(EMRBaseModel):
    facility = models.ForeignKey(
        "facility.Facility",
        on_delete=models.PROTECT,
        related_name="anaesthesia_methods",
    )

    anaesthesia_name = models.CharField(max_length=255)

    anaesthesia_code = models.CharField(max_length=100)

    description = models.TextField(blank=True, default="")

    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
        ],
        default="active",
    )

    class Meta:
        db_table = "emr_anaesthesia"
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "anaesthesia_code"],
                name="unique_anaesthesia_code_per_facility",
            )
        ]
        ordering = ["anaesthesia_name"]

    def __str__(self):
        return f"{self.anaesthesia_code} - {self.anaesthesia_name}"
