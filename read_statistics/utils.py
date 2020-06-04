from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
import datetime
from read_statistics.models import ReadNum,ReadDetail

'''
获取阅读量相关的数据
'''
def read_statistics_onece_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model,obj.pk)

    #  总阅读数 +1
    # if not request.COOKIES.get(key):
    #     if ReadNum.objects.filter(content_type=ct,object_id=obj.pk).count():
    #         readnum =ReadNum.objects.get(content_type=ct,object_id=obj.pk)
    #     else:
    #         readnum = ReadNum(content_type=ct,object_id=obj.pk)
    #     readnum.read_num +=1
    #     readnum.save()
    if not request.COOKIES.get(key):
        readnum,created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天x博客的阅读数+1
        date = timezone.now().date()
        readDetail , created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key

'''
获取当日前七天的阅读量数据
'''
def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days = i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = read_details.aggregate(read_num_sum = Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return  dates, read_nums

'''
获取今日热点文章
'''
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')
    return read_details[:7]


'''
获取昨日热点文章
'''
def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')
    return read_details[:7]


