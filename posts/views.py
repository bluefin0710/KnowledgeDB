#import logging
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.db.models import Count,Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,DeleteView
#from django.views.decorators.http import require_POST
from django.utils import timezone
from django.urls import reverse_lazy
from posts.forms import (
                PostForm, 
                SearchForm, 
                FileFormset, 
                EquipmentForm, 
                SubcategoryForm,
                SpilloverFormset, 
            )
from posts.models import (
                Post,
                Equipment,
                Category,
                Subcategory,
                State,
                Discoverydiv,
                Severity,
                Causediv,
                Checklist_A,
            )

import re

#logger = logging.getLogger('development')

#def index(request):
#    # return HttpResponse("Hello World! このページは投稿のインデックスです。")
#    posts = Post.objects.order_by('-published')
#    return render(request, 'posts/index.html', {'posts': posts})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # 入力された値からUserインスタンスを作成
        if form.is_valid():
            new_user = form.save() # ユーザーインスタンスを保存
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            # フォームの入力値で認証できればユーザーオブジェクト、できなければNoneを返す
            new_user = authenticate(username=input_username, password=input_password)
            # 認証成功時のみ、ユーザーをログインさせる
            if new_user is not None:
                # loginメソッドは、認証ができてなくてもログインさせることができる。→上のauthenticateで認証を実行する
                login(request, new_user)
#                return redirect('posts:index_listview', pk=new_user.pk)
                return redirect('posts:index_listview', )
    else:
        form = UserCreationForm()
    return render(request, 'posts/signup.html', {'form': form})


class Searchlistview(ListView):
    paginate_by = 25
#-- for debug    
#    paginate_by = 1
    template_name = 'posts/search_listview.html'
    model = Post

    def post(self, request, *args, **kwargs):

        form_value = [
                self.request.POST.getlist('Equipment_cb', None),
                self.request.POST.getlist('Category_cb', None),
                self.request.POST.getlist('Subcategory_cb', None),
                self.request.POST.getlist('State_cb', None),
                self.request.POST.getlist('Discoverydiv_cb', None),
                self.request.POST.getlist('Severity_cb', None),
                self.request.POST.getlist('Causediv_cb', None),
                self.request.POST.getlist('Checklist_A_cb', None),
                self.request.POST.get('overview', None),
                self.request.POST.get('content', None),
                self.request.POST.get('cause', None),
                self.request.POST.get('counterplan', None),
                self.request.POST.get('author', None),

#                self.request.POST.get('created_date', None),
#                self.request.POST.get('created_date_e', None),
#                self.request.POST.get('discovery_date', None),
#                self.request.POST.get('discovery_date_e', None),

                self.request.POST.get('created_date_get', None),
                self.request.POST.get('created_date_e_get', None),
                self.request.POST.get('discovery_date_get', None),
                self.request.POST.get('discovery_date_e_get', None),

#                self.request.POST.get('equipment', None),
#                self.request.POST.get('category', None),
#                self.request.POST.get('subcategory', None),
#                self.request.POST.get('state', None),
#                self.request.POST.get('discoverydiv', None),
#                self.request.POST.get('severity', None),
#                self.request.POST.get('causediv', None),
#                self.request.POST.get('checklist', None),
#                self.request.POST.getlist('Equipment_DICT', None),
#                self.request.POST.getlist('Category_DICT', None),
#                self.request.POST.getlist('Subcategory_DICT', None),
#                self.request.POST.getlist('State_DICT', None),
#                self.request.POST.getlist('Discoverydiv_DICT', None),
#                self.request.POST.getlist('Severity_DICT', None),
#                self.request.POST.getlist('Causediv_DICT', None),
#                self.request.POST.getlist('Checklist_A_DICT', None),
                ]
        request.session['form_value'] = form_value

        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
#        equipment = ''
        overview = ''
        content = ''
        cause = ''
        counterplan = ''
        author = ''
        created_date = ''
        created_date_e = ''
        discovery_date = ''
        discovery_date_e = ''
#        category = ''
#        subcategory = ''
#        state = ''
#        discoverydiv = ''
#        severity = ''  
#        causediv = ''  
#        checklist = ''
        Equipment_cb = ''
        Category_cb = ''
        Subcategory_cb = ''
        State_cb = ''
        Discoverydiv_cb = ''
        Severity_cb = ''
        Causediv_cb = ''
        Checklist_A_cb = ''
        Equipment_DICT = dict()
        Category_DICT = dict()
        Subcategory_DICT = dict()
        State_DICT = dict()
        Discoverydiv_DICT = dict()
        Severity_DICT = dict()
        Causediv_DICT = dict()
        Checklist_A_DICT = dict()
    
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']

