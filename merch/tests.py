from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import TournamentConfig, TournamentRegistration


class TournamentConfigTest(TestCase):
    def test_get_config_returns_seeded_config(self):
        config = TournamentConfig.get_config()
        self.assertEqual(config.pk, 1)
        self.assertEqual(TournamentConfig.objects.count(), 1)

    def test_spots_remaining(self):
        TournamentConfig.objects.update_or_create(pk=1, defaults={'max_participants': 5})
        config = TournamentConfig.get_config()
        self.assertFalse(config.is_full)
        self.assertEqual(config.spots_remaining, 5)

        for i in range(5):
            TournamentRegistration.objects.create(
                full_name=f'Player {i}',
                gender='MALE',
                gamer_tag=f'TAG_{i}',
                email=f'player{i}@test.com',
            )
            config.refresh_from_db()

        self.assertTrue(config.is_full)
        self.assertEqual(config.spots_remaining, 0)

    def test_unlimited_spots(self):
        TournamentConfig.objects.update_or_create(pk=1, defaults={'max_participants': 0})
        config = TournamentConfig.get_config()
        self.assertFalse(config.is_full)
        self.assertIsNone(config.spots_remaining)


class TournamentRegistrationModelTest(TestCase):
    def setUp(self):
        TournamentConfig.objects.update_or_create(pk=1, defaults={'max_participants': 2})

    def test_gamer_tag_uppercased(self):
        reg = TournamentRegistration.objects.create(
            full_name='John Doe',
            gender='MALE',
            gamer_tag='eyt_legend',
            email='john@test.com',
        )
        self.assertEqual(reg.gamer_tag, 'EYT_LEGEND')

    def test_full_tournament_rejects_new_registration(self):
        for i in range(2):
            TournamentRegistration.objects.create(
                full_name=f'Player {i}',
                gender='FEMALE',
                gamer_tag=f'PLY_{i}',
                email=f'player{i}@test.com',
            )
        with self.assertRaises(ValidationError):
            TournamentRegistration.objects.create(
                full_name='Extra Player',
                gender='OTHER',
                gamer_tag='EXTRA',
                email='extra@test.com',
            )


class TournamentPagesTest(TestCase):
    def setUp(self):
        TournamentConfig.objects.update_or_create(pk=1, defaults={
            'tournament_name': 'EYT Test Cup',
            'fee_amount': 5000,
            'currency': 'NGN',
            'account_name': 'EYT Gaming',
            'account_number': '0123456789',
            'bank_name': 'Test Bank',
            'max_participants': 10,
        })

    def test_tournament_page_renders_qr(self):
        response = self.client.get(reverse('merch:tournament'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<svg', status_code=200)
        self.assertContains(response, 'EYT Test Cup')
        self.assertContains(response, '0123456789')

    def test_register_page_renders_form(self):
        response = self.client.get(reverse('merch:tournament_register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Full Name')
        self.assertContains(response, 'Gamer Tag')
        self.assertContains(response, '0123456789')

    def test_successful_registration(self):
        response = self.client.post(reverse('merch:tournament_register'), {
            'full_name': 'Jane Doe',
            'gender': 'FEMALE',
            'gamer_tag': 'jane_doe',
            'email': 'jane@test.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TournamentRegistration.objects.count(), 1)
        reg = TournamentRegistration.objects.first()
        self.assertEqual(reg.payment_status, 'PENDING')
        self.assertEqual(reg.gamer_tag, 'JANE_DOE')

    def test_duplicate_gamer_tag_rejected(self):
        TournamentRegistration.objects.create(
            full_name='Jane Doe',
            gender='FEMALE',
            gamer_tag='jane_doe',
            email='jane@test.com',
        )
        response = self.client.post(reverse('merch:tournament_register'), {
            'full_name': 'Other Player',
            'gender': 'MALE',
            'gamer_tag': 'jane_doe',
            'email': 'other@test.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'has already been registered')
        self.assertEqual(TournamentRegistration.objects.count(), 1)

    def test_duplicate_email_rejected(self):
        TournamentRegistration.objects.create(
            full_name='Jane Doe',
            gender='FEMALE',
            gamer_tag='jane_doe',
            email='jane@test.com',
        )
        response = self.client.post(reverse('merch:tournament_register'), {
            'full_name': 'Other Player',
            'gender': 'MALE',
            'gamer_tag': 'other_p',
            'email': 'jane@test.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already been registered for the tournament')
        self.assertEqual(TournamentRegistration.objects.count(), 1)

    def test_required_fields(self):
        response = self.client.post(reverse('merch:tournament_register'), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertEqual(TournamentRegistration.objects.count(), 0)

    def test_full_portal_blocks_registration(self):
        TournamentConfig.objects.update_or_create(pk=1, defaults={'max_participants': 2})
        for i in range(2):
            TournamentRegistration.objects.create(
                full_name=f'Player {i}',
                gender='MALE',
                gamer_tag=f'GBL_{i}',
                email=f'gbl{i}@test.com',
            )
        response = self.client.get(reverse('merch:tournament_register'))
        self.assertContains(response, 'Tournament Full')
        response = self.client.post(reverse('merch:tournament_register'), {
            'full_name': 'Late Player',
            'gender': 'MALE',
            'gamer_tag': 'LATE_P',
            'email': 'late@test.com',
        })
        self.assertEqual(TournamentRegistration.objects.count(), 2)

    def test_closed_portal_blocks_registration(self):
        TournamentConfig.objects.update_or_create(pk=1, defaults={'is_registration_open': False})
        response = self.client.get(reverse('merch:tournament_register'))
        self.assertContains(response, 'Registration Closed')
        response = self.client.post(reverse('merch:tournament_register'), {
            'full_name': 'Late Player',
            'gender': 'MALE',
            'gamer_tag': 'LATE_P',
            'email': 'late@test.com',
        })
        self.assertEqual(TournamentRegistration.objects.count(), 0)