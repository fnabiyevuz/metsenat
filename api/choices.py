from django.db import models


class SponsorType(models.TextChoices):
    JISMONIY = "Jismoniy shaxs"
    YURIDIK = "Yuridik shaxs"


class SponsorStatus(models.TextChoices):
    YANGI = "Yangi"
    MODERATSIYADA = "Moderatsiyada"
    TASDIQLANGAN = "Tasdiqlangan"
    BEKOR_QILINGAN = "Bekor qilingan"


class PaymentType(models.TextChoices):
    NAQD = "Naqd"
    PUL_OTKAZMALARI = "Pul o'tkazmalari"


class StudentType(models.TextChoices):
    BAKALAVR = "Bakalavr"
    MAGISTR = "Magistr"
