from django.shortcuts import render
# from django.contrib.auth.models import User
# import django.contrib.auth as auth
from .models import MyUser, MyItem
from django.http import HttpResponse, Http404, HttpResponseRedirect
from recommend.RecommendModel import RecommendModel
import random
import json

recommend_model = RecommendModel()
with open('data/cold_start_user.txt', 'r', encoding='UTF-8') as f:
    cold_dict = eval(f.read())
with open('data/user_set.txt', 'r', encoding='UTF-8') as f:
    user_set = eval(f.read())
# item_list = list(MyUser.objects.all.values_list(('latitude', 'longitude'), flat=True))
# print(item_list)

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
    return render(request, 'recommend/BaiduMap.html', {'account': account})


last_item_list = []
def show_position(request, account, latitude, longitude):
    user = MyUser.objects.get(user_name=account)
    L = eval(user.L)
    S = eval(user.S)
    if L.__len__() + S.__len__() == 0:
        if user.user_name in cold_dict:
            friend_list = cold_dict[user.user_name]
            flag = False
            for i in range(50):
                friend = str(random.choice(friend_list))
                if friend in user_set:
                    user_friend = list(MyUser.objects.filter(user_name=friend)
                                     .values_list('user_name', flat=True))
                    if user_friend:
                        user = MyUser.objects.get(user_name=user_friend[0])
                        user_id = user_set.index(user.user_name)
                        L = eval(user.L)
                        S = eval(user.S)
                        flag = True
                        break
                else:
                    print('friend not in user_set')
            if not flag:
                return HttpResponse('Friends not in database.')
        else:
            return HttpResponse('No friendship info.')
    else:
        user_id = user_set.index(user.user_name)
    rank_list = recommend_model.get_result(user_id, L, S, latitude, longitude)
    item_list = []
    for item_id in rank_list:
        item = MyItem.objects.get(item_id=item_id)
        item_list.append(item)
    global last_item_list
    last_item_list = item_list
    return render(request, 'recommend/Result.html', {'item_list': item_list,
                                                     'account': account,
                                                     'latitude': latitude,
                                                     'longitude': longitude})

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


def show_result(request, account, latitude, longitude):
    name_list, la_list, lo_list = [], [], []
    for item in last_item_list:
        # item = MyItem.objects.get(item_id=item_id)
        name_list.append(item.item_name)
        la_list.append(item.latitude)
        lo_list.append(item.longitude)

        # name_list += list(MyItem.objects.filter(item_id=item_id)
        #                  .values_list('item_name', flat=True))
        # la_list += list(MyItem.objects.filter(item_id=item_id)
        #                   .values_list('latitude', flat=True))
        # lo_list += list(MyItem.objects.filter(item_id=item_id)
        #                   .values_list('longitude', flat=True))
    return render(request, 'recommend/ResultMap.html', {'name_list': json.dumps(name_list),
                                                        'la_list': json.dumps(la_list),
                                                        'lo_list': json.dumps(lo_list),
                                                        'len': json.dumps(name_list.__len__()),
                                                        'latitude': json.dumps(latitude),
                                                        'longitude': json.dumps(longitude)})
