from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.edit import View
from .models import *


class KeyPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'key_page.html', {})


class SignupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html', {})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user = User.objects.create(username=username, email=email, is_active=False)
            user.set_password(password)
            user.save()
            return redirect('http://127.0.0.1:8000/get_code_for_confirm_registration/')
        else:
            return redirect('http://127.0.0.1:8000/signup_error/')


class GetCodeForConfirmRegistrationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'get_code_for_confirm_registration.html', {})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username, is_active=False)
        if user.exists() and user[0].check_password(password) and not OneTimeCode.objects.filter(user=user).exists():
            OneTimeCode.objects.create(symbols=str(randint(100000, 999999)), user=user[0])
            return redirect('http://127.0.0.1:8000/confirm_registration/')
        else:
            return redirect('http://127.0.0.1:8000/get_code_for_confirm_registration_error/')


class ConfirmRegistrationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'confirm_registration.html', {})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        one_time_code = request.POST['one_time_code']
        user = User.objects.filter(username=username, is_active=False)
        if user.exists() and OneTimeCode.objects.filter(symbols=one_time_code, user=user[0]).exists():
            user.is_active = True
            user.save()
            code = OneTimeCode.objects.get(symbols=one_time_code, user=user[0])
            code.delete()
            return redirect('http://127.0.0.1:8000/usual_login/')
        else:
            return redirect('http://127.0.0.1:8000/confirm_registration_error/')


class UsualLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'usual_login.html', {})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and not OneTimeCode.objects.filter(user=user).exists():
            OneTimeCode.objects.create(symbols=str(randint(100000, 999999)), user=user)
            return redirect('http://127.0.0.1:8000/login_with_code/')
        else:
            return redirect('http://127.0.0.1:8000/usual_login_error/')


class LoginWithCodeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login_with_code.html', {})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        one_time_code = request.POST['one_time_code']
        if OneTimeCode.objects.filter(symbols=one_time_code, user__username=username).exists():
            login(request, User.objects.get(username=username))
            code = OneTimeCode.objects.get(symbols=one_time_code, user__username=username)
            code.delete()
            return redirect('http://127.0.0.1:8000/')
        else:
            return redirect('http://127.0.0.1:8000/login_with_code_error/')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'logout.html', {})

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('http://127.0.0.1:8000/')


class AdvertisementsCreateView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.all()
        }
        return render(request, 'advertisements_create.html', context)

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        category_name = request.POST['category_name']
        content = request.POST['content']
        user = request.user
        category = Category.objects.get(name=category_name)
        advertisement = Advertisement.objects.create(title=title, category=category, content=content, user=user)
        return redirect(f'http://127.0.0.1:8000/advertisements/{advertisement.pk}/')


class YourAdvertisementsUpdateView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.all(),
            'advertisement': Advertisement.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        }
        return render(request, 'your_advertisements_update.html', context)

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        category_name = request.POST['category_name']
        content = request.POST['content']
        category = Category.objects.get(name=category_name)
        advertisement = Advertisement.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        advertisement.title = title
        advertisement.category = category
        advertisement.content = content
        advertisement.save()
        return redirect(f'http://127.0.0.1:8000/advertisements/{advertisement.pk}/')


class YourAdvertisementsDeleteView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'advertisement': Advertisement.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        }
        return render(request, 'your_advertisements_delete.html', context)

    def post(self, request, *args, **kwargs):
        advertisement = Advertisement.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        advertisement.delete()
        return redirect('http://127.0.0.1:8000/advertisements/')


class AdvertisementsListView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'advertisements': Advertisement.objects.all().order_by('-create_datetime')
        }
        return render(request, 'advertisements.html', context)


class AdvertisementDetailView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'advertisement': Advertisement.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        }
        return render(request, 'advertisement.html', context)


class YourAdvertisementsListView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'advertisements': Advertisement.objects.filter(user=request.user).order_by('-create_datetime')
        }
        return render(request, 'your_advertisements.html', context)


