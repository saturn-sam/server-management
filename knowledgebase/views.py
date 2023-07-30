from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404
from django.core.exceptions import PermissionDenied

from authentication.models import CustomUser
from .models import *
from .forms import *
from taggit.models import Tag
# Create your views here.

@login_required
def home_page(request):
    popular_kb = KBViews.objects.values('kb__title','kb__slug','kb__id').annotate(kb_count=Count('kb')).filter(kb__status='published').order_by('-kb_count')[:5]
    recent_kb= KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).order_by('-created_at')[:4]
    kb_list= KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).order_by('-created_at')
    all_topic= KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).values('topic').annotate(c=Count('topic')).values('topic__id','topic__title','c')
    # tags = Tag.objects.all()
    tags = Tag.objects.all().filter(knowledgebase__status = "published").distinct()
    query = request.GET.get('q')
    if query:
        kb_list = KnowledgeBase.objects.filter(
        Q(status = 'published') &
        Q(delete_status = '0') &
        Q(title__icontains=query) |
        # Q(user_id__username=query) |
        Q(body__icontains=query)|
        Q(topic_id__title=query)
        ).order_by('-created_at')

    query2 = request.GET.get('cat')  
    if query2:
        kb_list = KnowledgeBase.objects.filter(
        Q(status = 'published') &
        Q(delete_status = '0') &
        Q(topic_id__title=query2)
        ).order_by('-created_at')   

    query3 = request.GET.get('author') 
    if query3:
        kb_list = KnowledgeBase.objects.filter(
        Q(status = 'published') &
        Q(delete_status = '0') &
        Q(author_id=query3)
        ).order_by('-created_at')  

    query4 = request.GET.get('tag')  
    if query4:
        kb_list = KnowledgeBase.objects.filter(
        Q(status = 'published') &
        Q(delete_status = '0') &
        Q(tags__slug=query4)
        ).order_by('-created_at') 

    paginator = Paginator(kb_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'popular_kb':popular_kb,
        'recent_kb':recent_kb,
        'tags': tags,
        'page_obj':page_obj,
        'all_topics': all_topic,
        # 'page_range':page_range

    }
    return render(request, 'server/kb/kb_list.html',context)

class KBCreateView(LoginRequiredMixin, CreateView):
    model = KnowledgeBase
    
    form_class = KBCreateForm
    template_name = 'server/kb/add_kb.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = self.request.user
        # unreplied_comments = user.notifications.unread()
        # context["unreplied_comments"] = unreplied_comments
            
        return context 

    def get_success_url(self):
        messages.success(self.request, 'New KB has been added successfully.')
        return reverse('add-kb')

class KBEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = KnowledgeBase
    
    form_class = KBEditForm
    template_name = 'server/kb/edit_kb.html'

    # def get_form_kwargs(self):
    #     kwargs = super(KBEditView, self).get_form_kwargs()
    #     # kwargs['pk'] = self.request.pk
    #     print(self)
    #     return kwargs
    def form_valid(self, form):
        pk = self.kwargs['pk']
        # if not form.instance.author.is_superuser:
        #     form.instance.author = self.request.user
        form.instance.updated_at = timezone.now()
        if form.instance.status == 'published':
            kb = KnowledgeBase.objects.get(pk=pk)
            kb.shared_with.clear()
        return super().form_valid(form)

    def test_func(self):
        kb = self.get_object()
        if self.request.user == kb.author or self.request.user.is_superuser:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context 

    def get_success_url(self):
        messages.success(self.request, 'KB edit submitted successfully.')
        return reverse('my-kb')

class KBTopicAddView(LoginRequiredMixin, CreateView):
    model = KBTopic
    form_class = KBTopicAddForm
    template_name = 'server/kb/add_kb_topic.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context 

    def get_success_url(self):
        messages.success(self.request, 'New KB Topic has been added successfully.')
        return reverse('add-kb-topic')

