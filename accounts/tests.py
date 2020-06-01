from django.test import TestCase, Client
from accounts.models import Profile
from django.contrib.auth.models import User
from django.conf import settings
from accounts.forms import ProfileForm
from accounts.views import SignUp
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
import os



# forms
class AccountsFormsTestCase(TestCase):
    def create_user(self, username, email):
        return User.objects.create(username=username, email=email)

    def setUp(self):
        self.user1 = self.create_user('user1', 'user1@gmail.com')
        self.profile1 = Profile.objects.get(id=1)

    def test_is_form_valid(self):
        form_data = {
            'city': 'bialystok',
            'description': 'test-description',
            'image': 'test.jpg',
            'website': 'http://google.com'
        }
        profile_form = ProfileForm(data=form_data)
        self.assertTrue(profile_form.is_valid())
        self.assertEqual(self.profile1.profile_img, 'default.jpg')

    def test_max_description_characters(self):
        form_data = {
            'city': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque tempor cursus iaculis. Maecenas at diam sed tellus cursus pellentesque non a quam.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque tempor cursus iaculis. Maecenas at diam sed tellus cursus pellentesque non a quam.'
        }
        profile_form = ProfileForm(data=form_data)
        self.assertFalse(profile_form.is_valid())

#models
class AccountsModelsTestCase(TestCase):
    def create_user(self, username, email):
        return User.objects.create(username=username, email=email)

    def setUp(self):
        self.user1 = self.create_user('user1', 'user1@gmail.com')
        self.profile1 = Profile.objects.get(id=1)

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user1, User))
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user1.email, 'user1@gmail.com')
        self.assertEqual(self.user1.id, 1)

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.profile1, Profile))
        self.assertEqual(self.profile1.id, 1)
        self.assertEqual(self.profile1.user, self.user1)
        self.assertEqual(str(self.profile1), 'user1 Profile')

# views


