import os
from datetime import timedelta

from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files import File
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.test import TestCase
from django.utils import timezone

from AATP import settings
from EasyStay.form import ManagerRegisterForm, ChangePasswordForm
from EasyStay.models import hotelmanager, roomtype, hotel, room, booking, user

# Create your tests here.

"""Login/Register Test"""


class LoginViewTests(TestCase):
    """Login test"""

    def test_login_home_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/user_login.html')

    """Manager Login test"""

    def test_manager_login_get(self):
        response = self.client.get(reverse('manager_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/manager_login.html')

    """Login Post test"""

    def test_manager_login_post_success(self):
        manager = hotelmanager.objects.create(email="kirayy301@gmail.com", password="1111111)P", manage_id="1")
        response = self.client.post(reverse('manager_login'),
                                    {'email': 'kirayy301@gmail.com', 'password': '1111111)P'})
        self.assertRedirects(response, expected_url=reverse('manager_home'))

    """Register Form Test"""

    def test_form_password_confirmation_failure(self):
        form_data = {
            'email': 'manager@example.com',
            'phone': '1234567890',
            'password': 'ABABABAB123!',
            'confirm_password': 'ABABABAB1234'
        }
        form = ManagerRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)

    def test_form_success(self):
        form_data = {
            'email': 'manager@gmail.com',
            'phone': '1111111111',
            'password': 'ABABABAB123!',
            'confirm_password': 'ABABABAB123!'
        }
        form = ManagerRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    """Manager Register test"""

    def test_manager_registration_success_redirect(self):
        form_data = {
            'email': 'manager@gmail.com',
            'phone': '1111111111',
            'password': 'ABABABAB123!',
            'confirm_password': 'ABABABAB123!'
        }
        response = self.client.post(reverse('manager_register'), form_data)

        self.assertTrue(hotelmanager.objects.filter(email='manager@gmail.com').exists())

        self.assertRedirects(response, reverse('manager_login') + '?uid=' + hotelmanager.objects.latest(
            'id').manage_id + '&from_url=manager_register', fetch_redirect_response=False)


"""Manager Home Test"""


class ManagerHomeNoHotelInfoTests(TestCase):
    def setUp(self):
        self.manager = hotelmanager.objects.create(email="manager@example.com", phone="+1234567890",
                                                   password="password", manage_id="M123456789")

    def test_manager_home_no_hotel_info(self):
        session = self.client.session
        session['id'] = self.manager.id
        session['manager_id'] = self.manager.manage_id
        session.save()

        response = self.client.get(reverse('manager_home'))
        self.assertTemplateUsed(response, 'manager/home_addhotel.html')


class ManagerHomeWithHotelInfoTests(TestCase):
    def setUp(self):
        self.manager = hotelmanager.objects.create(
            email="manager@example.com",
            phone="+1234567890",
            password="password",
            manage_id="M123456789"
        )

        test_image_hotel = os.path.join(settings.BASE_DIR, 'media', 'hotel_image', 'test.jpg')
        with open(test_image_hotel, 'rb') as file:
            self.image = File(file, name='test.jpg')
            self.hotel = hotel.objects.create(
                manager=self.manager,
                hotel_id="H123456789",
                name="Test Hotel",
                country="Test Country",
                city="Test City",
                location="Test Location",
                postcode="G11 G11",
                email="hotel@example.com",
                phone="+0987654321",
                description="Test Description",
                facility='["WiFi", "Pool", "Gym"]',
                image=self.image
            )

        # 如果需要为roomtype设置image字段，确保已经有了一个有效的文件路径
        test_image_room = os.path.join(settings.BASE_DIR, 'media', 'room_image', 'test.jpg')
        with open(test_image_room, 'rb') as file:
            self.image = File(file, name='test.jpg')
            self.room_type = roomtype.objects.create(
                hotel=self.hotel,
                type="Single",
                price=100,
                guests=1,
                facility='["WiFi", "Pool", "Gym"]',
                image=self.image
            )

    def test_manager_home_with_hotel_info(self):
        session = self.client.session
        session['id'] = self.manager.id
        session['manager_id'] = self.manager.manage_id
        session.save()

        response = self.client.get(reverse('manager_home'))
        self.assertTemplateUsed(response, 'manager/home.html')
        self.assertEqual(response.context['hotel'], self.hotel)

class ChangePasswordTests(TestCase):
    def setUp(self):
        # 直接使用 create 方法创建 hotelmanager 实例，密码为明文
        self.user = hotelmanager.objects.create(
            email="user@example.com",
            password="old_password",  # 明文密码
            manage_id="M123456"
        )
        # 模拟登录
        self.client.login(email="user@example.com", password="old_password")
        self.url = reverse('change_password')

    def test_change_password_form_display(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], ChangePasswordForm)
        self.assertTemplateUsed(response, 'manager/change_password.html')


