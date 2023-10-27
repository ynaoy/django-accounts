from django.test import TestCase
from django.urls import reverse
from unittest import skip
from ..models import User

def create_default_user(user_name="Test User",
                       email="example@example.com",
                       password="password"):
  user= User.objects.create_user(user_name=user_name,
                                       email=email,
                                       password=password)
  return user

class UserViewTests(TestCase):
  def test_index_view_with_not_login(self):
    """
    非ログイン時にindex_viewが表示されている
    """
    response = self.client.get(reverse("logins:index"))
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.context["user"])
    # 非ログイン時に表示されるコンテンツ
    self.assertContains(response, "Main")
    self.assertContains(response, "Signup")
    self.assertContains(response, "Login")

  def test_index_view_with_not_login(self):
    """
    ログイン時にindex_viewが表示されている
    """
    test_user = create_default_user()
    self.client.force_login(test_user)
    response = self.client.get(reverse("logins:index"))
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.context["user"])
    # ログイン時に表示されるコンテンツ
    self.assertContains(response, "Update")
    self.assertContains(response, "Update Password")
    self.assertContains(response, "Logout")
  

  def test_signup_view_get(self):
    """
    signup_viewにGETメソッドを送ったときにページが表示されている
    """
    response = self.client.get(reverse("logins:signup"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Create")
    self.assertContains(response, "Back")

  def test_signup_view_post(self):
    """
    signup_viewにPOSTメソッドを送ったときにユーザーが追加されてログインされている
    """
    response = self.client.post(reverse("logins:signup"),
                                { "user_name": "Test User",
                                  "email": "example@example.com",
                                  "password": "password"})
    self.assertRedirects(response, reverse("logins:index"))
    # sessionidが存在すればログインできている
    self.assertTrue(response.cookies.get("sessionid"))
    # ユーザーが追加されている
    self.assertTrue(User.objects.get(email="example@example.com"))

  def test_update_view_get(self):
    """
    update_viewにGETメソッドを送ったときにページが表示されている
    """
    test_user = create_default_user()
    self.client.force_login(test_user)
    response = self.client.get(reverse("logins:update", args=[test_user.pk]))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Update")
    self.assertContains(response, "Back")

  def test_update_view_get_by_another_user(self):
    """
    logins/update/<another_users_id>にGETメソッドを送ったときにページが表示されない
    """
    test_user = create_default_user()
    self.client.force_login(test_user)
    another_user = create_default_user(user_name="another_user",email="another_user@email.com")
    response = self.client.get(reverse("logins:update", args=[another_user.pk]))
    self.assertEqual(response.status_code, 403)

  def test_update_view_post(self):
    """
    logins/update/<another_users_id>にPOSTメソッドを送ったときにユーザーが更新される
    """
    test_user = create_default_user()
    self.client.force_login(test_user)
    response = self.client.post(reverse("logins:update", args=[test_user.pk]),
                                { "user_name":"Changed User",
                                  "email":"changedemail@example.com" },
                                )
    self.assertRedirects(response, reverse("logins:index"))

    test_user = User.objects.get(pk=test_user.pk)
    self.assertEqual(test_user.user_name,"Changed User")
    self.assertEqual(test_user.email,"changedemail@example.com")

  def test_update_password_view_get(self):
    """
    update_password_viewにGETメソッドを送ったときにページが表示されている
    """
    test_user = create_default_user()
    self.client.force_login(test_user)
    response = self.client.get(reverse("logins:update_password", args=[test_user.pk]))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Update")
    self.assertContains(response, "Back")

  def test_update_password_view_get_by_another_user(self):
    """
    logins/update_password/<another_users_id>にGETメソッドを送ったときにページが表示されない
    """
    test_user = create_default_user()
    self.client.force_login(test_user)
    another_user = create_default_user(user_name="another_user",email="another_user@email.com")
    response = self.client.get(reverse("logins:update_password", args=[another_user.pk]))
    self.assertEqual(response.status_code, 403)

  def test_update_password_view_post(self):
    """
    logins/update/<another_users_id>にPOSTメソッドを送ったときにユーザーが更新される
    """
    test_user = create_default_user()
    before_password = test_user.password
    self.client.force_login(test_user)
    response = self.client.post(reverse("logins:update_password", args=[test_user.pk]),
                                { "old_password":   "password",
                                  "new_password1":  "new_password",
                                  "new_password2":  "new_password" }
                                )
    self.assertRedirects(response, reverse("logins:index"))
    test_user = User.objects.get(pk=test_user.pk)
    self.assertNotEqual(test_user.password, before_password)


  def test_login_view_get(self):
    """
    login_viewにGETメソッドを送ったときにページが表示されている
    """
    response = self.client.get(reverse("logins:login"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Login")
    self.assertContains(response, "Back")

  def test_login_view_get_with_login(self):
    """
    ログイン状態の時にlogin_viewにGETメソッドを送ったときにリダイレクトされる
    """
    test_user = create_default_user()
    self.client.force_login(test_user)
    response = self.client.get(reverse("logins:login"))
    self.assertEqual(response.status_code, 403)

  def test_login_view_post(self):
    """
    login_viewにPOSTメソッドを送ったときにログイン状態になる
    """
    test_user = create_default_user()
    response = self.client.post(reverse("logins:login"),
                                { "username":  test_user.email,
                                  "password":  "password" }
                                )
    self.assertRedirects(response, reverse("logins:index"))
    # sessionidが存在すればログインできている
    self.assertTrue(response.cookies.get("sessionid"))

  def test_logout_view_get_with_not_login(self):
    """
    ログインしていないときにlogout_viewにGETメソッドを送ったらリダイレクトされる
    """
    response = self.client.get(reverse("logins:logout"))
    self.assertRedirects(response, reverse("logins:login"))

  def test_logout_view_get(self):
    """
    logout_viewにGETメソッドを送ったときにログアウト状態になる
    """
    test_user = create_default_user()
    self.client.force_login(test_user)
    response = self.client.get(reverse("logins:logout"))
    self.assertRedirects(response, reverse("logins:login"))
    # sessionidのmax-ageが0になっていればログアウトできている
    self.assertEqual(response.cookies.get("sessionid")["max-age"], 0)