#            equipment = form_value[0]
#            overview = form_value[1]
#            content = form_value[2]
#            cause = form_value[3]
#            counterplan = form_value[4]
#            category = form_value[5]
#            subcategory = form_value[6]
#            state = form_value[7]
#            discoverydiv = form_value[8]
#            severity = form_value[9]  
#            causediv = form_value[10]  
#            checklist = form_value[11]
#            Equipment_cb = form_value[12]
#            Category_cb = form_value[13]
#            Subcategory_cb = form_value[14]
#            State_cb = form_value[15]
#            Discoverydiv_cb = form_value[16]
#            Severity_cb = form_value[17]
#            Causediv_cb = form_value[18]
#            Checklist_A_cb = form_value[19]

            Equipment_cb = form_value[0]
            Category_cb = form_value[1]
            Subcategory_cb = form_value[2]
            State_cb = form_value[3]
            Discoverydiv_cb = form_value[4]
            Severity_cb = form_value[5]
            Causediv_cb = form_value[6]
            Checklist_A_cb = form_value[7]
            overview = form_value[8]
            content = form_value[9]
            cause = form_value[10]
            counterplan = form_value[11]
            author = form_value[12]

#---- for debug
#            print("get_context_data______form_value--------------")
#            print(form_value[13])
#            print(form_value[14])
#            print(form_value[15])
#            print(form_value[16])
#            print("----------------------------")
#
#            table = str.maketrans('/', '-',)
#            created_date = form_value[13].translate(table)
#            created_date_e = form_value[14].translate(table)
#            discovery_date = form_value[15].translate(table) 
#            discovery_date_e = form_value[16].translate(table)
#
#            print("get_context_data______created_date--------------")
#            print(created_date)
#            print(created_date_e)
#            print(discovery_date)
#            print(discovery_date_e)
#            print("----------------------------")
            
#            print(form_value[14])
#            print(created_date_e)

            created_date = form_value[13]
            created_date_e = form_value[14]
            discovery_date = form_value[15]
            discovery_date_e = form_value[16]

#            print(created_date_e)

#            print("form_value[0]:")
#            print(form_value[0])
#            print("form_value[1]:")
#            print(form_value[1])
#            print("form_value[2]:")
#            print(form_value[2])
#            print("form_value[3]:")
#            print(form_value[3])
#            print("form_value[4]:")
#            print(form_value[4])
#            print("form_value[5]:")
#            print(form_value[5])
#            print("form_value[6]:")
#            print(form_value[6])
#            print("form_value[7]:")
#            print(form_value[7])
#            print("form_value[8]:")
#            print(form_value[8])
#            print("form_value[9]:")
#            print(form_value[9])
#            print("form_value[10]:")
#            print(form_value[10])
#            print("form_value[11]:")
#            print(form_value[11])

#            print("form_value[12]:")
#            print(form_value[12])

#            print("form_value[13]:")
#            print(form_value[13])
#            print("form_value[14]:")
#            print(form_value[14])
#            print("form_value[15]:")
#            print(form_value[15])
#            print("form_value[16]:")
#            print(form_value[16])


            #データをDICT型で構成し、チェックボックスで、チェックしたkey(機種名称)のvalueを１にする
            for B in Equipment.objects.all():
                Equipment_DICT[B.name] = 0
                if Equipment_cb:
                    for A in Equipment_cb:
                        if A == B.name:
                            Equipment_DICT[B.name] = 1
                            break
 
            #データをDICT型で構成し、チェックボックスで、チェックしたkey(大区分)のvalueを１にする
            for B in Category.objects.all():
                Category_DICT[B.name] = 0
                if Category_cb:
                    for A in Category_cb:
                        if A == B.name:
                            Category_DICT[B.name] = 1
                            break

            #データをDICT型で構成し、チェックボックスで、チェックしたkey(小区分)のvalueを１にする
            for B in Subcategory.objects.all():
                Subcategory_DICT[B.name] = 0
                if Subcategory_cb:
                    for A in Subcategory_cb:
                        if A == B.name:
                            Subcategory_DICT[B.name] = 1 
                            break

            #データをDICT型で構成し、チェックボックスで、チェックしたkey(状態区分)のvalueを１にする
            for B in State.objects.all():
                State_DICT[B.name] = 0
                if State_cb:
                    for A in State_cb:
                        if A == B.name:
                            State_DICT[B.name] = 1
                            break
 
            #データをDICT型で構成し、チェックボックスで、チェックしたkey(発見区分)のvalueを１にする
            for B in Discoverydiv.objects.all():
                Discoverydiv_DICT[B.name] = 0
                if Discoverydiv_cb:
                    for A in Discoverydiv_cb:
                        if A == B.name:
                            Discoverydiv_DICT[B.name] = 1
                            break

            #データをDICT型で構成し、チェックボックスで、チェックしたkey(重度)のvalueを１にする
            for B in Severity.objects.all():
                Severity_DICT[B.name] = 0
                if Severity_cb:
                    for A in Severity_cb:
                        if A == B.name:
                            Severity_DICT[B.name] = 1
                            break

            #データをDICT型で構成し、チェックボックスで、チェックしたkey(原因区分)のvalueを１にする
            for B in Causediv.objects.all():
                Causediv_DICT[B.name] = 0
                if Causediv_cb:
                    for A in Causediv_cb:
                        if A == B.name:
                            Causediv_DICT[B.name] = 1
                            break

            #データをDICT型で構成し、チェックボックスで、チェックしたkey(チェックリスト)のvalueを１にする
            for B in Checklist_A.objects.all():
                Checklist_A_DICT[B.name] = 0
                if Checklist_A_cb:
                    for A in Checklist_A_cb:
                        if A == B.name:
                            Checklist_A_DICT[B.name] = 1
                            break