class ManagerRoomPageTests(TestCase):
    def setUp(self):
        self.manager = hotelmanager.objects.create(
            email="manager@example.com",
            phone="+1234567890",
            password="AAAA!!0091",
            manage_id="M123456789"
        )

        test_image_hotel = os.path.join(settings.BASE_DIR, 'media', 'hotel_image', 'test.jpg')
        with open(test_image_hotel, 'rb') as file:
            self.image = File(file, name='test.jpg')
            self.hotel = hotel.objects.create(
                manager=self.manager,
                hotel_id="H123456789",
                name="Test Hotel",
                country="Test Country",
                city="Test City",
                location="Test Location",
                postcode="G11 G11",
                email="hotel@example.com",
                phone="+0987654321",
                description="Test Description",
                facility='["WiFi", "Pool", "Gym"]',
                image=self.image
            )

        # 如果需要为roomtype设置image字段，确保已经有了一个有效的文件路径
        test_image_room = os.path.join(settings.BASE_DIR, 'media', 'room_image', 'test.jpg')
        with open(test_image_room, 'rb') as file:
            self.image = File(file, name='test.jpg')
            self.room_type1 = roomtype.objects.create(
                hotel=self.hotel,
                type="Single",
                price=100,
                guests=1,
                facility='["WiFi", "Pool", "Gym"]',
                image=self.image
            )
        with open(test_image_room, 'rb') as file:
            self.image = File(file, name='test.jpg')
            self.room_type2 = roomtype.objects.create(
                hotel=self.hotel,
                type="Double",
                price=100,
                guests=1,
                facility='["WiFi", "Pool", "Gym"]',
                image=self.image
            )

        self.room1 = room.objects.create(
            type=self.room_type2,
            Room_number="101",
            availability=True
        )
        self.room2 = room.objects.create(
            type=self.room_type2,
            Room_number="102",
            availability=True
        )

        session = self.client.session
        session['id'] = self.manager.id
        session['manager_id'] = self.manager.manage_id
        session.save()

    def test_manager_room_page_access(self):
        response = self.client.get(reverse('manager_room'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/room.html')

    def test_room_types_listed(self):
        response = self.client.get(reverse('manager_room'))
        self.assertContains(response, self.room_type1.type)
        self.assertContains(response, self.room_type2.type)

    def test_delete_room_type(self):
        response = self.client.delete(reverse('delete_room_type', kwargs={'room_type_id': self.room_type1.id}))
        self.assertFalse(roomtype.objects.filter(id=self.room_type1.id).exists())

    def test_delete_room_type_redirection(self):
        response = self.client.delete(reverse('delete_room_type', kwargs={'room_type_id': self.room_type1.id}))
        self.assertRedirects(response, reverse('manager_room'), msg_prefix="Successful redirect expected")

    def test_show_rooms(self):
        # Make a GET request to show_rooms view
        response = self.client.get(reverse('show_rooms', kwargs={'room_type_id': self.room_type2.id}))
        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        # Check if the template used is correct
        self.assertTemplateUsed(response, 'manager/room_by_type.html')
        # Check if room_type, rooms, id, manager_id, and hotel are present in the context
        self.assertIn('room_type', response.context)
        self.assertIn('rooms', response.context)
        self.assertIn('id', response.context)
        self.assertIn('manager_id', response.context)
        self.assertIn('hotel', response.context)
        # Check if the room_type in the context matches the room_type used in the test
        self.assertEqual(response.context['room_type'], self.room_type2)
        # Check if the number of rooms in the context matches the number of rooms created in the test
        self.assertEqual(len(response.context['rooms']), 2)

    def test_add_rooms_get(self):
        # Make a GET request to add_rooms view
        response = self.client.get(reverse('add_rooms', kwargs={'room_type_id': self.room_type2.id}))
        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        # Check if the template used is correct
        self.assertTemplateUsed(response, 'manager/room_add_rooms.html')
        # Check if the form is present in the context
        self.assertIn('form', response.context)

    def test_add_rooms_post_success(self):
        # Make a POST request to add_rooms view with valid form data
        form_data = {
            'Room_number': '111',  # Unique room number
            'availability': True
            # Add other required fields as necessary
        }
        response = self.client.post(reverse('add_rooms', kwargs={'room_type_id': self.room_type2.id}), form_data)
        # Check if the response is a redirect
        self.assertRedirects(response, reverse('show_rooms', kwargs={'room_type_id': self.room_type2.id}))



    def test_edit_rooms_access(self):
        # 发起编辑房间信息的GET请求
        response = self.client.get(
            reverse('update_rooms', kwargs={'room_type_id': self.room_type2.id, 'room_id': self.room1.id}))
        # 检查响应状态码和使用的模板
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/room_add_rooms.html')

    def test_edit_rooms_post_success(self):
        form_data = {
            'Room_number': '102',
            'availability': True
        }
        response = self.client.post(
            reverse('update_rooms', kwargs={'room_type_id': self.room_type2.id, 'room_id': self.room1.id}), form_data)
        updated_room = room.objects.get(id=self.room1.id)
        self.assertEqual(updated_room.Room_number, '101')

    def test_delete_room(self):
        response = self.client.delete(
            reverse('delete_rooms', kwargs={'room_type_id': self.room_type2.id, 'room_id': self.room1.id}))
        # 我们应该检查房间是否被删除，而不是房间类型
        self.assertFalse(room.objects.filter(id=self.room1.id).exists())

    def test_delete_room_redirection(self):
        response = self.client.delete(
            reverse('delete_rooms', kwargs={'room_type_id': self.room_type2.id, 'room_id': self.room1.id}))
        # 应该重定向到正确的页面，即该房间类型的房间列表页面
        self.assertRedirects(response, reverse('show_rooms', kwargs={'room_type_id': self.room_type2.id}),
                             msg_prefix="Successful redirect expected")

class BookingListTestCase(TestCase):
    def setUp(self):
        # 创建一个测试用户
        self.user = user.objects.create(
            username='testuser',
            password='password123',
            user_id='U123456765',
            email='email@gmail.com',
            phone='11112321'
        )

        # 创建一个酒店经理
        self.manager = hotelmanager.objects.create(
            email="manager@example.com",
            phone="+1234567890",
            password="AAAA!!0091",
            manage_id="M123456789"
        )

        # 创建一个酒店
        self.hotel = hotel.objects.create(
            manager=self.manager,
            hotel_id="H123456789",
            name="Test Hotel",
            country="Test Country",
            city="Test City",
            location="Test Location",
            postcode="G11 G11",
            email="hotel@example.com",
            phone="+0987654321",
            description="Test Description",
            facility='["WiFi", "Pool", "Gym"]',
            image="hotel_image/test.jpg"
        )

        # 创建一个房型
        self.room_type = roomtype.objects.create(
            hotel=self.hotel,
            type="Single",
            price=100,
            guests=1,
            facility='["WiFi", "Pool", "Gym"]',
            image="room_image/test.jpg"
        )

        # 创建一个房间
        self.room = room.objects.create(
            type=self.room_type,
            Room_number="101",
            availability=True
        )

        # 创建一个预订
        self.booking = booking.objects.create(
            user=self.user,
            room_number=self.room,
            ref_num="REF123",
            booking_date=timezone.now(),
            from_date=timezone.now().date(),
            to_date=(timezone.now() + timedelta(days=2)).date(),
            total_price=200,
            is_paid=True,
            reserved_name="Test User",
            reserved_phone="1234567890",
            status=1
        )

        self.booking1 = booking.objects.create(
            user=self.user,
            room_number=self.room,
            ref_num="REF123",
            booking_date=timezone.now(),
            from_date=timezone.now().date(),
            to_date=(timezone.now() + timedelta(days=2)).date(),
            total_price=200,
            is_paid=True,
            reserved_name="Test User",
            reserved_phone="1234567890",
            status=1,
            check_in_date=timezone.now(),
            check_out_date = timezone.now(),

            review_star = 3,
            review_comment = "review",
            review_date = timezone.now()
        )

        # 设置session以模拟登录状态
        session = self.client.session
        session['id'] = self.manager.id
        session['manager_id'] = self.manager.manage_id
        session.save()

    def test_booking_list(self):
        # 发起GET请求
        response = self.client.get(reverse('bookings'))
        # 检查响应状态码
        self.assertEqual(response.status_code, 200)
        # 检查模板是否被正确使用
        self.assertTemplateUsed(response, 'manager/booking.html')
        # 检查预订是否出现在页面中
        self.assertContains(response, self.booking.ref_num)

    def test_review_list(self):
        response = self.client.get(reverse('review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/reviews.html')
        self.assertContains(response, self.booking1.review_star)

    def test_reply(self):
        # 设置POST请求数据
        post_data = {
            'reply': 'Thank you for your review!'
        }
        response = self.client.post(reverse('reply_to_review', kwargs={'id': self.booking1.id}), post_data)
        self.assertRedirects(response, reverse('review'))
        updated_booking = booking.objects.get(id=self.booking1.id)
        self.assertEqual(updated_booking.reply, 'Thank you for your review!')
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your reply was successfully posted.')
        self.assertFalse(any(message.tags == 'error' for message in messages))



