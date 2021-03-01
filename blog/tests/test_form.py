from django.http import response
from django.template.defaultfilters import title
from django.test import TestCase, testcases
from ..models import Comment, Entry
from ..forms import CommentForm
from django.contrib.auth import get_user_model

class CommentFormTest(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user('zoidberg')
        self.entry = Entry.objects.create(author=user, title="My entry title")

    def test_init(self):
        CommentForm(entry=self.entry)

    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            CommentForm()
    
    def test_valid_data(self):
        form = CommentForm({
            'name': "Turanga Leela",
            'email': "leela@example.com",
            'body': "Hi there",
        }, entry=self.entry)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, "Turanga Leela")
        self.assertEqual(comment.email, "leela@example.com")
        self.assertEqual(comment.body, "Hi there")
        self.assertEqual(comment.entry, self.entry)
    
    # def test_blank_data(self):
    #     form = CommentForm({}, entry=self.entry)
    #     self.assertFalse(form.is_valid())
    #     print(form.errors)
    #     self.assertEqual(form.errors, {
    #         'name': ['This field is required.'],
    #         'email': ['Thi[55 chars]d.'],
    #         'body': ["This fi[14 chars]d."],
    #     })
            