#        for B in Equipment.objects.all():
#            Equipment_DICT[B.name] = 0
#            if self.request.POST.getlist('Equipment_cb', None):
#                for A in self.request.POST.getlist('Equipment_cb', None):
#                    if A == B.name:
#                        Equipment_DICT[B.name] = 1
#                        break

#        for B in Category.objects.all():
#            Category_DICT[B.name] = 0
#            if self.request.POST.getlist('Category_cb', None):
#                for A in self.request.POST.getlist('Category_cb', None):
#                    if A == B.name:
#                        Category_DICT[B.name] = 1
#                        break

#        for B in Subcategory.objects.all():
#            Subcategory_DICT[B.name] = 0
#            if self.request.POST.getlist('Subcategory_cb', None):
#                for A in self.request.POST.getlist('Subcategory_cb', None):
#                    if A == B.name:
#                        Subcategory_DICT[B.name] = 1
#                        break

#        for B in State.objects.all():
#            State_DICT[B.name] = 0
#            if self.request.POST.getlist('State_cb', None):
#                for A in self.request.POST.getlist('State_cb', None):
#                    if A == B.name:
#                        State_DICT[B.name] = 1
#                        break

#        for B in Discoverydiv.objects.all():
#            Discoverydiv_DICT[B.name] = 0
#            if self.request.POST.getlist('Discoverydiv_cb', None):
#                for A in self.request.POST.getlist('Discoverydiv_cb', None):
#                    if A == B.name:
#                        Discoverydiv_DICT[B.name] = 1
#                        break

#        for B in Severity.objects.all():
#            Severity_DICT[B.name] = 0
#            if self.request.POST.getlist('Severity_cb', None):
#                for A in self.request.POST.getlist('Severity_cb', None):
#                    if A == B.name:
#                        Severity_DICT[B.name] = 1
#                        break

#        for B in Causediv.objects.all():
#            Causediv_DICT[B.name] = 0
#            if self.request.POST.getlist('Causediv_cb', None):
#                for A in self.request.POST.getlist('Causediv_cb', None):
#                    if A == B.name:
#                        Causediv_DICT[B.name] = 1
#                        break

#        for B in Checklist_A.objects.all():
#            Checklist_A_DICT[B.name] = 0
#            if self.request.POST.getlist('Checklist_A_cb', None):
#                for A in self.request.POST.getlist('Checklist_A_cb', None):
#                    if A == B.name:
#                        Checklist_A_DICT[B.name] = 1
#                        break



        #searchFormにある要素の初期値の設定 フォームに値がある場合の処理
        default_data = {
#                        'equipment': equipment,  # 機種名称
                        'overview': overview,  # 概要
                        'content': content,  # 内容
                        'cause': cause,  # 原因
                        'counterplan': counterplan,  # 対策
                        'author': author,  # 登録者
                        'created_date': created_date,
                        'created_date_e': created_date_e,
                        'discovery_date': discovery_date, 
                        'discovery_date_e': discovery_date_e, 
#                        'category': category,  # 大分類
#                        'subcategory': subcategory,  # 小分類
#                        'state': state,
#                        'discoverydiv': discoverydiv,
#                        'severity': severity,  
#                        'causediv': causediv,  
 #                       'checklist': checklist,
#                        'Equipment_cb': Equipment_cb,
#                        'Category_cb': Category_cb, 
#                        'Subcategory_cb': Subcategory_cb, 
#                        'State_cb': State_cb,
#                        'Discoverydiv_cb': Discoverydiv_cb, 
#                        'Severity_cb': Severity_cb,
#                        'Causediv_cb': Causediv_cb,
#                        'Checklist_A_cb': Checklist_A_cb,
#                        'Equipment_DICT': Equipment_DICT,
#                        'Category_DICT': Category_DICT,
#                        'Subcategory_DICT': Subcategory_DICT,
                        }

        test_form = SearchForm(initial=default_data) # 検索フォーム

        context['test_form'] = test_form
        
        context['Equipment'] = Equipment.objects.all()
        context['Equipment_cb'] = Equipment_cb
        context['Equipment_DICT'] = Equipment_DICT

        context['Category'] = Category.objects.all()
        context['Category_cb'] = Category_cb
        context['Category_DICT'] = Category_DICT
 
        context['Subcategory'] = Subcategory.objects.all()
        context['Subcategory_cb'] = Subcategory_cb
        context['Subcategory_DICT'] = Subcategory_DICT

        context['State'] = State.objects.all()
        context['State_cb'] = State_cb
        context['State_DICT'] = State_DICT

        context['Discoverydiv'] = Discoverydiv.objects.all()
        context['Discoverydiv_cb'] = Discoverydiv_cb
        context['Discoverydiv_DICT'] = Discoverydiv_DICT

        context['Severity'] = Severity.objects.all()
        context['Severity_cb'] = Severity_cb
        context['Severity_DICT'] = Severity_DICT

        context['Causediv'] = Causediv.objects.all()
        context['Causediv_cb'] = Causediv_cb
        context['Causediv_DICT'] = Causediv_DICT

        context['Checklist_A'] = Checklist_A.objects.all()
        context['Checklist_A_cb'] = Checklist_A_cb 
        context['Checklist_A_DICT'] = Checklist_A_DICT
 
        return context

    def get_queryset(self):

        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
