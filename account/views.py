import pdb

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .models import UserProfile
from .forms import ProfileForm, ExtendedUser, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib import messages
from products.models import OrderDetail


#
# class UserSignUpView(View):
#     try:
#         def get(self, request):
#             user_form = ExtendedUser()
#             profile_form = ProfileForm()
#             return render(request, 'signup1.html', {
#                 'user_form': user_form, 'profile_form': profile_form})
#
#         def post(self, request):
#             profile_form = ProfileForm(request.POST, request.FILES)
#             user_form = ExtendedUser(request.POST)
#
#             if user_form.is_valid() and profile_form.is_valid():
#                 user = user_form.save()
#                 profile = profile_form.save(commit=False)
#                 profile.user = user
#                 profile.save()
#                 username = user_form.cleaned_data.get("username")
#                 password = user_form.cleaned_data.get("password1")
#                 signupuserlogin = authenticate(
#                     username=username, password=password)
#                 login(request, signupuserlogin)
#                 return HttpResponseRedirect(reverse('list_products'))
#             else:
#                 login_form = UserLoginForm()
#                 return render(request, "signup1.html", {'user_form': user_form,
#                                                         'login_form': login_form})
#             profile_form = ProfileForm()
#             user_form = ExtendedUser()
#             login_form = UserLoginForm()
#             return render(request, "signup1.html", {'profile_form': profile_form,
#                                                     'user_form': user_form, 'login_form': login_form})
#     except Exception as e:
#         print(e)
#


class UserSignUpView(View):
    try:
        def get(self, request):
            user_form = ExtendedUser()
            profile_form = ProfileForm()
            return render(request, 'signup1.html', {
                'user_form': user_form, 'profile_form': profile_form})

        def post(self, request):
            profile_form = ProfileForm(request.POST, request.FILES)
            user_form = ExtendedUser(request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                self.userlogin = user
                user.is_active = False
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('activate_eamil_message.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = user_form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, "Your Account has successfully created Please confirm your mail to Login ")

                return render(request, "login.html")
            else:
                return render(request, 'signup1.html', {
                    'user_form': user_form, 'profile_form': profile_form})

    except Exception as e:
        print(e)


UserModel = get_user_model()


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class UserLoginView(View):
    def get(self, request):
        login_form = UserLoginForm
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        login_form = UserLoginForm(request, request.POST)
        # username = login_form.GET.get('username')

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if not user.is_active:
                raise ValidationError("This account is inactive. please activate using your email link", code='inactive')
            else:
                if user is not None:
                    login(request, user)
                    return redirect('list_products')
                else:
                    return HttpResponse("no found ")

        return render(request,'login.html', {'login_form': login_form})


class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("list_products"))


class AccountView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # pdb.set_trace()
        user = request.user
        orders = user.orderdetail_set.all()

        order = {'status': 'Pending', 'orders': orders}
        return render(request, 'account.html', order)


class UpdateProfilePhoto(View):
    def post(self, request):
        image = request.FILES.get('image')
        profile_object = UserProfile.objects.get(user=request.user)
        profile_object.profile_pic = image
        profile_object.save()
        return redirect('/profile/')


class Tracking(View):
    def get(self, request):
        orders = OrderDetail.objects.all()

        return render(request, 'tracking.html')
