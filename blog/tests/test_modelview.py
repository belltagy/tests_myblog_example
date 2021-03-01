from django.http import response
from django.template.defaultfilters import title
from django.test import TestCase, testcases
import webtest
from ..models import Comment, Entry
from ..forms import CommentForm
from django.contrib.auth import get_user_model
from django_webtest import WebTest
# Create your tests here.
class EntryModelTest(TestCase):
    
    def test_string_representation(self):
        entry=Entry.objects.create(title='fist blog name')
        self.assertEqual(str(entry),'fist blog name')
    
    def test_verbose_name_plural(self):
        self.assertEqual(str(Entry._meta.verbose_name_plural), "entries")
    
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code ,200)

class HomePageTests(TestCase):

    """Test whether our blog entries show up on the homepage"""

    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')

    def test_one_entry(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')

    def test_two_entries(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        Entry.objects.create(title='2-title', body='2-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, '2-title')

    def test_no_entries(self):
        response = self.client.get('/')
        self.assertContains(response,'No blog entries yet.')

class EntryViewTest(WebTest):

    def setUp(self):
        self.user=get_user_model().objects.create(username='some_user')
        self.entry = Entry.objects.create(title='1-title', body='1-body',
                                          author=self.user)
    
    def test_basic_view(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertEqual(response.status_code,200)

    def test_get_absolute_url(self):
        #user = get_user_model().objects.create(username='some_user')
        entry = Entry.objects.create(title="my entry detial",author=self.user)
        self.assertIsNotNone(entry.get_absolute_url())

    def test_view_page(self):
        page=self.app.get(self.entry.get_absolute_url())
        self.assertEqual(len(page.forms),1)

    def test_form_error(self):
        page = self.app.get(self.entry.get_absolute_url())
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get(self.entry.get_absolute_url())
        page.form['name'] = "Phillip"
        page.form['email'] = "phillip@example.com"
        page.form['body'] = "Test comment body."
        page = page.form.submit()
        self.assertRedirects(page, self.entry.get_absolute_url())



class CommentModelTest(TestCase):

    def setUp(self):
        self.user=get_user_model().objects.create(username='some_user')
        self.entry = Entry.objects.create(title='1-title', body='1-body',
                                          author=self.user)

    def test_string_representation(self):
        comment = Comment(body="My comment body")
        self.assertEqual(str(comment), "My comment body")
    def test_no_comment_yet(self):

        response=self.client.get(self.entry.get_absolute_url())
        self.assertContains(response,'No comments yet.')

    def test_one_comment_exist(self):

        comment=Comment.objects.create(entry=self.entry,name='comment1 name',body="comment1.")
        response=self.client.get(self.entry.get_absolute_url())
        self.assertContains(response,'comment1 name')

