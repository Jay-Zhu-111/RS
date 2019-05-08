from django.shortcuts import render
# from django.contrib.auth.models import User
# import django.contrib.auth as auth
from .models import MyUser, MyItem
from django.http import HttpResponse, Http404, HttpResponseRedirect
from recommend.RecommendModel import RecommendModel

recommend_model = RecommendModel()


def login(request):
    errors = []
    account = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('Please Enter account')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password = request.POST.get('password')
        if account is not None and password is not None:
            # user = auth.authenticate(username=account, password=password)
            user_list = list(MyUser.objects.filter(user_name=account, password=password)
                             .values_list('user_name', flat=True))
            if user_list:
                # if user.is_active:
                #     auth.login(request, user)
                #     return HttpResponseRedirect('/index/')
                # else:
                #     errors.append('disabled account')
                return HttpResponseRedirect('/recommend/map/' + account + '/')
            else:
                errors.append('invalid user')
    return render(request, 'recommend/login.html', {'errors': errors})


def register(request):
    errors = []
    account = None
    password = None
    password2 = None
    flag = False

    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('Please enter account')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password = request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('Please Enter password2')
        else:
            password2 = request.POST.get('password2')

        if password is not None and password2 is not None:
            if password == password2:
                flag = True
            else:
                errors.append('password2 is diff password')

        if account is not None and password is not None and password2 is not None and flag:
            user_list = list(MyUser.objects.filter(user_name=account, password=password)
                             .values_list('user_name', flat=True))
            if not user_list:
                MyUser.objects.create(user_name=account, password=password, L=[], S=[])
                return HttpResponseRedirect('/recommend/login/')
            else:
                errors.append('user exists')

    return render(request, 'recommend/register.html', {'errors': errors})


def map_with_baidu(request, account):
    # return HttpResponse(account)
    return render(request, 'recommend/BaiduMap.html', {'account': account})


def show_position(request, account, latitude, longitude):
    user_list = MyUser.objects.get(user_name=account)
    rank_list = recommend_model.get_result(user_list.user_name, user_list.L, user_list.S, latitude, longitude)
    item_list = []
    for item_id in rank_list:
        item = MyItem.objects.get(item_id=item_id)
        item_list.append(item)
    return render(request, 'recommend/Result.html', {'item_list': item_list})

    #     # item_list = []
    #     # for item_id in rank_list:
    #     #     name = list(MyItem.objects.filter(item_id=item_id)
    #     #                      .values_list('item_name', flat=True))[0]
    #     #     la = list(MyItem.objects.filter(item_id=item_id)
    #     #                       .values_list('latitude', flat=True))[0]
    #     #     lo = list(MyItem.objects.filter(item_id=item_id)
    #     #                       .values_list('longitude', flat=True))[0]
    #     #     item_list.append((name, float(la), float(lo)))
    #     # print(item_list)
    #     # return render(request, 'recommend/ResultMap.html', {'item_list': item_list})
    #
    #     # name_list, la_list, lo_list = [], [], []
    #     # for item_id in rank_list:
    #     #     name_list += list(MyItem.objects.filter(item_id=item_id)
    #     #                      .values_list('item_name', flat=True))
    #     #     la_list += list(MyItem.objects.filter(item_id=item_id)
    #     #                       .values_list('latitude', flat=True))
    #     #     lo_list += list(MyItem.objects.filter(item_id=item_id)
    #     #                       .values_list('longitude', flat=True))
    #     # return render(request, 'recommend/ResultMap.html', {'name_list': name_list,
    #                                                     'la_list': la_list,
    #                                                     'lo_list': lo_list,
    #                                                     'len': name_list.__len__()})
