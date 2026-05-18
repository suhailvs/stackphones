from myapp.models import PhoneSpec
from django.db.models import Count, Q
print(PhoneSpec.objects.exclude(
    Q(announced__startswith='20')|
    Q(announced__startswith='199')
).values('announced').annotate(c=Count('id')).order_by('-c'))
print(PhoneSpec.objects.count()-PhoneSpec.objects.filter(Q(announced__startswith='20')|Q(announced__startswith='199')).count())

print()
print(PhoneSpec.objects.exclude(
    Q(status__startswith='Available. Released')|
    Q(status__startswith='Discontinued')|
    Q(status__startswith='Cancelled')
).values('status').annotate(c=Count('id')).order_by('-c'))
print(PhoneSpec.objects.count()-PhoneSpec.objects.filter(
    Q(status__startswith='Available. Released')|
    Q(status__startswith='Discontinued')|
    Q(status__startswith='Cancelled')).count())