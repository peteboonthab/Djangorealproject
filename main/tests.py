from django.test import TestCase
from django.urls import reverse
from .models import Signin, Unit
from django.http import HttpResponse
from .views import teacher_required


class AuthTest(TestCase):

    def test_upload_requires_login(self):

        response = self.client.get(
            reverse('file_page')
        )

        self.assertEqual(response.status_code, 302)

class SignupTest(TestCase):

    def test_create_user(self):

        user = Signin.objects.create(
            user='pete',
            password='hello@123',
            role='student'
        )

        self.assertEqual(user.user, 'pete')

class TeacherPermissionTest(TestCase):

    def test_student_cannot_access_teacher_page(self):

        unit = Unit.objects.create(
            unit_name='Math')
        

        Signin.objects.create(
            user='student1',
            password='pass@123',
            role='student'
        )

        session = self.client.session
        session['user'] = 'student1'
        session.save()

        response = self.client.get(
            reverse('unit_detail', args=[1])
        )

        self.assertEqual(response.status_code, 302)





