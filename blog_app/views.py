from django.shortcuts import render,get_object_or_404, redirect
from django.views import generic
from django.views import View
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, ContactForm
from taggit.models import Tag
from django.db.models import Count

class AboutView(View):
    def get(self, request):
        # <view logic>
        return render(request,'blog_app/about.html')

class ContactView(View):
    def get(self, request):
        # <view logic>
        return render(request,'blog_app/contact.html',{'form':ContactForm()})
    def post(self,request):
        fm = ContactForm(request.POST)
        if fm.is_valid():
            cd = fm.cleaned_data
            subject = f"New Contact from {cd['name']} from blog site"
            message = f"Phone number: {cd['phone']}, email:{cd['email']},{cd['name']}'s message: {cd['message']}"
            send_mail(subject,message,'admin@myblog.com',['admin@myblog.com'])
            return redirect('blog_app:contact_page')
        return render(request,'blog_app/contact.html',{'form':fm})


class PostListView(generic.ListView):
    model = Post
    template_name = 'blog_app/post_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self,*args,**kwargs):
        req = super(PostListView,self).get_queryset(*args,**kwargs)
        self.tag = None
        if self.kwargs.get('tag_slug',None):
            param = self.kwargs.get('tag_slug')
            self.tag = get_object_or_404(Tag,slug=param)
            req = req.filter(tags__in=[self.tag])

        return req
    def get_context_data(self,*args,**kwargs):
        context = super(PostListView,self).get_context_data(*args,**kwargs)
        context['tag'] = self.tag
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.commentform = CommentForm()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        if 'latest' in self.request.path:
            obj = Post.published.all()[0]
        else:
            obj = super().get_object()
        # Record the last accessed date
        return obj
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.commentform = CommentForm(request.POST)
        if self.commentform.is_valid():
            new_comment = self.commentform.save(commit=False)
            new_comment.post = self.object
            new_comment.save()
            self.commentform = CommentForm()
        return super().get(request, *args, **kwargs)
    def get_context_data(self,*args,**kwargs):
        context = super(PostDetailView,self).get_context_data(*args,**kwargs)
        post_tags_ids = self.object.tags.values_list('id',flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=self.object.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')
        context['comments'] = self.object.comments.filter(active=True)
        context['commentform'] = self.commentform
        context['similar_posts'] = similar_posts
        return context
def post_share(request,pk):
    post = get_object_or_404(Post,pk=pk,status='published')
    sent=False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read '{post.title}'"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comment']}"
            send_mail(subject,message,'admin@myblog.com',[cd['to']])
            sent=True
            form = EmailPostForm()
        pass
    elif request.method == 'GET':
        form = EmailPostForm()
    return render(request,'blog_app/share.html',{"post":post,'form':form,'sent':sent})


# Create your views here.
