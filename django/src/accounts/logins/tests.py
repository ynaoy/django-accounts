from django.test import TestCase
from .test.model_tests import UserModelTests
from .test.view_tests import UserViewTests

class Tests(TestCase):
  UserModelTests()
  UserViewTests()