@login_required
def KBDetailView(request, pk, slug):
    status=""
    message=""
    kb=get_object_or_404(KnowledgeBase, id=pk)

    if kb.status == 'draft' and kb.author != request.user and not request.user.is_superuser:
        raise Http404("Selected Knowledge not found.")
    elif kb.status == 'protected' and not kb.shared_with.filter(id=request.user.id) and kb.author != request.user and not request.user.is_superuser:
        # if not kb.shared_with.filter(id=request.user.id) and kb.author != request.user :
        # raise Http404("Selected Knowledge not found or you have no permission to view.")
        raise PermissionDenied("You have no permission to view this KB.")
    tags = Tag.objects.all().filter(knowledgebase__status = "published").distinct()
    recent_kb= KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).order_by('-created_at')[:4]
    all_topic=KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).values('topic').annotate(c=Count('topic')).values('topic__id','topic__title','c')
    comments = Comment.objects.filter(kb=kb, reply=None, active=True).order_by('-id')
    popular_kb = KBViews.objects.values('kb__title','kb__slug','kb__id').annotate(kb_count=Count('kb')).filter(kb__status='published').order_by('-kb_count')[:5]

    contribution = KnowledgeBase.objects.filter(status='published', author=kb.author).count
    
    like_count = kb.likes.count()
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    # PostViews.objects.get_or_create(IPAddres=get_client_ip(request), post=post)
    KBViews.objects.create(IPAddres=get_client_ip(request), kb=kb, created=timezone.now())

    if like_count > 1:
        like_count2 = like_count-1
    else:
        like_count2 = like_count           

    # notify_id = request.GET.get('notify_id')
    # if notify_id:
    #     request.user.notifications.get(id=notify_id).mark_as_read()

    if kb.likes.filter(id=request.user.id).exists():
        liker = ['you']
    else:
        liker = kb.likes.order_by('id')[:1]
    if request.method == 'POST':
        if request.user.is_authenticated:
            content=request.POST.get('comment')
            reply_id=request.POST.get('comment_id')
            comment_qs=None
            if reply_id:
                comment_qs=Comment.objects.get(id=reply_id)
            if content:
                if request.user.is_superuser:
                    savepost=Comment(content=content, kb=kb, username=request.user, reply=comment_qs, active=1)
                else:
                    savepost=Comment(content=content, kb=kb, username=request.user, reply=comment_qs)
                savepost.save()
                # return JsonResponse({"status":"success","message": f"You have commented successfully!"}) 
                # messages.success(request, 'You have commented successfully!.')
                status="success"
                message="Comment posted successfully!"
            else:
                status="error"
                message="Please fill the required field!"
        else:
            status="error"
            message="Please login to comment!!"
            # return JsonResponse({"status":"error","message": f"Please login to comment!"})
           
    commentreply = Comment.objects.filter(kb=kb, active=True).count()
    is_liked=False
    if kb.likes.filter(id=request.user.id).exists():
        is_liked=True
    context={
        'recent_kb':recent_kb,
        'popular_kb':popular_kb,
        'kb': kb,
        'all_topic': all_topic,
        'comments': comments,
        'commentreply': commentreply,
        'is_liked': is_liked,
        'like_count': like_count,
        'like_count2': like_count2,
        'liker': liker,
        'tags':tags,
        'contribution':contribution,
    }
    context2={
        'comments': comments,
        'commentreply': commentreply,
        'status':status,
        'message':message
    }
    if request.is_ajax():
        html = render_to_string('server/kb/comment_section.html', context2, request=request)
        return JsonResponse({"form":html, "status":status, "message":message})

    return render(request, 'server/kb/kb_detail.html',context)

@login_required
def kbpreview(request, pk, slug):
    kb=get_object_or_404(KnowledgeBase, id=pk)

    if kb.status == 'draft' and kb.author != request.user and not request.user.is_superuser:
        raise Http404("Selected Knowledge not found.")
    elif kb.status == 'protected' and not kb.shared_with.filter(id=request.user.id) and kb.author != request.user and not request.user.is_superuser:
        # if not kb.shared_with.filter(id=request.user.id) and kb.author != request.user :
        # raise Http404("Selected Knowledge not found or you have no permission to view.")
        raise PermissionDenied("You have no permission to view this KB.")

    tags = Tag.objects.all().filter(knowledgebase__status = "published").distinct()
    recent_kb= KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).order_by('-created_at')[:4]
    all_topic=KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).values('topic').annotate(c=Count('topic')).values('topic__id','topic__title','c')
    
    popular_kb = KBViews.objects.values('kb__title','kb__slug','kb__id').annotate(kb_count=Count('kb')).filter(kb__status='published').order_by('-kb_count')[:5]

    contribution = KnowledgeBase.objects.filter(status='published', author=kb.author).count

    context={
        'recent_kb':recent_kb,
        'popular_kb':popular_kb,
        'kb': kb,
        'all_topic': all_topic,
        'tags':tags,
        'contribution':contribution,
    }

    return render(request, 'server/kb/kb_preview.html',context)

@login_required
def like_post(request):
    #post=get_object_or_404(Post, id=request.POST.get('post_id'))
    try:
        kb = get_object_or_404(KnowledgeBase, ~Q(status='draft'), id=request.POST.get('id'))
    except:
        return JsonResponse({"status":"error","message": f"You cant share this KB. This is not Protected."})

    is_liked=False
    if kb.likes.filter(id=request.user.id).exists():
        kb.likes.remove(request.user)
        is_liked=False
    else:
        kb.likes.add(request.user)
        is_liked=True
    
    like_count = kb.likes.count()
    if like_count > 1:
        like_count2 = like_count-1
    else:
        like_count2 = like_count           


    if kb.likes.filter(id=request.user.id).exists():
        liker = ['you']
    else:
        liker = kb.likes.order_by('id')[:1]
    
    context={
        'kb': kb,
        #'all_topic': all_topic,
        #'comments': comments,
        #'commentreply': commentreply,
        'is_liked': is_liked,
        'like_count': like_count,
        'like_count2': like_count2,
        'liker': liker
    }
    #return HttpResponseRedirect(reverse('post-details', args=(post.id,post.slug,)))
    if request.is_ajax():
        html = render_to_string('server/kb/like_section.html', context, request=request)
        return JsonResponse({'form':html})

