from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment , InstgramFeeds, Category
from django.views.generic import ListView,DetailView
from .forms import EmailPostForm, CommentForm, ContactForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

def post_detail(request,slug,year,month,day,tag_slug=None):
    post = get_object_or_404(
        Post,
        status = 'published',
        slug   = slug,
        publish__year = year,
        publish__month = month,
        publish__day = day,
    )
    insta = InstgramFeeds.objects.all()[:6]
    category = Category.objects.all()


    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    #list similar post
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]


    context = {
        'comment_form':comment_form,
        'post':post,
        'comments':comments,
        'new_comment':new_comment,
        'similar_posts':similar_posts,
        'insta':insta,
        'category':category,
    }
    return render(request,'single-blog.html',context)


def post_list(request,tag_slug=None):
    object_list = Post.published.all()
    insta = InstgramFeeds.objects.all()[:6]
    category = Category.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog.html', {'page_obj': page,'posts': posts,'tag': tag,'insta':insta,'category':category,})

def category_detail(request,slug):
    category_list = Category.objects.get(slug=slug)
    insta = InstgramFeeds.objects.all()[:6]
    category = Category.objects.all()

    context = {
        'category':category,
        'insta':insta,
        'category_list':category_list,
    }
    return render(request,'category.html',context)

# class CategoryDetail(DetailView):
#     model = Category
#     context_object_name = 'category'
#     template_name = 'category.html'



def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['message'])
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'post_share.html', {'post': post,'form': form,'sent': sent})


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name    = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email   = form.cleaned_data['email']
            message = form.cleaned_data['message']
            sub = "{} - {}".format(name,subject)
            mes = "{} \n {} \n {} \n {}".format(name,email,subject,message)
            send_mail(sub,mes,['worldofbooks1751998@gmail.com'])
    else:
        form = ContactForm()
    context = {
        'form':form,
    }
    return render(request,'contact.html',context)