#            equipment = form_value[0]
#            overview = form_value[1]
#            content = form_value[2]
#            cause = form_value[3]
#            counterplan = form_value[4]
#            category = form_value[5]
#            subcategory = form_value[6]
#            state = form_value[7]
#            discoverydiv = form_value[8]
#            severity = form_value[9]  
#            causediv = form_value[10]  
#            checklist = form_value[11]

#            Equipment_cb = form_value[12]
#            Category_cb = form_value[13]
#            Subcategory_cb = form_value[14]
#            State_cb = form_value[15]
#            Discoverydiv_cb = form_value[16]
#            Severity_cb = form_value[17]
#            Causediv_cb = form_value[18]
#            Checklist_A_cb = form_value[19]


            Equipment_cb = form_value[0]
            Category_cb = form_value[1]
            Subcategory_cb = form_value[2]
            State_cb = form_value[3]
            Discoverydiv_cb = form_value[4]
            Severity_cb = form_value[5]
            Causediv_cb = form_value[6]
            Checklist_A_cb = form_value[7]
            overview = form_value[8]
            content = form_value[9]
            cause = form_value[10]
            counterplan = form_value[11]
            author = form_value[12]
#            created_date = form_value[13]
#            created_date_e = form_value[14]
#            discovery_date = form_value[15] 
#            discovery_date_e = form_value[16]
            #日付のフォーマット変換。「/」を「-」にする


#---- for debug
#            print("form_value--------------")
#            print(form_value[13])
#            print(form_value[14])
#            print(form_value[15])
#            print(form_value[16])
#            print("----------------------------")

            table = str.maketrans('/', '-',)
            created_date = form_value[13].translate(table)
            created_date_e = form_value[14].translate(table)
            discovery_date = form_value[15].translate(table) 
            discovery_date_e = form_value[16].translate(table)

 #---- for debug
#           print("created_date--------------")
#            print(created_date)
#            print(created_date_e)
#            print(discovery_date)
#            print(discovery_date_e)
#            print("----------------------------")

            # 検索条件
            condition_equipment = Q()
            condition_category = Q()
            condition_subcategory = Q()
            condition_state = Q()
            condition_discoverydiv = Q()
            condition_severity = Q()  
            condition_causediv = Q()  
            condition_checklist = Q()
            condition_overview = Q()
            condition_content = Q()
            condition_cause = Q()
            condition_counterplan = Q()
            condition_author = Q()
            condition_created_at = Q()
            condition_discoverydate = Q()

#            if len(equipment) != 0 and equipment[0]:
#                condition_equipment = Q(equipment__name__icontains=equipment)
#            if len(category) != 0 and category[0]:
#                condition_category = Q(category__name__icontains=category)
#            if len(subcategory) != 0 and subcategory[0]:
#                condition_subcategory = Q(subcategory__name__icontains=subcategory)
#            if len(state) != 0 and state[0]:
#                condition_state = Q(state__name__icontains=state)
#            if len(discoverydiv) != 0 and discoverydiv[0]:
#                condition_discoverydiv = Q(discoverydiv__icontains=discoverydiv)
#            if len(severity) != 0 and severity[0]:
#                condition_severity = Q(severity__icontains=severity)
#            if len(causediv) != 0 and causediv[0]:
#                condition_causediv = Q(causediv__icontains=causediv)
#            if len(checklist) != 0 and checklist[0]:
#                condition_checklist = Q(checklist__name__icontains=checklist)

            if len(Equipment_cb) != 0 and Equipment_cb[0]:
                count = 0
                for A in Equipment_cb:
                    if count == 0:
                        condition_equipment = Q(equipment__name__icontains=A)
                    else:
                        condition_equipment = condition_equipment | Q(equipment__name__icontains=A)
                    count +=1

            if len(Category_cb) != 0 and Category_cb[0]:
                count = 0
                for A in Category_cb:
                    if count == 0:
                        condition_category = Q(category__name__icontains=A)
                    else:
                        condition_category = condition_category | Q(category__name__icontains=A)
                    count +=1

            if len(Subcategory_cb) != 0 and Subcategory_cb[0]:
                count = 0
                for A in Subcategory_cb:
                    if count == 0:
                        condition_subcategory = Q(subcategory__name__icontains=A)
                    else:
                        condition_subcategory = condition_subcategory | Q(subcategory__name__icontains=A)
                    count +=1

            if len(State_cb) != 0 and State_cb[0]:
                count = 0
                for A in State_cb:
                    if count == 0:
                        condition_state = Q(state__name__icontains=A)
                    else:
                        condition_state = condition_state | Q(state__name__icontains=A)
                    count +=1

            if len(Discoverydiv_cb) != 0 and Discoverydiv_cb[0]:
                count = 0
                for A in Discoverydiv_cb:
                    if count == 0:
                        condition_discoverydiv = Q(discoverydiv__name__icontains=A)
                    else:
                        condition_discoverydiv = condition_discoverydiv | Q(discoverydiv__name__icontains=A)
                    count +=1

            if len(Severity_cb) != 0 and Severity_cb[0]:
                count = 0
                for A in Severity_cb:
                    if count == 0:
                        condition_severity = Q(severity__name__icontains=A)
                    else:
                        condition_severity = condition_severity | Q(severity__name__icontains=A)
                    count +=1

            if len(Causediv_cb) != 0 and Causediv_cb[0]:
                count = 0
                for A in Causediv_cb:
                    if count == 0:
                        condition_causediv = Q(causediv__name__icontains=A)
                    else:
                        condition_causediv = condition_causediv | Q(causediv__name__icontains=A)
                    count +=1

            if len(Checklist_A_cb) != 0 and Checklist_A_cb[0]:
                count = 0
                for A in Checklist_A_cb:
                    if count == 0:
                        condition_checklist = Q(checklist__name__icontains=A)
                    else:
                        condition_checklist = condition_checklist | Q(checklist__name__icontains=A)
                    count +=1

            if len(overview) != 0 and overview[0]:
                word_split = overview.split()
                count = 0
                for A in word_split:
                    if count == 0:
                        condition_overview = Q(overview__icontains=A)
                    else:
                        condition_overview = condition_overview and Q(overview__icontains=A)
                    count +=1