@login_required
def my_kb(request):
    kb = KnowledgeBase.objects.filter( delete_status = '0', author=request.user ).order_by('-created_at')
    tags = Tag.objects.all().filter(knowledgebase__status = "published").distinct()
    recent_kb= KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).order_by('-created_at')[:4]
    all_topics=KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).values('topic').annotate(c=Count('topic')).values('topic__id','topic__title','c')
    popular_kb = KBViews.objects.values('kb__title','kb__slug','kb__id').annotate(kb_count=Count('kb')).filter(kb__status='published').order_by('-kb_count')[:5]
    all_users = CustomUser.objects.filter(~Q(email=request.user.email),is_active=True)
    # all_users = all_users.exclude(request.user)

    print(all_users)

    context = {
        'kbs':kb,
        'recent_kb':recent_kb,
        'popular_kb':popular_kb,
        'tags':tags,
        'all_topics':all_topics,
        'all_users':all_users,
    }

    return render(request, 'server/kb/my_kb.html',context)

@login_required
def all_kb(request):
    kb = KnowledgeBase.objects.all().order_by('-created_at')
    tags = Tag.objects.all().filter(knowledgebase__status = "published").distinct()
    recent_kb= KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).order_by('-created_at')[:4]
    all_topics=KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).values('topic').annotate(c=Count('topic')).values('topic__id','topic__title','c')
    popular_kb = KBViews.objects.values('kb__title','kb__slug','kb__id').annotate(kb_count=Count('kb')).filter(kb__status='published').order_by('-kb_count')[:5]
    all_users = CustomUser.objects.filter(~Q(email=request.user.email),is_active=True)
    # all_users = all_users.exclude(request.user)

    print(all_users)

    context = {
        'kbs':kb,
        'recent_kb':recent_kb,
        'popular_kb':popular_kb,
        'tags':tags,
        'all_topics':all_topics,
        'all_users':all_users,
    }

    return render(request, 'server/kb/all_kb.html',context)

@login_required
def share_kb(request):
    if request.method == 'POST':
        if request.POST["share-user"] != "":
            share_user = request.POST["share-user"]
            user_instance = CustomUser.objects.get(pk=share_user)
            kb = get_object_or_404(KnowledgeBase, pk=request.POST["kb-id"])
            if user_instance not in kb.shared_with.all():
                # kb.shared_with.add(share_user)
                kb.shared_with.add(user_instance)
                kb.save()
                # print(kb.users_except_shared())
                return JsonResponse({"status":"success","message": f' KB "{kb.title}" has been shared with "{user_instance.get_full_name()}"'})
            else:
                return JsonResponse({"status":"error","message": f' KB "{kb.title}" already shared with "{user_instance.get_full_name()}"'})
        else:
            return JsonResponse({"status":"error","message": f"Please Select at least one User"})

@login_required
def unshare_kb(request):
    if request.method == 'POST':
        if request.POST.getlist('unshare_user[]') != []:
            unshare_users = request.POST.getlist('unshare_user[]')
            kb_id = request.POST["kb_id"]
            try:
                kb = get_object_or_404(KnowledgeBase, Q(status='protected'), id=kb_id)
            except:
                return JsonResponse({"status":"error","message": f"You cant share this KB. This is not Protected."})

            for unshare_user in unshare_users:
                if kb.shared_with.filter(id=unshare_user).exists():
                    kb.shared_with.remove(unshare_user)
            return JsonResponse({"status":"success","message": f"Successfully unshare to selected user"})
        else:
            return JsonResponse({"status":"error","message": f"Please Select one User"})

@login_required
def shared_with_me(request):
    popular_kb = KBViews.objects.values('kb__title','kb__slug','kb__id').annotate(kb_count=Count('kb')).filter(kb__status='published').order_by('-kb_count')[:5]
    recent_kb= KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).order_by('-created_at')[:4]
    kb_list= KnowledgeBase.objects.filter( delete_status = '0', status = 'protected').exclude(~Q(shared_with=request.user)).order_by('-created_at')
    all_topic= KnowledgeBase.objects.filter( delete_status = '0', status = 'published' ).values('topic').annotate(c=Count('topic')).values('topic__id','topic__title','c')
    # tags = Tag.objects.all()
    tags = Tag.objects.all().filter(knowledgebase__status = "published").distinct()

    paginator = Paginator(kb_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'popular_kb':popular_kb,
        'recent_kb':recent_kb,
        'tags': tags,
        'page_obj':page_obj,
        'all_topics': all_topic,
        # 'page_range':page_range

    }
    return render(request, 'server/kb/shared_with_me_kb_list.html',context)