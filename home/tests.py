from django.test import TestCase
from home.views import get_index
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from accounts.models import User

class HomePageTest(TestCase):

    # can be in or out of code.
    fixtures = ['subjects', 'user']

    def setUp(self):
        super(HomePageTest, self).setUp()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('letmein')
        self.user.save()

    def test_login(self):
        login = self.client.login(username='testuser', password='letmein')
        self.assertTrue(login)

    def test_home_page_uses_index_view(self):
        home_page = resolve('/')
        self.assertEqual(home_page.func, get_index)

    def test_home_page_uses_index_template(self):
        home_page = self.client.get('/')
        self.assertTemplateUsed(home_page, "index.html")

    def test_home_page_logged_in_content(self):
        self.client.login(username='testuser', password='letmein')
        home_page = self.client.get('/')

        home_page_template_output = render_to_response(
            "index.html", {'user': self.user}).content
        self.assertEquals(home_page.content, home_page_template_output)

        # original tests below

    def test_home_page_resolves(self):
        home_page = resolve('/')
        self.assertEqual(home_page.func, get_index)


    def test_home_page_status_is_ok(self):
        home_page = self.client.get('/')
        self.assertEqual(home_page.status_code, 200)


    def test_check_content_is_correct(self):
        home_page = self.client.get('/')
        self.assertTemplateUsed(home_page, "index.html")
        home_page_template_output = render_to_response("index.html").content
        self.assertEqual(home_page.content, home_page_template_output)