#                print(condition_overview)
                    
            if len(content) != 0 and content[0]:
                word_split = content.split()
                count = 0
                for A in word_split:
                    if count == 0:
                        condition_content = Q(content__icontains=A)
                    else:
                        condition_content = condition_content and Q(content__icontains=A)
                    count +=1
#                print(condition_content)

            if len(cause) != 0 and cause[0]:
                word_split = cause.split()
                count = 0
                for A in word_split:
                    if count == 0:
                        condition_cause = Q(cause__icontains=A)
                    else:
                        condition_cause = condition_cause and Q(cause__icontains=A)
                    count +=1
#                print(condition_cause)

            if len(counterplan) != 0 and counterplan[0]:
                word_split = counterplan.split()
                count = 0
                for A in word_split:
                    if count == 0:
                        condition_counterplan = Q(counterplan__icontains=A)
                    else:
                        condition_counterplan = condition_counterplan and Q(counterplan__icontains=A)
                    count +=1
#                print(condition_counterplan)

            if len(author) != 0 and author[0]:
                word_split = author.split()
                count = 0
                for A in word_split:
                    if count == 0:
                        condition_author = Q(author__username__icontains=A)
                    else:
                        condition_author = condition_author and Q(author__username__icontains=A)
                    count +=1
#                print(condition_author)

            if len(created_date) != 0 and created_date[0]:
                if len(created_date_e) != 0 and created_date_e[0]:
                    condition_created_at = Q(created_at__gte=created_date, created_at__lte=created_date_e)
                else:
                    condition_created_at = Q(created_at__gte=created_date)
            elif len(created_date_e) != 0 and created_date_e[0]:
                    condition_created_at = Q(created_at__lte=created_date_e)
                
#            print(condition_created_at)

            if len(discovery_date) != 0 and discovery_date[0]:
                if len(discovery_date_e) != 0 and discovery_date_e[0]:
                    condition_discoverydate = Q(discoverydate__gte=discovery_date, discoverydate__lte=discovery_date_e)
                else:
                    condition_discoverydate = Q(discoverydate__gte=discovery_date)
            elif len(discovery_date_e) != 0 and discovery_date_e[0]:
                    condition_discoverydate = Q(discoverydate__lte=discovery_date_e)
                
#            print(condition_discoverydate)

            return Post.objects.select_related().filter(
                                        condition_equipment  
                                        & condition_overview  
                                        & condition_content 
                                        & condition_cause 
                                        & condition_counterplan  
                                        & condition_category  
                                        & condition_subcategory 
                                        & condition_state 
                                        & condition_discoverydiv 
                                        & condition_severity 
                                        & condition_causediv 
                                        & condition_checklist
                                        & condition_author
                                        & condition_created_at
                                        & condition_discoverydate
                                        )
        else:
            # 何も返さない
            return Post.objects.none()

class SearchPostView(ListView):
    model = Post
    template_name = 'posts/search_post.html'

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
             Q(equipment__name__icontains=query)
             | Q(category__name__icontains=query)
             | Q(subcategory__name__icontains=query)
             | Q(state__name__icontains=query)
             | Q(discoverydiv__icontains=query)
             | Q(severity__icontains=query) 
             | Q(overview__icontains=query)
             | Q(content__icontains=query)
             | Q(causediv__icontains=query) 
             | Q(cause__icontains=query)
             | Q(counterplan__icontains=query)  
             | Q(checklist__name__icontains=query)
