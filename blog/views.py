from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm, EmailPostForm




class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

#class PostDetail(generic.DetailView):
#    model = Post
#    template_name = 'post_detail.html'

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def post_share(request, post_id):
    template_name = 'share.html'
    #Retrieve post by id 
    post = get_object_or_404(Post, id=post_id, status=1)
    sent = False

    if request.method =='POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            #..send email...
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'sagargohil564@gmail.com',
            [cd['to']])
            sent = True
            
    else:
        form = EmailPostForm()
    return render(request, template_name, {'post':post, 'form':form})

def about(request):
    return render(request, 'about.html')

#   return HttpResponse("this is about page")

def policy(request):
    return render(request, 'policy.html')

#   return HttpResponse("this is services page")

def contact(request):
    return render(request, 'contact.html')

#   return HttpResponse("this is services page")


