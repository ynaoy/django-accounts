from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, UpdateView as BaseUpdateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView, PasswordChangeView
from django.contrib.auth.mixins import UserPassesTestMixin 
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import User

class OnlyYouMixin(UserPassesTestMixin):
    """
    ユーザー自身しか通さないMIXIN
    """
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk']
    
class OnlyLoginMixin(UserPassesTestMixin):
    """
    ログイン中のユーザーしか通さないMIXIN
    """
    def test_func(self):
        # ログインしていないならログインページにリダイレクト
        return self.request.user.pk!=None
    
    def handle_no_permission(self):
        return redirect('logins:login')

class OnlyLogoutMixin(UserPassesTestMixin):
    """
    ログアウト中のユーザーしか通さないMIXIN
    """
    raise_exception = True

    def test_func(self):
        # ログインしているならエラーを発生させる
        return self.request.user.pk==None
    
    
class IndexView(TemplateView):
    """ ホームビュー """
    template_name = "index.html"


class SignupView(CreateView):
    """ ユーザー登録用ビュー """
    model = User
    fields = ("user_name",
              "email",
              "password",)
    template_name = "signup.html" 
    success_path = "logins:index"
    failure_path = "logins:signup"

    def form_valid(self, form):
        """ユーザー作成とログインをしてリダイレクト"""
        try:
            raw_password = form.cleaned_data.get("password")
            user_name = form.cleaned_data.get("user_name")
            email = form.cleaned_data.get("email")
            user= self.model.objects.create_user(user_name=user_name,
                                                 email=email,
                                                 password=raw_password)
            login(self.request, user)
            return redirect(self.success_path)
        except:
            return redirect(self.failure_path)
        
class UpdateView(OnlyYouMixin, BaseUpdateView):
    """ユーザー更新用ビュー"""
    model = User
    fields = ("user_name",
              "email",)
    template_name = 'update.html'

    def get_success_url(self):
        return reverse_lazy("logins:index")
    
class UpdatePasswordView(OnlyYouMixin, PasswordChangeView):
    """パスワード更新用ビュー"""
    model = User
    fields = ("password")
    success_url = reverse_lazy('logins:index')
    template_name = 'update_password.html'

class LoginView(OnlyLogoutMixin, BaseLoginView):
  """ ログイン用ビュー """
  model = User
  template_name = "login.html"

class LogoutView(OnlyLoginMixin, BaseLogoutView):
    """ ログアウト用ビュー """
    success_url = reverse_lazy("logins:index")

