from django.shortcuts import render,HttpResponse,redirect,render_to_response
from django.http import JsonResponse
from django.contrib import auth
from info import models
from info.form.login import StudentForm
from info.pager import Pagination, PaginationG
import json
import uuid

from info.Helper import Checkcode
import io


#登陆


def create_uuid():
    s_uuid = str(uuid.uuid1())
    l_uuid = s_uuid.split('-')
    uid = ''.join(l_uuid)
    return uid


#登陆
def login(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("account")
        pwd = request.POST.get("password")
        user = auth.authenticate(username=username, password=pwd)
        if user:
            # 用户名密码正确
            # 给用户做登录
            ret["status"] = 1
            auth.login(request, user)
            ret["msg"] = "/index/"
        else:
            # 用户名密码错误
            ret["status"] = 0
            ret["msg"] = "用户名或密码错误,请重新输入！"
        return JsonResponse(ret)
    return render(request, "login.html")


#空白页面
def welcome(request):
    return render(request, 'welcome.html')

#退出登录
def logout(request):
    auth.logout(request)
    return redirect('/login/')


#首页
def index(request):
    # print(request.user.is_authenticated())
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('/login/')


#文章列表
def article_list(request):
    article_list = models.Article.objects.all().order_by("-create_time")
    count = models.Article.objects.all().count()
    # print(count)
    # print(article_list.tags__set("title"), type(article_list))
    # article_list = []
    # for a in article_obj:
    #     print(a.tags.all())
    # #     tags = models.Tag.objects.filter(nid=article_list).values_list("title")
    # #     article_list.append(a)
    # # print(article_list)
    return render(request, 'article-list.html', locals())


#添加文章 保存并提交
def add_article(request):
    tags_list = models.Tag.objects.all()
    if request.method == "POST":
        # print(request.POST)
        # print("-" * 120)
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        tags = request.POST.get("tags")
        article_content = request.POST.get("article_content")
        user = request.user
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, 'html.parser')
        # print(bs,type(bs))
        # print("-" * 120)

        # desc = bs[0:150]

        for tag in bs.find_all():
            if tag.name in["script"]:
                tag.decompose()
        tag_obj = models.Tag.objects.filter(title=tags).first()
        article_obj = models.Article.objects.create(title=title, desc=desc, status=1, content=str(bs), tags_id=tag_obj.nid)
        # models.ArticleDetail.objects.create(content=str(bs), article=article_obj)
        ret = {}
        ret["msg"] = "提交成功，已发布！！"
        ret["link"] = "/article_list/"
        return JsonResponse(ret)
        # import time
        # time.sleep(5)
        # return redirect('/index/')

    return render(request, 'article-add.html', locals())