class AccountsViewsTestCase(TestCase):
    def generate_photo_file(self, filename):
        file = BytesIO(
            b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            b'\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        file.name = filename
        file.seek(0)
        return file

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('index')
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.profile_url = reverse('accounts:profile', args=['usertest1'])
        self.edit_profile_url = reverse('accounts:profile_edit')
        self.edit_profile_password_url = reverse('accounts:profile_password')
        self.user1_account = {'username': 'UserTest1', 'email': 'usertest1@gmail.com', 
                'password1': 'usertestpassword123', 'password2': 'usertestpassword123'}
        self.new_image = self.generate_photo_file('new.jpg')


    def test_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_post(self):
        response = self.client.post(self.signup_url, self.user1_account, follow=True)
        user_number = User.objects.count()
        usertest1 = User.objects.get(id=1)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(user_number, 1)
        self.assertEqual(usertest1.email, 'usertest1@gmail.com')
        # self.assertEqual(usertest1.is_authenticated, True)
        self.assertEqual(usertest1.username, 'UserTest1')

    def test_login_get(self):
        response = self.client.get(self.login_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    
    def test_login_post(self):
        usertest1 = User.objects.create_user(username='UserTest1', email='usertest1@gmail.com', password='usertestpassword123')
        # self.assertTrue(usertest1.is_authenticated)
        response = self.client.post(self.login_url, {'username': 'UserTest1','password': 'usertestpassword123'}, follow=True)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.status_code, 200)




    def test_profile_detail_not_log_in(self):

        response = self.client.get(self.profile_url, follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')
        # 200 not log in
        self.assertEqual(response.status_code, 200)

    
    def test_profile_detail_log_in(self):

        usertest1 = User.objects.create_user(username='UserTest1', email='usertest1@gmail.com', password='usertestpassword123')
        self.client.login(username='UserTest1', password='usertestpassword123')
        response = self.client.get(self.profile_url, follow=True)
       
        self.assertTemplateUsed(response, 'accounts/profile.html')
        # self.assertTrue(usertest1.is_authenticated)
        self.assertEqual(response.status_code, 200)

        #profile detail data
        profile_detail = response.context['profile']
        self.assertEqual(profile_detail.username, 'UserTest1')
        self.assertEqual(profile_detail.email, 'usertest1@gmail.com')
        self.assertEqual(profile_detail.first_name, '')
        self.assertEqual(profile_detail.last_name, '')
        self.assertEqual(profile_detail.profile.description, '')
        self.assertEqual(profile_detail.profile.city, '')
        self.assertEqual(profile_detail.profile.website, '')
        self.assertEqual(profile_detail.profile.profile_img, 'default.jpg')
        

    def test_profile_edit_detail_not_log_in(self):
        response = self.client.get(self.edit_profile_url, follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_detail_log_in_get(self):
        usertest1 = User.objects.create_user(username='UserTest1', email='usertest1@gmail.com', password='usertestpassword123')
        self.client.login(username='UserTest1', password='usertestpassword123')
        response = self.client.get(self.edit_profile_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')



    def test_profile_edit_detail_log_in_post(self):
        # create a new file
        newimg = SimpleUploadedFile('newimg.jpg', self.new_image.read(), content_type='image/jpg')

        usertest1 = User.objects.create_user(username='UserTest1', email='usertest1@gmail.com', password='usertestpassword123')
        self.client.login(username='UserTest1', password='usertestpassword123')
        form_data = {'first_name':'John','last_name':'Doe','email':'newmail@gmail.com',
        'description':'NewEdit', 'city':'Bialystok','website':'http://google.com',
        'profile_img':newimg }
        response = self.client.post(self.edit_profile_url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

        profile_detail = response.context['profile']
        self.assertEqual(profile_detail.username, 'UserTest1')
        self.assertEqual(profile_detail.email, 'newmail@gmail.com')
        self.assertEqual(profile_detail.first_name, 'John')
        self.assertEqual(profile_detail.last_name, 'Doe')
        self.assertEqual(profile_detail.profile.description, 'NewEdit')
        self.assertEqual(profile_detail.profile.city, 'Bialystok')
        self.assertEqual(profile_detail.profile.website, 'http://google.com')
        self.assertEqual(profile_detail.profile.profile_img, 'profile/newimg.jpg')
        # remove newly generated file
        os.remove(settings.MEDIA_ROOT + '/profile/newimg.jpg')

        # test to check if default photo is fallbacking correctly
        form_data_without_photo = {'first_name':'Adam','last_name':'Malysz','email':'newmail@gmail.com',
        'description':'NewEdit', 'city':'Bialystok','website':'http://google.com',
        'profile_img': '', 'profile_img-clear': 'on' }
        response_without_photo = self.client.post(self.edit_profile_url, form_data_without_photo, follow=True)
        profile_detail_without_photo = response_without_photo.context['profile']
        self.assertEqual(profile_detail_without_photo.profile.profile_img, 'default.jpg')

    def test_profile_change_password_not_log_in(self):
        response = self.client.get(self.edit_profile_password_url, follow=True)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(response.status_code, 200)


    def test_profile_change_password_get(self):
        usertest1 = User.objects.create_user(username='UserTest1', email='usertest1@gmail.com', password='usertestpassword123')
        self.client.login(username='UserTest1', password='usertestpassword123')
        response = self.client.get(self.edit_profile_password_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_change_password.html')


    def test_profile_change_password(self):
        usertest1 = User.objects.create_user(username='UserTest1', email='usertest1@gmail.com', password='usertestpassword123')
        self.client.login(username='UserTest1', password='usertestpassword123')
        form_data = {'old_password': 'usertestpassword123', 'new_password1':'newusertestpassword123', 'new_password2':'newusertestpassword123'}
        response = self.client.post(self.edit_profile_password_url , form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_change_password_password_wrong_pass(self):
        usertest1 = User.objects.create_user(username='UserTest1', email='usertest1@gmail.com', password='usertestpassword123')
        self.client.login(username='UserTest1', password='usertestpassword123')
        form_data = {'WRONGold_password': 'usertestpassword123', 'new_password1':'newusertestpassword123', 'new_password2':'newusertestpassword123'}
        response = self.client.post(self.edit_profile_password_url , form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error', status_code=200 )
        self.assertTemplateUsed(response, 'accounts/profile_change_password.html')



      
    