#             | Q(author__user__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

class Indexlistview(ListView):
    model = Post
    template_name = 'posts/index_listview.html'
#    paginate_by = 10
    context_object_name = 'post'

    def get_queryset(self):
#        published_date <= timezone.now()で絞り込まれ、order by published_date descでソート
#        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

#        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-created_at')

        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-updated_at')

#        published_date is Null, order by created_dateとしてリストを取得
#        return Post.objects.filter(published_date__isnull=True).order_by('created_at')
        # 公開フラグがTrueで、作成日順に並び替え
#        return super().get_queryset().filter(is_public=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
#        context['id_sort_asc'] = Post.objects.filter.order_by('pk')
#        context['id_sort_desc'] = Post.objects.filter.order_by('-pk') 
        return context


#def index(request):
#    # return HttpResponse("Hello World! このページは投稿のインデックスです。")
#    post = Post.objects.order_by('-discoverydate')
#    return render(request, 'posts/index.html', {'post': post})

def post_top(request):
    post = Post.objects.order_by('-discoverydate')
    return render(request, 'posts/top.html', {'post': post})
#    return redirect('index')


class Postdetailview(DetailView):
    model = Post
    template_name = 'posts/post_detailview.html'
#    context_object_name = 'post'
#    pk_url_kwarg = 'post_id'

    #-- 「投稿が公開されていない、かつ、ユーザがログインしていない場合は 404 エラーを送出する」
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['checklist_list'] = Checklist_A.objects.all()
##        context['Post_list'] = self.object.Post_set.all()
#        context['Post_list'] = Post.objects
#        return context

#def post_detail(request, post_id):
#    post = get_object_or_404(Post, pk=post_id)
#    return render(request, 'posts/post_detail.html', {'post':post})

#def index_template(request):
#    form = ContactForm()
#    return render(request,'posts/post_detail.html',{
#                'form':form,
#    })


#--2019-12-13 under construction.....
class MypageView(FormView):
    template_name = 'posts/mypage_view.html'
#    form_class = TaskForm

# 印刷・Excel・CSV出力の基底クラス
class BaseReportView(ListView):
    model = Post

    # 選択データの取得
    def get_queryset(self):
#        id_list = self.request.GET['pk'].split('_')
        result = Post.objects.filter(Post.pk)

        return result

# 印刷画面表示
class PrintView(DetailView):
    model = Post
    template_name = 'posts/print2.html'

#    context_object_name = 'post'
#    pk_url_kwarg = 'post_id'

    #-- 「投稿が公開されていない、かつ、ユーザがログインしていない場合は 404 エラーを送出する」
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj



## Excelダウンロード
## django-excel-response
## https://pypi.org/project/django-excel-response/
#class ExcelView(ExcelMixin, BaseReportView):
#
#    # 見出し行を日本語にする
#    def get_queryset(self):
#        header = [['id', '県名', '市町村名', 'ふりがな', '郵便番号', '住所', '電話番号', '自治体コード']]
#        body = [list(entry.values()) for entry in super().get_queryset().values()]
#        return header + body

## CSVダウンロード
#class CsvView(ExcelView):
#    force_csv = True
#

def post_new_org(request):
    form = PostForm(request.POST or None)
    context = {'form': form}
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        formset = FileFormset(request.POST, files=request.FILES, instance=post)
        if formset.is_valid():
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            formset.save()
            return redirect('posts:post_detail', pk=post.pk)
#           return redirect('post_detail', post_id=post.pk)
        else:
            context['formset'] = formset
    else:
#        form = PostForm()
        context['formset'] = FileFormset()

#    return render(request, 'posts/post_edit.html', {'form': form})
    return render(request, 'posts/post_edit.html', context)

