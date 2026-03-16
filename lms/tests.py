from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from lms.models import Course, Lesson, Subscription


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='12345678'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='12345678'
        )
        self.moderator = User.objects.create_user(
            email='moderator@test.com',
            password='12345678'
        )

        self.moderators_group = Group.objects.create(name='moderators')
        self.moderator.groups.add(self.moderators_group)

        self.course = Course.objects.create(
            title='Python course',
            description='Test description',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='Lesson 1',
            description='Lesson description',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

        self.lesson_list_url = reverse('lesson-list')
        self.lesson_detail_url = reverse('lesson-detail', args=[self.lesson.id])

    def test_lesson_create_by_owner(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'New lesson',
            'description': 'New description',
            'video_url': 'https://www.youtube.com/watch?v=abc',
            'course': self.course.id
        }

        response = self.client.post(self.lesson_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        created_lesson = Lesson.objects.get(title='New lesson')
        self.assertEqual(created_lesson.owner, self.user)

    def test_lesson_create_by_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)

        data = {
            'title': 'New lesson',
            'description': 'New description',
            'video_url': 'https://www.youtube.com/watch?v=abc',
            'course': self.course.id
        }

        response = self.client.post(self.lesson_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_by_owner(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Updated lesson',
            'description': self.lesson.description,
            'video_url': self.lesson.video_url,
            'course': self.course.id
        }

        response = self.client.put(self.lesson_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated lesson')

    def test_lesson_update_by_other_user_forbidden(self):
        self.client.force_authenticate(user=self.user2)

        data = {
            'title': 'Hacked lesson',
            'description': self.lesson.description,
            'video_url': self.lesson.video_url,
            'course': self.course.id
        }

        response = self.client.put(self.lesson_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_by_moderator(self):
        self.client.force_authenticate(user=self.moderator)

        data = {
            'title': 'Moderator updated lesson',
            'description': self.lesson.description,
            'video_url': self.lesson.video_url,
            'course': self.course.id
        }

        response = self.client.put(self.lesson_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Moderator updated lesson')

    def test_lesson_delete_by_owner(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_delete_by_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)

        response = self.client.delete(self.lesson_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_list_only_own_lessons_for_user(self):
        Lesson.objects.create(
            title='Other lesson',
            description='Other description',
            video_url='https://www.youtube.com/watch?v=other',
            course=self.course,
            owner=self.user2
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_lesson_list_all_for_moderator(self):
        Lesson.objects.create(
            title='Other lesson',
            description='Other description',
            video_url='https://www.youtube.com/watch?v=other',
            course=self.course,
            owner=self.user2
        )

        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.lesson_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='12345678'
        )
        self.course = Course.objects.create(
            title='Python course',
            description='Test description',
            owner=self.user
        )

        self.subscription_url = reverse('subscription')
        self.course_detail_url = reverse('course-detail', args=[self.course.id])

    def test_subscription_create(self):
        self.client.force_authenticate(user=self.user)

        data = {'course_id': self.course.id}
        response = self.client.post(self.subscription_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_delete(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

        data = {'course_id': self.course.id}
        response = self.client.post(self.subscription_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_course_is_subscribed_true(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.course_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])

    def test_course_is_subscribed_false(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.course_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_subscribed'])

    def test_subscription_unauthorized_forbidden(self):
        data = {'course_id': self.course.id}
        response = self.client.post(self.subscription_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)