class YourAdvertisementDetailView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'advertisement': Advertisement.objects.get(user=request.user,
                                                       pk=int(''.join([i for i in request.path if i.isdigit()])))
        }
        return render(request, 'your_advertisement.html', context)


class RepliesOnAdsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'replies': Reply.objects.all().order_by('-create_datetime')
        }
        return render(request, 'replies_on_ads.html', context)


class RepliesOnAdView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'replies': Reply.objects.filter(
                advertisement__pk=int(''.join([i for i in request.path if i.isdigit()]))).order_by('-create_datetime')
        }
        return render(request, 'replies_on_ad.html', context)


class ReplyOnAdView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'replies': Reply.objects.filter(pk=int(''.join([i for i in request.path if i.isdigit()])),
                                            advertisement__pk=int(
                                                ''.join([i for i in request.path if i.isdigit()]))).order_by(
                '-create_datetime')
        }
        return render(request, 'reply_on_ad.html', context)


class YourRepliesOnAdsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'replies': Reply.objects.filter(user=request.user).order_by('-create_datetime')
        }
        return render(request, 'your_replies_on_ads.html', context)


class YourRepliesOnAdView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'replies': Reply.objects.filter(user=request.user,
                                            advertisement__pk=int(
                                                ''.join([i for i in request.path if i.isdigit()]))).order_by(
                '-create_datetime')
        }
        return render(request, 'your_replies_on_ad.html', context)


class YourReplyOnAdView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'replies': Reply.objects.filter(user=request.user,
                                            pk=int(''.join([i for i in request.path if i.isdigit()])),
                                            advertisement__pk=int(
                                                ''.join([i for i in request.path if i.isdigit()]))).order_by(
                '-create_datetime')
        }
        return render(request, 'your_reply_on_ad.html', context)


class RepliesOnYourAdsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'replies': Reply.objects.filter(advertisement__user=request.user).order_by('-create_datetime')
        }
        return render(request, 'replies_on_your_ads.html', context)


class RepliesOnYourAdView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'replies': Reply.objects.filter(advertisement__pk=int(''.join([i for i in request.path if i.isdigit()])),
                                            advertisement__user=request.user).order_by('-create_datetime')
        }
        return render(request, 'replies_on_your_ad.html', context)


class ReplyOnYourAdView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'replies': Reply.objects.filter(pk=int(''.join([i for i in request.path if i.isdigit()])),
                                            advertisement__pk=int(''.join([i for i in request.path if i.isdigit()])),
                                            advertisement__user=request.user).order_by('-create_datetime')
        }
        return render(request, 'reply_on_your_ad.html', context)


class RepliesCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'replies_create.html', {})

    def post(self, request, *args, **kwargs):
        advertisement = Advertisement.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        text = request.POST['text']
        user = request.user
        reply = Reply.objects.create(advertisement=advertisement, text=text, user=user)
        return redirect(f'http://127.0.0.1:8000/advertisements/{advertisement.pk}/replies/{reply.pk}/')


class YourRepliesUpdateView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'reply': Reply.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        }
        return render(request, 'your_replies_update.html', context)

    def post(self, request, *args, **kwargs):
        text = request.POST['text']
        reply = Reply.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        reply.text = text
        reply.save()
        return redirect(f'http://127.0.0.1:8000/advertisements/{advertisement.pk}/replies/{reply.pk}/')


class YourRepliesDeleteView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'reply': Reply.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        }
        return render(request, 'your_replies_delete.html', context)

    def post(self, request, *args, **kwargs):
        reply = Reply.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        reply.delete()
        advertisement = Advertisement.objects.get(pk=int(''.join([i for i in request.path if i.isdigit()])))
        return redirect(f'http://127.0.0.1:8000/advertisements/{advertisement.pk}/replies/')


class SignupErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup_error.html', {})


class GetCodeForConfirmRegistrationErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'get_code_for_confirm_registration_error.html', {})


class ConfirmRegistrationErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'confirm_registration_error.html', {})


class UsualLoginErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'usual_login_error.html', {})


class LoginWithCodeErrorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login_with_code_error.html', {})
