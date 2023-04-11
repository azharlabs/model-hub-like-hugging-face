from taggit.models import Tag

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.generic import CreateView,UpdateView,DeleteView, DetailView, View
from django.utils.text import slugify
from django.urls import reverse,reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import F

from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from tracking_analyzer.models import Tracker

from accounts.models import Profile
from .models import Post, Comment, Vote
from .forms import PostForm, CommentForm

from analytics.signals import object_viewed_signal



class NewBlogView(CreateView, LoginRequiredMixin):
    form_class = PostForm
    template_name = 'blog/post_add.html'
    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        blog_obj.slug = slugify(blog_obj.title)
        
        # print(blog_obj.tags.all)
        # for tag in self.request.POST.get('tags').replace(' ', '').split(','):
        #     blog_obj.tags.add(tag)
        
        print("tags", blog_obj)
        
        messages.success(self.request, f'Blog post: {blog_obj.title} saved.' )
        blog_obj.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('blog:post_add'))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
       
        return context

class UpdateBlogPostView(UpdateView, LoginRequiredMixin):
    form_class = PostForm
    template_name = 'blog/post_update.html'
    success_url = '/blog/'
    model = Post
    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        blog_obj.slug = slugify(blog_obj.title)
        
        # print(blog_obj.tags.all)
        # for tag in self.request.POST.get('tags').replace(' ', '').split(','):
        #     blog_obj.tags.add(tag)
        
        print("tags", blog_obj)
        
        messages.success(self.request, f'Blog post: {blog_obj.title} saved.' )
        blog_obj.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('blog:post_list'))


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
       
        return context


class DeletePost(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
       
        return context



class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        post=get_object_or_404(Post,slug=slug,status='published')
        object_viewed_signal.send(post.__class__, instance=post, request=request)
        Tracker.objects.create_from_request(request, post)

        fav = bool


        if post.favourites.filter(id=request.user.id).exists():
            fav = True

        count_hit = True

        context = {}

        comments =None# post.comments.filter(active=True)
        new_comment = None
    
       
            # List of similar posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:6]
        #ads
        
        # hitcount logic
        hit_count = get_hitcount_model().objects.get_for_object(post)
        hits = hit_count.hits
        hitcontext = context['hitcount'] = {'pk': hit_count.pk}
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
        if hit_count_response.hit_counted:
            hits = hits + 1
            hitcontext['hit_counted'] = hit_count_response.hit_counted
            hitcontext['hit_message'] = hit_count_response.hit_message
            hitcontext['total_hits'] = hits

        

        context = {
            'post':post,
            'comments': comments,
            # 'comment_form':comment_form,
            'similar_posts':similar_posts,
            'fav':fav,
            # 'genad':genad,
            }
        return render(request, 'blog/detail.html',context)    

    
    def post(self, request, slug, *args, **kwargs):
        post=get_object_or_404(Post,slug=slug,status='published')

        fav = bool


        if post.favourites.filter(id=request.user.id).exists():
            fav = True

        count_hit = True

        context = {}

        comments = post.comments.filter(active=True)
        new_comment = None
        comment_form = CommentForm(request.POST)
        print("s")
        if request.method == "POST" :
            print("==================body=================")
            print(request.POST.get('body'))
            # A comment was posted
            comment_form = CommentForm(request.POST)
            
            # comment_form.name = 
            if comment_form.is_valid():
                body = request.POST.get('body')

                print("==================body=================")
                print(body)
                name = request.user
                email = request.user.email

                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.post = post
                # new_comment.name = request.user
                # new_comment.email = request.user.email
                # Save the comment to the database
                new_comment.save()

              
                # redirect to same page and focus on that comment
                return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
            else:
                comment_form = CommentForm()
            # List of similar posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:6]
        #ads
        genad = GeneralAd.objects.all()
        # hitcount logic
        hit_count = get_hitcount_model().objects.get_for_object(post)
        hits = hit_count.hits
        hitcontext = context['hitcount'] = {'pk': hit_count.pk}
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
        if hit_count_response.hit_counted:
            hits = hits + 1
            hitcontext['hit_counted'] = hit_count_response.hit_counted
            hitcontext['hit_message'] = hit_count_response.hit_message
            hitcontext['total_hits'] = hits

        

        context = {
            'post':post,
            'comments': comments,
            'comment_form':comment_form,
            'similar_posts':similar_posts,
            'fav':fav,
            'genad':genad,
            }
        return render(request, 'blog/detail.html',context)

       



def post_list(request, tag_slug=None):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.published.all().order_by('?')
    profile_user = Profile.objects.all()[:6]
    profile = get_object_or_404(Profile, user=request.user)

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        print(tag)
        # posts = Post.objects.filter(tags__in=["ddd"])
        posts = posts.filter(tags__in=[tag])

        print("posts", posts)

    query = request.GET.get("q")
    if query:
        posts=Post.published.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()

    followings = []
    suggestions = []
    if request.user.is_authenticated:
        followings = Profile.objects.filter(followers=request.user).values_list('pk', flat=True)
        profile_user = Profile.objects.exclude(pk__in=followings).exclude(pk=profile.pk).order_by("?")[:6]



    paginator = Paginator(posts, 2) 

    tags_common = Post.tags.most_common()[:10]

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts':posts,
        'pages':page,
        'tag':tag,
        'profile_user':profile_user,
        'followings':followings,
        'tags_common':tags_common,
        }
    return render(request,'blog/post_list.html',context)



@login_required
def thumbs(request):

    if request.POST.get('action') == 'thumbs':

        print("request post",request.POST)

        id = int(request.POST.get('postid'))
        button = request.POST.get('button')
        update = Post.objects.get(id=id)

        if update.thumbs.filter(id=request.user.id).exists():

            # Get the users current vote (True/False)
            q = Vote.objects.get(
                Q(post_id=id) & Q(user_id=request.user.id))
            evote = q.vote

            if evote == True:

                # Now we need action based upon what button pressed

                if button == 'thumbsup':

                    update.thumbsup = F('thumbsup') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

                if button == 'thumbsdown':

                    # Change vote in Post
                    update.thumbsup = F('thumbsup') - 1
                    update.thumbsdown = F('thumbsdown') + 1
                    update.save()

                    # Update Vote

                    q.vote = False
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

            pass

            if evote == False:

                if button == 'thumbsup':

                    # Change vote in Post
                    update.thumbsup = F('thumbsup') + 1
                    update.thumbsdown = F('thumbsdown') - 1
                    update.save()

                    # Update Vote

                    q.vote = True
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

                if button == 'thumbsdown':

                    update.thumbsdown = F('thumbsdown') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

        else:        # New selection

            if button == 'thumbsup':
                update.thumbsup = F('thumbsup') + 1
                update.thumbs.add(request.user)
              
                update.save()
                # Add new vote
                new = Vote(post_id=id, user_id=request.user.id, vote=True)
                new.save()
            else:
                # Add vote down
                update.thumbsdown = F('thumbsdown') + 1
                update.thumbs.add(request.user)
                update.save()
                # Add new vote
                new = Vote(post_id=id, user_id=request.user.id, vote=False)
                new.save()

            # Return updated votes
            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown

            return JsonResponse({'up': up, 'down': down})

    pass

# handling reply, reply view
def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            reply = form.save(commit=False)
    
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
           
            reply.save()

            return redirect(post_url+'#'+str(reply.id))

    return redirect("/")

