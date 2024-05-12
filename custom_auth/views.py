from django.shortcuts import render,redirect
from django.views import View
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from codingmantra.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages

# Create your views here.

# SignIn View
class SignIn(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return render(request,'sign-in.html')
    def post(self,request):
        form = SignInForm(request.POST)
        error_message = ""
        if form.is_valid():
            email            =   form.cleaned_data.get('email')
            password         =   form.cleaned_data.get('password')
            user             =   authenticate(request,email=email,password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "welcome to dashboard")
                return redirect('/dashboard/')
            else:
                error_message =  "Invalid email or password. Please try again."
        return render(request,'sign-in.html',{'form':form,'error_message':error_message})
    

# SignUp View
class SignUp(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return render(request,'sign-up.html')
    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "account created successfully")
            return redirect('/')
        return render(request, 'sign-up.html', {'form': form})
    
# Logout View
class LogoutView(View):
    @method_decorator(login_required, name='dispatch')
    def get(self,request):
        logout(request)
        messages.success(request, "logout successfully")
        return redirect('/')


# Dashboard View
class Dashboard(View):
    @method_decorator(login_required, name='dispatch')
    def get(self,request):
        return render(request,'dashboard.html')
    def post(self,request):
        form = PostBlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "blog posted successfully")
            return redirect('/all-blog/')  # Redirect to post detail page
        return render(request, 'dashboard.html', {'form': form})
    
        
# BlogList View
class BlogList(View):
    @method_decorator(login_required, name='dispatch')
    def get(self,request):
        q = request.GET.get('search')  # Get the search query from the request
        if q:
            all_list_q = PostBlog.objects.filter(place_name__icontains=q).count()
            if all_list_q:
                all_list = PostBlog.objects.filter(place_name__icontains=q)
            else:
                 all_list = PostBlog.objects.order_by('-id')
        else:
            all_list = PostBlog.objects.order_by('-id')
        per_page = 5
        paginator = Paginator(all_list, per_page)
        page_number = request.GET.get('page')
        try:
            all_list = paginator.page(page_number)
        except PageNotAnInteger:
            all_list = paginator.page(1)
        except EmptyPage:
            all_list = paginator.page(paginator.num_pages)
        return render(request,'blog-list.html',{'all_list':all_list,'q': q})


# YourBlog
class YourBlog(View):
    @method_decorator(login_required, name='dispatch')
    def get(self,request):
        q = request.GET.get('search')  # Get the search query from the request
        if q:
            all_list_q = PostBlog.objects.filter(place_name__icontains=q,user_id = request.user.id).count()
            if all_list_q:
                all_list = PostBlog.objects.filter(place_name__icontains=q,user_id = request.user.id).order_by('-id')
            else:
                 all_list = PostBlog.objects.filtere(user_id = request.user.id).order_by('-id')
        else:
            all_list = PostBlog.objects.filter(user_id = request.user.id).order_by('-id')
        per_page = 5
        paginator = Paginator(all_list, per_page)
        page_number = request.GET.get('page')
        try:
            all_list = paginator.page(page_number)
        except PageNotAnInteger:
            all_list = paginator.page(1)
        except EmptyPage:
            all_list = paginator.page(paginator.num_pages)
        return render(request,'blog-blog-list.html',{'all_list':all_list,'q': q})

@csrf_exempt 
def save_comment(request):
    comment_msg    = request.POST['comment_msg']
    blog_id        = request.POST['blog_id']
    user           = CommentOnBlog.objects.create(user_id = request.user.id, blog_id = blog_id,message =comment_msg)
    comment_list   = CommentOnBlog.objects.filter(id = user.id ).first()

    html_message   = render_to_string('ajax_comment.html', {'c':comment_list})
    data_count     = CommentOnBlog.objects.filter(blog_id = blog_id ).count()
    count_val      = str(data_count) + " Comment"
       
    final_data     = { 'html_com': html_message,'count_val':count_val}
    return JsonResponse(final_data,safe = False)



@csrf_exempt 
def save_like(request):
    blog_id    = request.POST['blog_id']
    type_like  = request.POST['type_like']
    if type_like == "like":
        LikeOnBlog.objects.create(user_id = request.user.id, blog_id = blog_id)
    else:
        LikeOnBlog.objects.filter(user_id = request.user.id, blog_id = blog_id).delete()

    data_count   = LikeOnBlog.objects.filter(blog_id = blog_id).count()
    count_val    = str(data_count) + " Like"
    final_data   = {'count_val':count_val}
    return JsonResponse(final_data,safe = False)


def share_blog(request):
    email       = request.POST['email']
    blog_id     = request.POST['blogid_name']
    all_list    = PostBlog.objects.filter(id = blog_id).first()
    email_html  = render_to_string('blog_email.html', {'i':all_list,'request':request})

    email = EmailMessage(
        subject='Blog Post',
        body=email_html,
        from_email=EMAIL_HOST_USER,
        to=[email],
    )
    email.content_subtype = "html" 
    email.send()
    return redirect("/all-blog/")


class DeleteBlog(View):
    def get(self,request,id):
        PostBlog.objects.filter(id=id).delete()
        messages.success(request, "blog deleted successfully")
        return redirect('your-blog')