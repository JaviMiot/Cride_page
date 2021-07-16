"""invitations test"""

from django.test import TestCase
from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.test import APITestCase

from cride.circles.models import Circle, Invitation, Membership
from cride.users.models import Users, Profiles


class InvitationsManagerTestCase(TestCase):
    """Invitatiosn manager teste case"""

    def setUp(self):
        """test case setup"""
        self.user = Users.objects.create(
            first_name='javier',
            last_name='manobanda',
            email='javi@gmail',
            username='javim',
            password='javi123456789'
        )

        self.circle = Circle.objects.create(
            name='Facultad Mecatrónica',
            slug_name='fciencias',
            about='Grupo oficial de mecatrónica',
            verified=True,
        )

    def test_code_generations(self):
        """random coces shoul be generatedt automatically"""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )

        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        """if the code is given, there´s no need to create a new one"""
        code = 'holamundo'
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code,
        )

        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """if given code is not unique, a new one must be generated."""
        code = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
        ).code

        # * created a onother invitations white the past code

        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code,
        )

        self.assertNotEqual(code, invitation.code)


class MemberInvitationsAPITestCase(APITestCase):

    def setUp(self):
        """test case setup"""
        self.user = Users.objects.create(
            first_name='javier',
            last_name='manobanda',
            email='javi@gmail',
            username='javim',
            password='javi123456789'
        )

        self.circle = Circle.objects.create(
            name='Facultad Mecatrónica',
            slug_name='fciencias',
            about='Grupo oficial de mecatrónica',
            verified=True,
        )

        self.profile = Profiles.objects.create(
            users=self.user,
        )

        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_inv=10,
        )

        self.token = Token.objects.create(
            user=self.user
        ).key

        self.url = f'/circles/{self.circle.slug_name}/members/{self.user.username}/invitations/'

        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.token}')

    def test_response_success(self):
        """verified request succeeded"""

        request = self.client.get(self.url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitations_creations(self):
        """verifica que las invitaciones creadas no existan previamente"""
        # * invitations in db must be 0

        self.assertEqual(Invitation.objects.count(), 0)

        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # * verify new invitations were created
        invitations = Invitation.objects.filter(issued_by=self.user)
        self.assertEqual(Invitation.objects.count(), self.membership.remaining_inv)

        for invitation in invitations:
            self.assertIn(invitation.code, request.data['invitations'])
