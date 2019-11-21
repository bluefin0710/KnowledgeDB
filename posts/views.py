#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.db.models import Count,Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,DeleteView
#from django.views.decorators.http import require_POST
from django.utils import timezone
from django.urls import reverse_lazy
from posts.forms import PostForm, SearchForm, FileFormset, EquipmentForm, SubcategoryForm
from posts.models import Post,Equipment,Category,Subcategory,State
#from posts.models import Checklist_A

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
    template_name = 'posts/search_listview.html'
    model = Post

    def post(self, request, *args, **kwargs):

        form_value = [
                self.request.POST.get('equipment', None),
                self.request.POST.get('overview', None),
                self.request.POST.get('content', None),
                self.request.POST.get('cause', None),
                self.request.POST.get('counterplan', None),
                self.request.POST.get('category', None),
                self.request.POST.get('subcategory', None),
                ]
        request.session['form_value'] = form_value

        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        equipment = ''
        overview = ''
        content = ''
        cause = ''
        counterplan = ''
        category = ''
        subcategory = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            equipment = form_value[0]
            overview = form_value[1]
            content = form_value[2]
            cause = form_value[3]
            counterplan = form_value[4]
            category = form_value[5]
            subcategory = form_value[6]

        default_data = {'equipment': equipment,  # タイトル
                        'overview': overview,  # 概要
                        'content': content,  # 内容
                        'cause': cause,  # 原因
                        'counterplan': counterplan,  # 対策
                        'category': category,  # 大分類
                        'subcategory': subcategory,  # 小分類
                        }

        test_form = SearchForm(initial=default_data) # 検索フォーム
        context['test_form'] = test_form

        return context

    def get_queryset(self):

        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            equipment = form_value[0]
            overview = form_value[1]
            content = form_value[2]
            cause = form_value[3]
            counterplan = form_value[4]
            category = form_value[5]
            subcategory = form_value[6]

            # 検索条件
            condition_equipment = Q()
            condition_overview = Q()
            condition_content = Q()
            condition_cause = Q()
            condition_counterplan = Q()
            condition_category = Q()
            condition_subcategory = Q()

            if len(equipment) != 0 and equipment[0]:
                condition_equipment = Q(equipment__contains=equipment)
            if len(overview) != 0 and overview[0]:
                condition_overview = Q(overview__contains=overview)
            if len(content) != 0 and content[0]:
                condition_content = Q(content__contains=content)
            if len(cause) != 0 and cause[0]:
                condition_cause = Q(cause__contains=cause)
            if len(counterplan) != 0 and counterplan[0]:
                condition_counterplan = Q(counterplan__contains=counterplan)
#            if len(category) != 0 and category[0]:
            condition_category = Q(category__contains=category)
#            if len(subcategory) != 0 and subcategory[0]:
            condition_subcategory = Q(subcategory__contains=subcategory)

            return Post.objects.select_related().filter(condition_equipment & condition_overview & condition_content & condition_cause & condition_counterplan)
#            return Post.objects.select_related().filter(condition_equipment & condition_overview & condition_content & condition_cause & condition_counterplan & condition_category & condition_subcategory)
        else:
            # 何も返さない
            return Post.objects.none()

class SearchPostView(ListView):
    model = Post
    template_name = 'posts/search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(equipment__name__icontains=query) |
            Q(overview__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(subcategory__name__icontains=query) | 
            Q(cause__icontains=query) |
            Q(couunterplan__icontains=query)
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

def post_new(request):
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

def post_edit(request, pk):
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