def post_edit_org(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    formset = FileFormset(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        form = PostForm(request.POST,request.FILES, instance=post)
#        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
#            image = request.FILES['Image_file1']
#            box = (200, 200, 200, 200)
#            cropped = image.crop(box)
#            post.image = cropped
#            post.Image_file1 = request.FILES['Image_file1']
#            post.Image_file1 = form.cleaned_data['Image_file1']
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
#            form.save()
            form.save_m2m()
            formset.save()
            return redirect('posts:post_detail', pk=post.pk)
#            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm( instance=post )


    context = {
        'form': form,
        'formset': formset,
    }
#    return render(request, 'posts/post_edit.html', {'form': form})
    return render(request, 'posts/post_edit.html', context)

def post_new(request):
    form = PostForm(request.POST or None)
    context = {'form': form}
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        formset = FileFormset(request.POST, files=request.FILES, instance=post)
        spilloverformset = SpilloverFormset(request.POST or None,files=request.FILES or None, instance=post)
        if formset.is_valid()  and spilloverformset.is_valid():
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
#            form.save_m2m()
            form.save()
            formset.save()
            spilloverformset.save()
            return redirect('posts:post_detail', pk=post.pk)
#           return redirect('post_detail', post_id=post.pk)
        else:
#            context['formset'] = formset
            form = PostForm( instance=post )
    else:
#        form = PostForm()
#        context['formset'] = FileFormset()
        context = {
                'form': PostForm(),
                'formset': FileFormset(),
                'spilloverformset': SpilloverFormset(),
#                'formset': formset,
#                'spilloverformset': spilloverformset,
                }

#    return render(request, 'posts/post_edit.html', {'form': form})
    return render(request, 'posts/post_edit.html', context)

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
#    form = PostForm(request.POST or None)
    formset = FileFormset(request.POST or None, files=request.FILES or None, instance=post)
    spilloverformset = SpilloverFormset(request.POST or None, files=request.FILES or None, instance=post)
#--- for debug
#    print("0")
    if request.method == "POST":
#--- for debug
#        print("1")
        post = form.save(commit=False)
        form = PostForm(request.POST or None, instance=post)
        formset = FileFormset(request.POST or None, files=request.FILES or None, instance=post)
        spilloverformset = SpilloverFormset(request.POST or None, files=request.FILES or None, instance=post)

#--- for debug
#        print("-------------post---------------------------------")
#        print(post)
#        print("-------------form---------------------------------")
#        print(form)
#        print("-------------formset------------------------------")
#        print(formset)
#        print("-------------spilloverformset---------------------")
#        print(spilloverformset)
#
#        print("-------------is_valid()---------------------")
#        print(form.is_valid())
#        print(formset.is_valid())
#        print(spilloverformset.is_valid())

        if form.is_valid() and formset.is_valid() and spilloverformset.is_valid():
#--- for debug
#            print("2")
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
#            form.save_m2m()
            form.save()
            formset.save()
            spilloverformset.save()
            return redirect('posts:post_detail', pk=post.pk)
        else:
#--- for debug
#            print("3")
            form = PostForm( instance=post )
#    else:
#--- for debug
#    print("4")

    context = {
            'form': form,
            'formset': formset,
            'spilloverformset': spilloverformset,
            }
 
#--- for debug
#    print("5")
    return render(request, 'posts/post_edit.html', context)


#    print("0")
#    print("--------------------------")
#    print(post)
#    print(form)
#    print(formset)
#    print(spilloverformset)
#
#    print("--------------------------")
#    print(request.method)
#    print(form.is_valid())
#
#    if request.method == "POST" and form.is_valid():
##    if request.method == "POST" and form.is_valid() and formset.is_valid() and spilloverformset.is_valid():
##    if request.method == "POST" and form.is_valid() and formset.is_valid():
#        form = PostForm(request.POST, request.FILES, instance=post)
##        form = PostForm(request.POST)
##        if form.is_valid():
#
##        formset = FileFormset(request.POST, files=request.FILES, instance=post)
##        spilloverformset = SpilloverFormset(request.POST, files=request.FILES, instance=post)
#
#        print("--------------------------")
#         print("1")
##        if form.is_valid() or formset.is_valid() or spilloverformset.is_valid():
#        if formset.is_valid() and spilloverformset.is_valid():
##        if formset.is_valid()  and spilloverformset.is_valid():
#            print("--------------------------")
#            print("2") 
#            post = form.save(commit=False)
##            image = request.FILES['Image_file1']
##            box = (200, 200, 200, 200)
##            cropped = image.crop(box)
##            post.image = cropped
##            post.Image_file1 = request.FILES['Image_file1']
##            post.Image_file1 = form.cleaned_data['Image_file1']
#            post.author = request.user
#            post.published_date = timezone.now()
#            post.save()
##            form.save()
#            form.save_m2m()
#            formset.save()
#            spilloverformset.save()
#            return redirect('posts:post_detail', pk=post.pk)
##            return redirect('post_detail', post_id=post.pk)
#
#    else:
#        form = PostForm( instance=post )
#        print("--------------------------")
#        print("3")
#
#        print("--------------------------")
#        print("4")
#    context = {
#            'form': form,
#            'formset': formset,
#            'spilloverformset': spilloverformset,
#            }
##    return render(request, 'posts/post_edit.html', {'form': form})
#
#    return render(request, 'posts/post_edit.html', context)


#@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
#    formset = FileFormset(request.POST or None, files=request.FILES or None, instance=post)
#    formset.delete()
    post.delete()
    return redirect('posts:index_listview')

#class PostDeleteView(DeleteView):
#    template_name = 'posts/post_confirm_delete.html'
#    model = Post
#    success_url = reverse_lazy('posts:index_listview')
#    items_to_delete = []
#
#    def get_queryset(self):
#        queryset = super(Post, self).get_queryset()
#        self.queryset = queryset.filter(id__in=self.items_to_delete)
#        return self.queryset
#
#    def get_object(self, queryset=None):
#        return self.get_queryset()
#
#    def post(self, request, *args, **kwargs):
#        self.items_to_delete = self.request.POST.getlist('itemsToDelete')
#        if self.request.POST.get("confirm_delete"):
#            # when confirmation page has been displayed and confirm button pressed
#            queryset = self.get_queryset()
#            queryset.delete() # deleting on the queryset is more efficient than on the model object
#            return redirect(self.success_url)
#        elif self.request.POST.get("cancel"):
#            # when confirmation page has been displayed and cancel button pressed
#            return redirect(self.success_url)
#        else:
#            # when data is coming from the form which lists all items
#            return self.get(self, *args, **kwargs)
        
class EquipmentPostView(ListView):
    model = Post
#    context_object_name = 'post'
    template_name = 'posts/equipment_post.html'

    def get_queryset(self):
        equipment_slug = self.kwargs['equipment_slug']
        self.equipment = get_object_or_404(Equipment, slug=equipment_slug)
        qs = super().get_queryset().filter(equipment=self.equipment)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment'] = self.equipment
        return context


class CategoryPostView(ListView):
    model = Post
 #   context_object_name = 'post'
    template_name = 'posts/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class SubcategoryPostView(ListView):
    model = Post
#    context_object_name = 'post'
    template_name = 'posts/subcategory_post.html'

    def get_queryset(self):
        subcategory_slug = self.kwargs['subcategory_slug']
        self.subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        qs = super().get_queryset().filter(subcategory=self.subcategory)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategory'] = self.subcategory
        return context

class StatePostView(ListView):
    model = Post
#    context_object_name = 'post'
    template_name = 'posts/state_post.html'

    def get_queryset(self):
        state_slug = self.kwargs['state_slug']
        self.state = get_object_or_404(State, slug=state_slug)
        qs = super().get_queryset().filter(state=self.state)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state'] = self.state
        return context

class EquipmentListView(ListView):
#    template_name = 'posts/equipment_list.html'
    queryset = Equipment.objects.annotate(
            num_posts=Count('post', filter=Q(post__is_public=True)))

class CategoryListView(ListView):
#    template_name = 'posts/category_list.html'
    queryset = Category.objects.annotate(
            num_posts=Count('post', filter=Q(post__is_public=True)))

class SubcategoryListView(ListView):
    queryset = Subcategory.objects.annotate(
            num_posts=Count('post', filter=Q(post__is_public=True)))

class StateListView(ListView):
    queryset = State.objects.annotate(
            num_posts=Count('post', filter=Q(post__is_public=True)))


class EquipmentCreate(CreateView):
    #"""機種名称の作成"""
    model = Equipment
#    fields = '__all__'
    form_class = EquipmentForm  
    success_url = reverse_lazy('posts:post_edit')

class SubcategoryCreate(CreateView):
    #"""小区分の作成"""
    model = Subcategory
#    fields = '__all__'
    form_class = SubcategoryForm  
    success_url = reverse_lazy('posts:post_edit')

class PopupEquipmentCreate(EquipmentCreate):
    #"""ポップアップでの機種名称追加"""
#    def form_valid(self, form):
    def form_valid(Equipment, form):
#        Equipment.slug = slugify(self.name)
#        Equipment.save()
        equipment = form.save()
        context = {
            'object_name': str(equipment.name),
            'object_pk': equipment.pk,
            'function_name': 'add_equipment'
        }
#        return render(self.request, 'posts/close.html', context)
        return render(Equipment.request, 'posts/close.html', context)

class PopupSubcategoryCreate(SubcategoryCreate):
    #"""ポップアップでの小区分追加"""
#    def form_valid(self, form):
    def form_valid(Subcategory, form):
#        Subcategory.slug = slugify(self.name)
#        Subcategory.save()
        subcategory = form.save()
        context = {
            'object_name': str(subcategory.name),
            'object_pk': subcategory.pk,
            'function_name': 'add_subcategory'
        }
#        return render(self.request, 'posts/close.html', context)
        return render(Subcategory.request, 'posts/close.html', context)


#
# 検索用のキーワードを分割する関数
#

def normalize_query(query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):

    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace(' ',(t[0] or t[1]).strip()) for t in findterms(query_string)]

#
# 検索用のキーワードを分割する関数
#
def get_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects. 
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

##-----------------------------------------------------------------
#class CommentFormView(CreateView):
#    model = Comment
#    form_class = CommentForm
#
#    def form_valid(self, form):
#        comment = form.save(commit=False)
#        post_pk = self.kwargs['pk']
#        comment.post = get_object_or_404(Post, pk=post_pk)
#        comment.save()
#        return redirect('blog:post_detail', pk=post_pk)
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        post_pk = self.kwargs['pk']
#        context['post'] = get_object_or_404(Post, pk=post_pk)
#        return context
#
#@login_required
#def comment_approve(request, pk):
#    comment = get_object_or_404(Comment, pk=pk)
#    comment.approve()
#    return redirect('blog:post_detail', pk=comment.post.pk)
#
#@login_required
#def comment_remove(request, pk):
#    comment = get_object_or_404(Comment, pk=pk)
#    comment.delete()
#    return redirect('blog:post_detail', pk=comment.post.pk)

