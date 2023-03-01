from django.db.models import Sum

from .choices import *


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Sponsors(BaseModel):
    type = models.CharField(max_length=15, choices=SponsorType.choices, default=SponsorType.YURIDIK)
    fish = models.CharField(max_length=255)
    phone = models.CharField(max_length=9)
    summa = models.IntegerField()
    organization = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=15, choices=SponsorStatus.choices, default=SponsorStatus.YANGI)
    payment = models.CharField(max_length=16, choices=PaymentType.choices, default=PaymentType.NAQD)

    def __str__(self):
        return self.fish

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"

    @property
    def donation(self):
        donations = self.sponsor_donations.all().aggregate(total=Sum('summa'))['total']
        if donations:
            return donations
        return 0

    @property
    def residue(self):
        res = self.summa - self.donation

        if res:
            return res
        return 0


class OTMs(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "OTM"
        verbose_name_plural = "OTMs"


class Students(BaseModel):
    type = models.CharField(max_length=15, choices=StudentType.choices, default=StudentType.BAKALAVR)
    fish = models.CharField(max_length=255)
    phone = models.CharField(max_length=9)
    contract = models.IntegerField()
    otm = models.ForeignKey(OTMs, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.fish

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    @property
    def donation(self):
        donations = self.student_donations.all().aggregate(total=Sum('summa'))['total']
        if donations:
            return donations
        return 0

    @property
    def residue(self):
        res = self.contract - self.donation
        if res:
            return res
        return 0


class Donations(BaseModel):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student_donations")
    sponsor = models.ForeignKey(Sponsors, on_delete=models.CASCADE, related_name="sponsor_donations")
    summa = models.IntegerField()

    def __str__(self):
        return self.student.fish + " " + self.sponsor.fish + " " + (self.summa)

    class Meta:
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
