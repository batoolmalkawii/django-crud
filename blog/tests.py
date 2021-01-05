from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Post

# Create your tests here.

class SnacksCRUDTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'batool',
            email = 'batool@batool.com',
            password = '2231996'
        )
        self.post = Post.objects.create(
            title = 'TestPost',
            author = self.user,
            body = 'Is this a real blog?'
        )

    # Pages Status
    def test_posts_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_post_details_status(self):
        response = self.client.get(reverse('post_details', args='1'))
        self.assertEqual(response.status_code, 200)

    def test_post_details_content(self):
        response = self.client.get(reverse('post_details', args='1'))
        self.assertContains(response, 'TestPost')

    def test_update_post_status(self):
        urls = reverse('post_update',args='1')
        response = self.client.get(urls)
        self.assertEquals(response.status_code, 200)

    
    # Create
    def test_create_post_status(self):
        urls = reverse('post_create')
        response = self.client.get(urls)
        self.assertEquals(response.status_code, 200)

    # Update
    def test_post_update(self):
        response = self.client.post(reverse('post_update', args='1'), {
            'body': 'This is not a real blog.',
        })
        self.assertContains(response, 'This is not a real blog.')
        self.assertNotContains(response, 'Is this a real blog?')

    # Delete
    def test_delete_post_status(self):
        post_response = self.client.post(reverse('post_delete', args='1'), follow=True)
        self.assertRedirects(post_response, reverse('home'), status_code=302)
        
    def test_post_after_delete_status(self):
        self.client.post(reverse('post_delete', args='1'), follow=True)
        urls = reverse('post_delete', args='1')
        response = self.client.get(urls)
        self.assertEquals(response.status_code, 404)