#删除文章
def del_article(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Article.objects.filter(nid=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


#文章下架(停用)
def article_stop(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Article.objects.filter(nid=id).update(status=0)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)



#文章悬浮下架(停用)
def float_stop(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Float.objects.filter(nid=id).update(status=0)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


#文章悬浮
def picture_start(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Float.objects.filter(nid=id).update(status=1)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)

#悬浮删除
def picture_del(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Float.objects.filter(nid=id).delete()
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


#文章发布
def article_start(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Article.objects.filter(nid=id).update(status=1)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


#文章编辑
def article_edit(request, id):
    if request.method == "POST":
        # print(id)
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        tags = request.POST.get("tags")
        article_content = request.POST.get("article_content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, 'html.parser')

        for tag in bs.find_all():
            if tag.name in ["script"]:
                tag.decompose()
        tag_obj = models.Tag.objects.filter(title=tags).first()
        article_obj = models.Article.objects.filter(nid=id).update(title=title, desc=desc, status=1, content=str(bs),
                                                                   tags_id=tag_obj.pk)
        ret = {}
        ret["msg"] = "提交成功，已发布！！"
        ret["link"] = "/article_list/"
        return JsonResponse(ret)

    else:
        article_obj = models.Article.objects.filter(nid=id).first()
        tags_list=models.Tag.objects.all()
        # print(article_obj.tags)
        tags_obj = []
        for tags in tags_list:
            # print(tags)
            if article_obj.tags == tags:
                tags_obj.insert(0, article_obj.tags)
            else:
                tags_obj.append(tags)

        # print(len(tags_obj), len(tags_list))
        # print(tags_obj)


    return render(request, 'article_edit.html', locals())


#分类列表
def article_class(request):
    tags_list = models.Tag.objects.all()
    count = models.Tag.objects.all().count()

    return render(request, 'article-class.html', locals())

#分类列表
def article_class_add(request):
    if request.method == "POST":
        tags_title = request.POST.get("article_tags")
        is_exist = models.Tag.objects.filter(title=tags_title).first()
        ret = {}
        if is_exist:
            ret["status"] = 0
            ret["msg"] = "此分类已存在！"
        else:
            tags_obj =  models.Tag.objects.create(title=tags_title)
            tags_count = models.Tag.objects.all().count()
            ret["status"] = 1
            ret["tags_ccount"] = models.Tag.objects.all().count()
            ret["nid"] = tags_obj.pk
            ret["tags_title"] = tags_obj.title

        return JsonResponse(ret)


#浮动窗口内容列表
def float_list(request):
    float_obj = models.Float.objects.all().order_by("-create_time")
    count = models.Float.objects.all().count()
    return render(request, 'picture-list.html', locals())



#浮动窗口内容列表
def float_edit(request,id):
    # print(id)
    if request.method == "POST":
        # print(id)
        article_title = request.POST.get("article_title")
        article_desc = request.POST.get("article_desc")
        float_title = request.POST.get("float_title")
        float_desc = request.POST.get("float_desc")
        article_content = request.POST.get("article_content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, 'html.parser')
        for tag in bs.find_all():
            if tag.name in ["script"]:
                tag.decompose()
        models.Float.objects.filter(nid=id).update(a_title=article_title, a_desc=article_desc, status=1, content=str(bs),
                                                    f_title=float_title, f_desc=float_desc)


        ret = {}
        ret["msg"] = "提交成功，已发布！！"
        ret["link"] = "/picture_list/"
        return JsonResponse(ret)

    else:
        float_obj = models.Float.objects.filter(nid=id).first()
    return render(request, 'picture-edit.html', locals())


#添加浮动窗口内容
def float_add(request):
    if request.method == "POST":
        article_title = request.POST.get("article_title")
        article_desc = request.POST.get("article_desc")
        float_title = request.POST.get("float_title")
        float_desc = request.POST.get("float_desc")
        article_content = request.POST.get("article_content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, 'html.parser')
        for tag in bs.find_all():
            if tag.name in ["script"]:
                tag.decompose()
        models.Float.objects.create(a_title=article_title, a_desc=article_desc, status=1, content=str(bs),
                                                    f_title=float_title, f_desc=float_desc)
        ret = {}
        ret["msg"] = "提交成功，已发布！！"
        ret["link"] = "/picture_list/"
        return JsonResponse(ret)

    return render(request, 'picture-add.html')



#招聘会列表
def invite_list(request):
    invite_list = models.Invite.objects.all()
    count = models.Invite.objects.all().count()
    return render(request, "invite-list.html", locals())


#招聘会添加
def add_invite(request):
    # print("hahahahahhahahhaha")
    ret = {}
    if request.method == "POST":
        # print("jejejej")
        name = request.POST.get("name")
        city = request.POST.get("city")
        i_type = request.POST.get("type")
        i_data = request.POST.get("data")
        sponsor = request.POST.get("sponsor")
        content = request.POST.get("content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(content, 'html.parser')
        models.Invite.objects.create(i_name=name, i_data=i_data, i_city=city, i_sponsor=sponsor, i_type=i_type, i_content=str(bs))
        # print(name, city, i_type, i_data, sponsor, content)
        ret["msg"] = "添加成功！"
        ret["link"] = "/invite_list/"
        return JsonResponse(ret)

    return render(request, "invite-add.html", locals())


#招聘会删除
def del_invite(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Invite.objects.filter(id=id).delete()
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)



#招聘会编辑
def invite_edit(request, id):
    ret = {}
    if request.method == "POST":
        name = request.POST.get("name")
        city = request.POST.get("city")
        i_type = request.POST.get("type")
        i_data = request.POST.get("data")
        sponsor = request.POST.get("sponsor")
        content = request.POST.get("content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(content, 'html.parser')
        models.Invite.objects.filter(id=id).update(i_name=name, i_data=i_data, i_city=city, i_sponsor=sponsor, i_type=i_type,
                                     i_content=str(bs))
        # print(name, city, i_type, i_data, sponsor, content)
        ret["msg"] = "修改成功，已发布！"
        ret["link"] = "/invite_list/"
        return JsonResponse(ret)


    else:
        invite_obj = models.Invite.objects.filter(id=id).first()

    return render(request, 'invite-edit.html', locals())


# 宣讲会编辑
def teachin_edit(request, id):
    ret = {}
    if request.method == "POST":
        title = request.POST.get("title")
        city = request.POST.get("city")
        school = request.POST.get("school")
        i_time = request.POST.get("i_time")
        detail = request.POST.get("detail")

        from bs4 import BeautifulSoup
        bs = BeautifulSoup(detail, 'html.parser')

        models.Teachin.objects.filter(id=id).update(x_title=title, x_time=i_time, x_city=city, x_school=school,
                                                    x_detail=str(bs))

        ret["msg"] = "修改成功，已发布！"
        ret["link"] = "/Teachin_list/"
        return JsonResponse(ret)


    else:
        teachin_obj = models.Teachin.objects.filter(id=id).first()

    return render(request, 'teachin_edit.html', locals())


# 宣讲会列表
def Teachin_list(request):
    count = models.Teachin.objects.count()
    teachin_list = models.Teachin.objects.all()
    return render(request, 'Theachin-list.html', locals())


# 宣讲会审核通过
def teachin_start(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        # print("id", id)
        models.Teachin.objects.filter(id=id).update(x_status=1)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


# 宣讲会审核未通过
def teachin_stop(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        print("id", id)
        models.Teachin.objects.filter(id=id).update(x_status=2)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


# 宣讲会删除
def teachin_del(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Teachin.objects.filter(id=id).delete()
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


# 孟浩
# 首页
def m_index(request):
    info = {'status': ''}
    if request.session.get('is_login1', None):
        infor = request.session.get('status', None)
        if infor == 'company':
            info['status'] = 'company'
            number = request.session.get('number', None)
            studentID = '001'
            name = models.Conpanys.objects.filter(c_number=number).values()
            preach = models.Invite.objects.filter().all().order_by('-id')
            company = models.Conpanys.objects.filter().all().order_by('-id')
            teachin = models.Teachin.objects.filter().all().order_by('-id')
            zhaopin = models.Zhaopin.objects.filter().all().order_by('-id')
            article = models.Article.objects.filter().all().order_by('-nid')
            blogroll = models.BlogrollImage.objects.filter().all().order_by('-f_create_time')[:10]
            float = models.Float.objects.filter(status='1').values().order_by('-create_time')[:2]
            news_list = models.NewsArticle.objects.filter(status='1').values().order_by('-create_time')[:5]
            # news_count = models.NewsArticle.objects.filter(status='1').values().count()
            return render(request, 'm_index.html', {
                'number': number,
                'name': name,
                'studentID': studentID,
                'info': info,
                'company': company,
                'preach_infor': preach,
                'teachin': teachin,
                'zhaopin': zhaopin,
                'article': article,
                'float': float,
                'blogroll': blogroll,
                'news_list': news_list,
                # 'news_count': news_count,
            })
        elif infor == 'students':
            info['status'] = 'students'
            snumber = request.session.get('snumber', None)
            sname = models.StudentInfo.objects.filter(snumber=snumber).values()
            studentID = models.StudentInfo.objects.filter(snumber=snumber).values_list('id')[0][0]
            preach = models.Invite.objects.filter().all().order_by('-id')
            company = models.Conpanys.objects.filter().all().order_by('-id')
            teachin = models.Teachin.objects.filter().all().order_by('-id')
            zhaopin = models.Zhaopin.objects.filter().all().order_by('-id')
            article = models.Article.objects.filter().all().order_by('-nid')
            blogroll = models.BlogrollImage.objects.filter().all().order_by('-f_create_time')[:10]
            float = models.Float.objects.filter(status='1').values().order_by('-create_time')[:2]
            news_list = models.NewsArticle.objects.filter(status='1').values().order_by('-create_time')[:5]
            # news_count = models.NewsArticle.objects.filter(status='1').values().count()
            return render(request, 'm_index.html', {
                'snumber': snumber,
                'sname': sname,
                'studentID': studentID,
                'info': info,
                'company': company,
                'preach_infor': preach,
                'teachin': teachin,
                'zhaopin': zhaopin,
                'article': article,
                'float': float,
                'blogroll': blogroll,
                'news_list': news_list,
                # 'news_count': news_count,
            })
    else:
        info['status'] = 'false'
        studentID = '001'
        preach = models.Invite.objects.filter().all().order_by('-id')
        company = models.Conpanys.objects.filter().all().order_by('-id')
        teachin = models.Teachin.objects.filter().all().order_by('-id')
        zhaopin = models.Zhaopin.objects.filter().all().order_by('-id')
        article = models.Article.objects.filter().all().order_by('-nid')
        float = models.Float.objects.all().order_by('-create_time')[:2]
        blogroll = models.BlogrollImage.objects.filter().all().order_by('-f_create_time')[:10]
        news_list = models.NewsArticle.objects.filter(status='1').values().order_by('-create_time')[:5]
        return render(request, 'm_index.html', {
            'info': info,
            'studentID': studentID,
            'company':company,
            'preach_infor':preach,
            'teachin':teachin,
            'zhaopin':zhaopin,
            'article':article,
            'float':float,
            'blogroll': blogroll,
            'news_list': news_list,
        })

#登录
def m_login(request):
    if request.method == "GET":
        # 创建一个HTML
        obj_form = StudentForm()
        return render(request, 'm_login.html', locals())
    else:
        # infor = {'status': 'company'}
        obj_form = StudentForm(request.POST)
        # 是否全部验证成功
        if obj_form.is_valid():
            # 用户提交的数据
            c_number = obj_form.cleaned_data['number']
            c_pwds = obj_form.cleaned_data['pwd']
            c_pwd = hashlib.md5(c_pwds.encode(encoding='UTF-8')).hexdigest()
            # print(c_pwd)
            c_ret = models.Conpanys.objects.filter(c_number=c_number,c_pwd=c_pwd).count()
            check_code = request.POST.get('checkcode')
            # 从session中获取验证码
            session_code = request.session["CheckCode"]

            if c_ret == 0:
                # infor['status'] = 'company'
                obj_form.error_class = "用户账号或密码错误，请重新输入。。。。"
                return render(request, 'm_login.html', {'obj_form': obj_form})
            elif check_code.strip().lower() != session_code.lower():
                # infor['status'] = 'false'
                error_ver = "验证码错误，请重新输入。。。。"
                return render(request, 'm_login.html', {'obj_form': obj_form, 'error_ver': error_ver})
            else:
                request.session['is_login1'] = True
                request.session['number'] = c_number
                request.session['status'] = 'company'
                return redirect('/')
        else:
            return render(request, 'm_login.html', {'obj_form': obj_form})

# 注册
# e10adc3949ba59abbe56e057f20f883e

import hashlib
def m_register(request):
    if request.method == 'GET':
        return render(request, 'm_register.html')
    else:
        info = {'status': True, 'mession': None}
        c_name = request.POST.get('username')
        c_number = request.POST.get('number')
        c_pwds = request.POST.get('password')
        c_pwd = hashlib.md5(c_pwds.encode(encoding='UTF-8')).hexdigest()
        c_linkman = request.POST.get('c_linkman')
        c_phone = request.POST.get('phone')
        c_nature = request.POST.get('c_nature')
        c_city = request.POST.get('c_city')
        c_industry = request.POST.get('c_industry')
        if c_name and c_number and c_pwd and c_linkman and c_phone:
            company_count = models.Conpanys.objects.filter(c_number=c_number).count()
            if company_count:
                info['status'] = False
                info['mession'] = '账号已存在，无需重新注册，请返回登录界面！'
                return render(request, 'register.html', {'info': info})
            else:
                info['status'] = True
                info['mession'] = '注册成功，请返回登录界面！'
                info['link'] = '/m_login/'

                models.Conpanys.objects.filter().create(
                    c_name=c_name,
                    c_number=c_number,
                    c_pwd=c_pwd,
                    c_linkman=c_linkman,
                    c_phone=c_phone,
                    c_nature=c_nature,
                    c_city=c_city,
                    c_industry=c_industry,
                )
        else:
            info['status'] = False
            info['mession'] = '请填写完整的信息！'
        return JsonResponse(info)

# 注册成功
def success(request):
    return render(request,'succes.html')

def m_news_gywm(request):
    return render(request, 'm_news_gywm.html')

# 通知公告
def m_news_tzgg(request):
    t = models.Article.objects.filter(tags_id=1).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_news_tzgg/')
    article = models.Article.objects.filter(tags_id=1).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_news_tzgg.html', {"date_obj": date_obj, "page_obj": page_obj})
# 通知公告文章
def m_news_tzgg_article(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        # for i in article_infor:
        #     print(i)
        return render(request,'m_news_tzgg_article.html',{'article_infor':article_infor})
# 新闻快递
def m_news_xwkd(request):
    t = models.Article.objects.filter(tags_id=2).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_news_xwkd/')
    article = models.Article.objects.filter(tags_id=2).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_news_xwkd.html', {"date_obj": date_obj, "page_obj": page_obj})
# 新闻快递文章
def m_news_xwkd_article(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        # for i in article_infor:
        #     print(i)
        return render(request,'m_news_xwkd_article.html',{'article_infor':article_infor})
# 校园公示
def m_news_xygs(request):
    t = models.Article.objects.filter(tags_id=3).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_news_xygs/')
    article = models.Article.objects.filter(tags_id=3).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_news_xygs.html', {"date_obj": date_obj, "page_obj": page_obj})
# 校园公示文章
def m_news_xygs_article(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_news_xygs_article.html',{'article_infor':article_infor})

# 宣讲会
def m_teachin(request):
    # company_teachin = models.Conpanys.objects.filter().all()
    datas = []
    t = models.Teachin.objects.filter(x_status='1').all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_teachin/')
    teachin_teachin = models.Teachin.objects.filter(x_status='1').values().order_by('-id')
    for teachin in teachin_teachin:
        data = {}
        id = teachin['x_company_id']
        x_id = teachin['id']
        x_time = teachin['x_time']
        x_city = teachin['x_city']
        x_school = teachin['x_school']
        x_company_id = teachin['x_company_id']
        data['x_id'] = x_id
        data['x_time'] = x_time
        data['x_city'] = x_city
        data['x_school'] = x_school
        company_teachin = models.Conpanys.objects.filter(id=id).values()
        for company in company_teachin:
            c_name = company['c_name']
            data['c_name'] = c_name

        datas.append(data)

    date_obj = datas[page_obj.start():page_obj.end()]
    return render(request, 'm_teachin.html', {"date_obj": date_obj, "page_obj": page_obj})
# 宣讲会-内容
def m_teachin_content(request):
    if request.method == "GET":
        pid = request.GET.get('pid')
        teachin_infor = models.Teachin.objects.filter(id=pid).values()
        teachins = []
        for teachin in teachin_infor:
            te={}
            x_time = teachin['x_time']
            x_city = teachin['x_city']
            x_school = teachin['x_school']
            x_detail = teachin['x_detail']
            x_company_id = teachin['x_company_id']
            te['x_time']=x_time
            te['x_city']=x_city
            te['x_school']=x_school
            te['x_detail']=x_detail
            company_infor = models.Conpanys.objects.filter(id=x_company_id).values()
            for company in company_infor:
                c_name = company['c_name']
                c_nature = company['c_nature']
                c_industry = company['c_industry']
                c_scale = company['c_scale']
                c_brief = company['c_brief']
                c_phone = company['c_phone']
                te['c_name'] = c_name
                te['c_nature'] = c_nature
                te['c_industry'] = c_industry
                te['c_scale'] = c_scale
                te['c_brief'] = c_brief
                te['c_phone'] = c_phone
            teachins.append(te)
        return render(request, 'm_teachin_content.html', {'teachins':teachins})
# 招聘公告

def m_campus(request):
    z_infos = []
    t = models.Zhaopin.objects.all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_campus/')
    zhaopin_teachin = models.Zhaopin.objects.filter().values().order_by('-id')
    for zhaopin in zhaopin_teachin:
        z_info = {}
        zid = zhaopin['id']
        z_id = zhaopin['z_company_id']
        z_position = zhaopin['z_position']
        z_data = zhaopin['z_data']
        z_info['zid'] = zid
        z_info['z_position'] = z_position
        z_info['z_data'] = z_data
        companys = models.Conpanys.objects.filter(id=z_id).values()
        for company in companys:
            id = company['id']
            c_name = company['c_name']
            c_city = company['c_city']
            z_info['id'] = id
            z_info['c_name'] = c_name
            z_info['c_city'] = c_city
            students = models.Relationship.objects.filter(company_id=id, remake=zid).values()
            if students:
                for student in students:
                    z_info['studentID'] = student['id']
            z_info['studentID'] = '001'
        z_infos.append(z_info)
    date_obj = z_infos[page_obj.start():page_obj.end()]
    return render(request, 'm_campus.html', {"date_obj": date_obj, "page_obj": page_obj})

# 招聘公告-内容
def m_campus_content(request):
    if request.method == "GET":
        pid = request.GET.get('pid')
        zid = request.GET.get('zid')
        print('zid', zid)
        studentId = request.GET.get('studentsID')
        relations = []
        if studentId == '001':
            relations = []

        # relationcount = models.Relationship.objects.filter(company_id=pid, remake=zid).values().count()
        # if relationcount:
        relations = models.Relationship.objects.filter(company_id=pid, remake=zid).values()

        # relationcount = models.Relationship.objects.filter(company_id=pid, remake=zid).values().count()
        # if relationcount:
        #     relations = models.Relationship.objects.filter(company_id=pid, remake=zid).values()
        company_infor = models.Conpanys.objects.filter(id=pid).values()
        companys=[]
        for company in company_infor:
            cop = {}
            c_id = company['id']
            c_name = company['c_name']
            c_nature = company['c_nature']
            c_industry = company['c_industry']
            c_scale = company['c_scale']
            c_brief = company['c_brief']
            c_city = company['c_city']
            cop['c_id'] = c_id
            cop['c_name'] = c_name
            cop['c_nature'] = c_nature
            cop['c_industry'] = c_industry
            cop['c_scale'] = c_scale
            cop['c_brief'] = c_brief
            cop['c_city'] = c_city
            zhaopin_infor = models.Zhaopin.objects.filter(z_company_id=c_id).values()
            for zhaopin in zhaopin_infor:
                zid = zhaopin['id']
                z_position = zhaopin['z_position']
                z_number = zhaopin['z_number']
                z_salary = zhaopin['z_salary']
                z_data = zhaopin['z_data']
                z_city = zhaopin['z_city']
                z_email = zhaopin['z_email']
                z_detail = zhaopin['z_detail']
                cop['zid'] = zid
                cop['z_position'] = z_position
                cop['z_number'] = z_number
                cop['z_salary'] = z_salary
                cop['z_city'] = z_city
                cop['z_data'] = z_data
                cop['z_email'] = z_email
                cop['z_detail'] = z_detail

            companys.append(cop)


        return render(request, 'm_campus_content.html',
                      {'companys': companys, 'studentId': studentId, 'relations': relations})
# 招聘会
def m_jobfair(request):
    t = models.Invite.objects.all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_jobfair/')
    preach_infor = models.Invite.objects.all().values().order_by('-id')
    date_obj = preach_infor[page_obj.start():page_obj.end()]
    return render(request, 'm_jobfair.html', {"date_obj": date_obj, "page_obj": page_obj})


def exchange(request):
    if request.method == "POST":
        info = {'status': True, 'mession': None}
        studentid = request.POST.get('excahngep')
        companyid = request.POST.get('companyid')
        zid = request.POST.get('zid')
        if studentid != '001' and companyid:
            count = models.Relationship.objects.filter(student_id=studentid, company_id=companyid,
                                                       remake=zid).values().count()
            if count:
                info['status'] = False
                info['mession'] = '您已添加联系，无需重复添加！'
            else:
                models.Relationship.objects.filter().create(
                    student_id=studentid,
                    company_id=companyid,
                    remake=zid,
                )
                info['status'] = True
                info['mession'] = '添加成功'
        else:
            info['status'] = False
            info['mession'] = '您没有权限，请登录'
        ret = json.dumps(info)
        return HttpResponse(ret)


def checkrelation(request):
    if request.method == 'GET':
        studentid = request.GET.get('studentid')
        print('studentid', studentid)
        student = models.StudentInfo.objects.filter(id=studentid).values()
        print('student', student)
        return render(request, 'students/checkrelation.html', {'student': student})

# 招聘会-内容
def m_jobfair_content(request):
    if request.method == "GET":
        zid = request.GET.get('zid')
        invite_infor = models.Invite.objects.filter(id=zid).values()
        company_invite = models.Conpanys.objects.filter().all()
        zhaopin_invite = models.Zhaopin.objects.filter().values()
        # print(zhaopin_invite)
        return render(request,'m_jobfair_content.html',{
            'invite_infor':invite_infor,
            'company_invite':company_invite,
            'zhaopin_invite':zhaopin_invite,
        })
# 岗位
def m_station(request):
    z_infos = []
    t = models.Zhaopin.objects.all().count()
    current_page = request.GET.get('p')
    page_obj = PaginationG(t, current_page, '/m_station/')
    zhaopin_teachin = models.Zhaopin.objects.filter().values().order_by('-id')
    for zhaopin in zhaopin_teachin:
        z_info = {}
        z_id = zhaopin['z_company_id']
        z_position = zhaopin['z_position']
        z_data = zhaopin['z_data']
        z_info['z_position'] = z_position
        z_info['z_data'] = z_data
        companys = models.Conpanys.objects.filter(id=z_id).values()
        for company in companys:
            id = company['id']
            c_name = company['c_name']
            c_city = company['c_city']
            c_industry = company['c_industry']
            z_info['id'] = id
            z_info['c_name'] = c_name
            z_info['c_city'] = c_city
            z_info['c_industry'] = c_industry
        z_infos.append(z_info)

    date_obj = z_infos[page_obj.start():page_obj.end()]
    return render(request, 'm_station.html', {"date_obj": date_obj, "page_obj": page_obj})
# 岗位-内容
def m_station_content(request):
    if request.method == "GET":
        pid = request.GET.get('pid')
        company_infor = models.Conpanys.objects.filter(id=pid).values()
        return render(request,'m_station_content.html',{'company_infor':company_infor})
# 招考公告
def m_invite(request):
    t = models.Article.objects.filter(tags_id=4).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_invite/')
    article = models.Article.objects.filter(tags_id=4).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request,'m_invite.html',locals())
# 招考公告-内容
def m_invite_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_invite_content.html',locals())

# 政策法规
def m_policy(request):
    t = models.Article.objects.filter(tags_id=5).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_policy/')
    article = models.Article.objects.filter(tags_id=5).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_policy.html', {"date_obj": date_obj, "page_obj": page_obj})
# 政策法规-内容
def m_policy_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_policy_content.html',locals())
# 就业指导
def m_obtain(request):
    t = models.Article.objects.filter(tags_id=6).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_obtain/')
    article = models.Article.objects.filter(tags_id=6).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_obtain.html', {"date_obj": date_obj, "page_obj": page_obj})
# 就业指导-内容
def m_obtain_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_obtain_content.html',locals())
# # 创业指导
def m_guide(request):
    t = models.Article.objects.filter(tags_id=7).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_guide/')
    article = models.Article.objects.filter(tags_id=7).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_guide.html', locals())

# 创业指导-内容
def m_guide_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_guide_content.html',locals())
# 创业教育
def m_education(request):
    t = models.Article.objects.filter(tags_id=8).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_education/')
    article = models.Article.objects.filter(tags_id=8).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_education.html', locals())
# 创业教育-内容
def m_education_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_education_content.html',locals())
# 创业实践
def m_practice(request):
    t = models.Article.objects.filter(tags_id=9).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_practice/')
    article = models.Article.objects.filter(tags_id=9).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request,'m_practice.html',locals())
# 创业实践-内容
def m_practice_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_practice_content.html',locals())
# 创业风采
def m_elegant(request):
    t = models.Article.objects.filter(tags_id=10).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_elegant/')
    article = models.Article.objects.filter(tags_id=10).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request,'m_elegant.html',locals())
# 创业风采-内容
def m_elegant_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_elegant_content.html',locals())


# 资料下载
def m_download(request):
    t = models.Article.objects.filter(tags_id=11).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_download/')
    article = models.Article.objects.filter(tags_id=11).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_downloads.html', locals())


# 资料下载-内容
def m_download_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request, 'm_download_content.html', locals())


# 生源状况
def m_enroliment(request):
    t = models.Article.objects.filter(tags_id=12).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_enroliment/')
    article = models.Article.objects.filter(tags_id=12).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_enroliment.html', {"date_obj": date_obj, "page_obj": page_obj})


# 生源状况详情
def m_enroliment_content(request):
    nid = request.GET.get('news_id')
    article_infor = models.Article.objects.filter(nid=nid).values()
    return render(request, 'm_enroliment_content.html', locals())


# 就业质量报告
def m_quality(request):
    t = models.Article.objects.filter(tags_id=13).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_quality/')
    article = models.Article.objects.filter(tags_id=13).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_quality.html', {"date_obj": date_obj, "page_obj": page_obj})


def m_quality_content(request):
    nid = request.GET.get('news_id')
    article_infor = models.Article.objects.filter(nid=nid).values()
    return render(request, 'm_quality_content.html', locals())


# 实习就业
def m_intership(request):
    t = models.Article.objects.filter(tags_id=14).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_intership/')
    article = models.Article.objects.filter(tags_id=14).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_intership.html', {"date_obj": date_obj, "page_obj": page_obj})


# 实习就业详情
def m_intership_content(request):
    nid = request.GET.get('news_id')
    article_infor = models.Article.objects.filter(nid=nid).values()
    return render(request, 'm_intership_content.html', locals())


# 调查统计
def m_survey(request):
    t = models.Article.objects.filter(tags_id=15).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_survey/')
    article = models.Article.objects.filter(tags_id=15).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_survey.html', {"date_obj": date_obj, "page_obj": page_obj})


# 调查统计详情
def m_survey_content(request):
    nid = request.GET.get('news_id')
    article_infor = models.Article.objects.filter(nid=nid).values()
    return render(request, 'm_survey_content.html', locals())


# 校友风采
def m_alumnus(request):
    t = models.Article.objects.filter(tags_id=16).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_alumnus/')
    article = models.Article.objects.filter(tags_id=16).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_alumnus.html', {"date_obj": date_obj, "page_obj": page_obj})


# 校友风采详情
def m_alumnus_content(request):
    nid = request.GET.get('news_id')
    article_infor = models.Article.objects.filter(nid=nid).values()
    return render(request, 'm_alumnus_content.html', locals())


# 创业服务
def m_incubation(request):
    t = models.Article.objects.filter(tags_id=17).all().count()
    current_page = request.GET.get('p')
    page_obj = Pagination(t, current_page, '/m_incubation/')
    article = models.Article.objects.filter(tags_id=17).values().order_by('-nid')
    date_obj = article[page_obj.start():page_obj.end()]
    return render(request, 'm_incubation.html', {"date_obj": date_obj, "page_obj": page_obj})


# 创业服务详情
def m_incubation_content(request):
    nid = request.GET.get('news_id')
    article_infor = models.Article.objects.filter(nid=nid).values()
    return render(request, 'm_incubation_content.html', locals())

# 浮动框
def m_float(request):
    nid = request.GET.get('news')
    float_infor = models.Float.objects.filter(nid=nid).values()

    return render(request,'m_float.html',locals())

#退出登录
def m_logout(request):
    del request.session["is_login1"]
    return redirect('/')


# 文章 文件上传
import os
from jobinfo import settings

def ariticle_upload(request):
    obj = request.FILES.get("upload_img")
    avatar_uid = create_uuid()
    avatar_img_name = avatar_uid + "." + obj.name.split(".")[1]
    flag = ".doc" in obj.name
    if flag:
        path = os.path.join(settings.MEDIA_ROOT, 'add_article_file', avatar_img_name)
    else:
        path = os.path.join(settings.MEDIA_ROOT, 'add_article_img', avatar_img_name)

    with open(path,"wb") as f:
        for line in obj:
            f.write(line)

    print()
    res ={
        "error":0,
        # "url": "/" + path.split("\\")[3] + "/" + path.split("\\")[4] + "/" + avatar_img_name
        "url": "/" + path.split("\\")[4] + "/" + path.split("\\")[5] + "/" + avatar_img_name
    }

    return HttpResponse(json.dumps(res))


# 浮动内容 文件上传
def float_upload(request):
    obj = request.FILES.get("upload_img")
    avatar_uid = create_uuid()
    avatar_img_name = avatar_uid + "." + obj.name.split(".")[1]
    flag = ".doc" in obj.name
    if flag:
        path = os.path.join(settings.MEDIA_ROOT, 'add_float_file', avatar_img_name)
    else:
        path = os.path.join(settings.MEDIA_ROOT, 'add_float_img', avatar_img_name)

    with open(path, "wb") as f:
        for line in obj:
            f.write(line)

    print()
    res = {
        "error": 0,
        # "url": "/" + path.split("\\")[3] + "/" + path.split("\\")[4] + "/" + avatar_img_name
        "url": "/" + path.split("\\")[4] + "/" + path.split("\\")[5] + "/" + avatar_img_name
    }

    return HttpResponse(json.dumps(res))


# 招聘会 文件上传
def invite_upload(request):
    obj = request.FILES.get("upload_img")
    avatar_uid = create_uuid()
    avatar_img_name = avatar_uid + "." + obj.name.split(".")[1]
    flag = ".doc" in obj.name
    if flag:
        path = os.path.join(settings.MEDIA_ROOT, 'add_invite_file', avatar_img_name)
    else:
        path = os.path.join(settings.MEDIA_ROOT, 'add_invite_img', avatar_img_name)

    with open(path, "wb") as f:
        for line in obj:
            f.write(line)

    res = {
        "error": 0,
        # "url": "/" + path.split("\\")[3] + "/" + path.split("\\")[4] + "/" + avatar_img_name
        "url": "/" + path.split("\\")[4] + "/" + path.split("\\")[5] + "/" + avatar_img_name
    }

    return HttpResponse(json.dumps(res))


# 宣讲会 文件上传
def teachin_upload(request):
    obj = request.FILES.get("upload_img")
    avatar_uid = create_uuid()
    avatar_img_name = avatar_uid + "." + obj.name.split(".")[1]
    flag = ".doc" in obj.name
    if flag:
        path = os.path.join(settings.MEDIA_ROOT, 'add_teachin_file', avatar_img_name)
    else:
        path = os.path.join(settings.MEDIA_ROOT, 'add_teachin_img', avatar_img_name)

    with open(path, "wb") as f:
        for line in obj:
            f.write(line)

    print('path', path)

    res = {
        "error": 0,
        # "url": "/" + path.split("\\")[3] + "/" + path.split("\\")[4] + "/" + avatar_img_name
        "url": "/" + path.split("\\")[4] + "/" + path.split("\\")[5] + "/" + avatar_img_name
    }
    print('res', res)
    return HttpResponse(json.dumps(res))


# 友情连接
def blogroll_list(request):
    blogroll_list = models.BlogrollImage.objects.values().order_by('-f_create_time')
    count = models.BlogrollImage.objects.all().count()
    return render(request, 'blogroll_list.html', {'blogroll_list': blogroll_list, 'count': count})


def create_uuid():
    import uuid
    s_uuid = str(uuid.uuid1())
    l_uuid = s_uuid.split('-')
    uid = ''.join(l_uuid)
    return uid


from jobinfo import settings


# 友情链接添加
def blogroll_add(request):
    if request.method == 'GET':
        return render(request, 'blogroll_add.html')

    else:
        ret = {}
        name = request.POST.get('name')
        parse_url = request.POST.get('parse_url')
        img_id = request.POST.get('img_id')
        if name and parse_url and img_id:
            models.BlogrollImage.objects.filter(f_code_img=img_id).update(
                f_name=name,
                f_parse_url=parse_url
            )
            ret["status"] = True
            ret["msg"] = "添加成功！"
            ret["link"] = "/blogroll_list/"
        else:
            ret["status"] = False
            ret["msg"] = "添加失败！"

        return JsonResponse(ret)


# 友情链接上传图片
def upload_img(request):
    if request.method == "POST":
        ret = {}
        id = request.POST.get("id")
        avatar_img = request.FILES.get("avatar")
        avatar_uid = create_uuid()
        ret['img_id'] = avatar_uid
        if avatar_img:
            avatar_img_name = avatar_uid + "." + avatar_img.name.split(".")[1]
            print('avatar_img_name', avatar_img_name)
            path = os.path.join(settings.MEDIA_ROOT, 'slideshow', avatar_img_name)
            with open(path, "wb") as f:
                for line in avatar_img:
                    f.write(line)

            avatar_url = "http://" + request.get_host() + "/media/slideshow/" + avatar_img_name
            models.BlogrollImage.objects.create(
                f_image_url=avatar_url,
                f_code_img=avatar_uid
            )
            ret["status"] = True
            ret["msg"] = "上传成功！"
        else:
            ret["status"] = False
            ret["msg"] = "上传失败！"

        return JsonResponse(ret)


# 友情链接删除
def del_blogroll(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.BlogrollImage.objects.filter(id=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


# 图片新闻
def news_list(request):
    news_list = models.NewsArticle.objects.values().order_by('-create_time')
    count = models.NewsArticle.objects.all().count()
    return render(request, 'news_list.html', {'news_list': news_list, 'count': count})


# 添加新闻
def news_add(request):
    if request.method == 'GET':
        return render(request, 'news_add.html')

    else:
        ret = {}
        img_id = request.POST.get('img_id')
        title = request.POST.get('title')
        article_content = request.POST.get('article_content')

        print('img_id', img_id)
        print('title', title)
        print('article_content', article_content)

        if title and article_content and img_id:
            models.NewsArticle.objects.filter(image_url=img_id).update(
                title=title,
                content=article_content
            )
            ret["status"] = True
            ret["msg"] = "添加成功！"
            ret["link"] = "/news_list/"
        else:
            ret["status"] = False
            ret["msg"] = "添加失败！"

        return JsonResponse(ret)


# 新闻图片上传
def upload_news_img(request):
    if request.method == "POST":
        ret = {}
        avatar_img = request.FILES.get("avatar")
        avatar_uid = create_uuid()
        if avatar_img:
            avatar_img_name = avatar_uid + "." + avatar_img.name.split(".")[1]
            path = os.path.join(settings.MEDIA_ROOT, 'newsimage', avatar_img_name)
            with open(path, "wb") as f:
                for line in avatar_img:
                    f.write(line)

            avatar_url = "http://" + request.get_host() + "/media/newsimage/" + avatar_img_name
            models.NewsArticle.objects.create(
                image_url=avatar_url,
            )
            ret["status"] = True
            ret["msg"] = "上传成功！"
            ret['img_id'] = avatar_url
        else:
            ret["status"] = False
            ret["msg"] = "上传失败！"

        return JsonResponse(ret)


# 新闻图片删除
def del_news(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.NewsArticle.objects.filter(id=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


def news_start(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.NewsArticle.objects.filter(id=id).update(status='1')
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


def news_stop(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.NewsArticle.objects.filter(id=id).update(status='2')
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


def news_upload(request):
    obj = request.FILES.get("upload_img")
    avatar_uid = create_uuid()
    avatar_img_name = avatar_uid + "." + obj.name.split(".")[1]
    flag = ".doc" in obj.name
    if flag:
        path = os.path.join(settings.MEDIA_ROOT, 'add_new_file', avatar_img_name)
    else:
        path = os.path.join(settings.MEDIA_ROOT, 'add_new_img', avatar_img_name)

    with open(path, "wb") as f:
        for line in obj:
            f.write(line)

    print()
    res = {
        "error": 0,
        # "url": "/" + path.split("\\")[3] + "/" + path.split("\\")[4] + "/" + avatar_img_name
        "url": "/" + path.split("\\")[4] + "/" + path.split("\\")[5] + "/" + avatar_img_name
    }

    return HttpResponse(json.dumps(res))


def news_edit(request):
    if request.method == 'POST':
        ret = {}
        img_id = request.POST.get('img_id')
        title = request.POST.get('title')
        article_content = request.POST.get('article_content')

        print('img_id', img_id)
        print('title', title)
        print('article_content', article_content)

        if title and article_content and img_id:
            models.NewsArticle.objects.filter(image_url=img_id).update(
                title=title,
                content=article_content
            )
            ret["status"] = True
            ret["msg"] = "修改成功！"
            ret["link"] = "/news_list/"
        else:
            ret["status"] = False
            ret["msg"] = "修改失败！"

        return JsonResponse(ret)

    else:
        id = request.GET.get('id')
        news_obj = models.NewsArticle.objects.filter(id=id).values()

        return render(request, 'news_edit.html', locals())


def edit_news_img(request):
    if request.method == "POST":
        ret = {}
        id = request.POST.get('id')
        avatar_img = request.FILES.get("avatar")
        avatar_uid = create_uuid()
        if avatar_img:
            avatar_img_name = avatar_uid + "." + avatar_img.name.split(".")[1]
            path = os.path.join(settings.MEDIA_ROOT, 'newsimage', avatar_img_name)
            with open(path, "wb") as f:
                for line in avatar_img:
                    f.write(line)

            avatar_url = "http://" + request.get_host() + "/media/newsimage/" + avatar_img_name
            models.NewsArticle.objects.filter(id=id).update(
                image_url=avatar_url,
            )
            ret["status"] = True
            ret["msg"] = "上传成功！"
            ret['img_id'] = avatar_url
        else:
            ret["status"] = False
            ret["msg"] = "上传失败！"

        return JsonResponse(ret)


def news_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        print(id)
        news = models.NewsArticle.objects.filter(id=id).values()
        return render(request, 'news_detail.html', {'news': news})


# 验证码
def CheckCode(request):
    mstream = io.BytesIO()
    validate_code = Checkcode.create_validate_code()
    img = validate_code[0]
    img.save(mstream, "GIF")
    # 将验证码保存到session
    request.session["CheckCode"] = validate_code[1]
    return HttpResponse(mstream.getvalue())


# 企业管理
def business_administration(request):
    company_list = models.Conpanys.objects.filter().values().order_by('-c_create_time')
    count = models.Conpanys.objects.all().count()
    return render(
        request,
        'business_administration.html',
        {'company_list': company_list, 'count': count})


# 企业详情
def business_detail(request):
    if request.method == "GET":
        id = request.GET.get('companr-id')
        company_list = models.Conpanys.objects.filter(id=id).values()
        return render(request, 'business_detail.html', {'company_list': company_list})
