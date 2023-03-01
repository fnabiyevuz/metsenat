from datetime import datetime, date as datee
from django.http import Http404
from django_filters import rest_framework as filterss
from rest_framework import filters, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import SponsorsFilter
from .serializers import *
from django.contrib.auth import authenticate


class SponsorCreate(CreateAPIView):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer


class SponsorList(ListAPIView):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer
    filter_backends = [filterss.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SponsorsFilter
    search_fields = ['type', 'fish', 'phone', 'summa', 'organization', 'status', 'payment']


class Sponsor(RetrieveAPIView):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer


class SponsorUpdate(UpdateAPIView):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer


# @api_view()
# def get_sponsor(request):
#     sponsors = Sponsors.objects.filter(status='Tasdiqlangan')
#     donations = Donations.objects.annotate(total=Sum('summa'))
#
#     return Response(serializer)


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsReadSerializer
    filter_backends = [filterss.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'otm']
    search_fields = ['fish']

    def destroy(self, request, pk=None):
        response = {'message': 'Delete function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        serializer = StudentsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DonationsView(APIView):

    def get(self, request):
        r = request.GET
        student_id = r['student_id']
        student = Students.objects.get(id=student_id)
        serializer = StudentsReadSerializer(student)
        donations = student.student_donations.all()
        serializer_donations = DonationsReadSerializer(donations, many=True)

        return Response({
            'student': serializer.data,
            'donations': serializer_donations.data
        })

    def post(self, request):
        r = request.data.get
        student_id = r('student_id')
        sponsor_id = r('sponsor_id')
        summa = int(r('summa'))
        sponsor = Sponsors.objects.get(id=sponsor_id)
        student = Students.objects.get(id=student_id)

        if sponsor.residue > summa:
            donation = Donations.objects.create(student=student, sponsor=sponsor, summa=summa)
        else:
            return Response({'result': "Sponsor has not enought money"})
        serializer = DonationsCreateSerializer(donation).data
        return Response(serializer)


class DonationDetailView(APIView):

    def get(self, request, pk, format=None):
        try:
            serializer = DonationsReadSerializer(Donations.objects.get(pk=pk))
            return Response(serializer.data)
        except Donations.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        r = request.data
        summa = int(r['summa'])
        # student = Students.objects.get(id=r['student'])
        sponsor = Sponsors.objects.get(id=r['sponsor'])
        donation = Donations.objects.get(pk=pk)
        serializer = DonationsCreateSerializer(donation, data=request.data)
        if serializer.is_valid():
            if sponsor == donation.sponsor:
                if donation.sponsor.residue + donation.summa > summa and donation.student.residue + donation.summa > summa:
                    serializer.save()
                    return Response(serializer.data)
                raise Exception("Donation has no enough money or etc.")
            else:
                if sponsor.residue > summa and donation.student.residue + donation.summa > summa:
                    serializer.save()
                    return Response(serializer.data)
                raise Exception("Donation has no enough money or etc.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def dashboard(request):
    paid = Sponsors.objects.filter(status='Tasdiqlangan').aggregate(total=Sum('summa'))['total']
    requested = Students.objects.all().aggregate(total=Sum('contract'))['total']
    date = datetime.today()
    year = date.year
    data = []
    months = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avgust', 'Sentabr', 'Oktabr', 'Noyabr',
              'Dekabr']
    for i in range(1, 13):
        if i == 12:
            month2 = 1
            year2 = year + 1
        else:
            month2 = i + 1
            year2 = year
        gte = datetime(year, i, 1)
        lt = datetime(year2, month2, 1)
        spon = Sponsors.objects.filter(created_at__gte=gte, created_at__lte=lt)
        stud = Students.objects.filter(created_at__gte=gte, created_at__lte=lt)
        dt = {
            'month': months[i - 1],
            'sponsors': spon.count(),
            'paid': spon.aggregate(total=Sum('summa'))['total'],
            'students': stud.count(),
            'need': stud.aggregate(total=Sum('contract'))['total'],
        }
        data.append(dt)

    return Response({
        'paid': paid,
        'requested': requested,
        'need': requested - paid,
        'data': data
    })


@api_view()
def by_day(request):
    paid = Sponsors.objects.filter(status='Tasdiqlangan').aggregate(total=Sum('summa'))['total']
    requested = Students.objects.all().aggregate(total=Sum('contract'))['total']
    date = datetime.today()
    year = date.year
    start_date = datetime(year, 1, 1).toordinal()
    finish_date = datetime(year, 12, 31).toordinal()
    data = []
    for date in range(start_date, finish_date + 1):
        spon = Sponsors.objects.filter(created_at__gte=datee.fromordinal(date),
                                       created_at__lte=datee.fromordinal(date + 1))
        stud = Students.objects.filter(created_at__gte=datee.fromordinal(date),
                                       created_at__lte=datee.fromordinal(date + 1))
        dt = {
            'date': datee.fromordinal(date),
            'sponsors': spon.count(),
            'paid': spon.aggregate(total=Sum('summa'))['total'],
            'students': stud.count(),
            'need': stud.aggregate(total=Sum('contract'))['total'],
        }
        data.append(dt)

    return Response({
        'paid': paid,
        'requested': requested,
        'need': requested - paid,
        'data': data
    })


@api_view(['POST'])
def sign_in(request):
    try:
        r = request.data
        username = r['username']
        password = r['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
        return Response({
            'result': "User don't found"
        })
    except Exception as e:
        return Response({
            'error': f'{e}'
        })
