#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import json

from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from django_fine_uploader import views, settings, fineuploader
from django_fine_uploader.forms import FineUploaderUploadForm


class TestDjango_fine_uploader_form(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_fineuploaderuploadform(self):
        """Test the FineUploaderUploadForm.
        The form should requires
        data: qquuid, qqfilename
        files: qqfile
        """
        # test_file_object = open("test_file.txt", 'rb').read()
        test_file = SimpleUploadedFile("test_file.txt", "test".encode())
        form = FineUploaderUploadForm()
        assert form.is_valid() is False
        form_data = {
            'qquuid': '11111111-2222-3333-4444-555555555555',
            'qqfilename': test_file.name,
            'qqadmin': False,
        }
        form_files = {
            'qqfile': test_file,
        }
        form = FineUploaderUploadForm(data=form_data, files=form_files)
        assert form.is_valid() is True
        # self.assertTrue(form.is_valid())

    def test_fineuploaderview_no_admin(self):
        """Test the view with qqadmin is set to False.
        """
        test_file = SimpleUploadedFile("test_file.txt", "test".encode())
        post_data = {
            'qqfile': test_file,
            'qquuid': '11111111-2222-3333-4444-555555555555',
            'qqfilename': test_file.name,
            # 'qqadmin': False,
        }
        file_path = '{}/{}/{}'.format(
            os.getcwd(),
            settings.UPLOAD_DIR,
            post_data['qquuid'],
            post_data['qqfilename']
        )

        request = self.factory.post(
            reverse('django_fine_uploader:upload'),
            post_data
        )
        response = views.FineUploaderView.as_view()(request)
        # Before Python 3.6 json.loads cannot accept bytes input.
        # The input needs to be decoded to str before loads to json.
        if sys.version_info[0] == 3 and sys.version_info < (3, 6):
            result = json.loads(response.content.decode('utf-8'))
        else:
            result = json.loads(response.content)

        print(result)
        assert response.status_code == 200
        assert result['success'] == True
        assert result['path'] == '%s%s/%s' % (settings.UPLOAD_DIR, post_data['qquuid'], post_data['qqfilename'])
        assert result['uuid'] == post_data['qquuid']
        assert os.path.exists(file_path) == True
        # self.assertEqual(response.status_code, 201)
        # self.assertEqual(result['success'], True)
        # self.assertTrue(os.path.exists(file_path))

    def test_fineuploaderview_admin(self):
        """Test the view with qqadmin is set to True.
        """
        test_file = SimpleUploadedFile("test_file.txt", "test".encode())
        post_data = {
            'qqfile': test_file,
            'qquuid': '11111111-2222-3333-4444-555555555555',
            'qqfilename': test_file.name,
            'qqadmin': True,
        }
        file_path = '{}/{}/{}'.format(
            os.getcwd(),
            settings.UPLOAD_DIR,
            post_data['qquuid'],
            post_data['qqfilename']
        )
        print(reverse('django_fine_uploader:upload'))
        request = self.factory.post(
            reverse('django_fine_uploader:upload'),
            post_data
        )
        response = views.FineUploaderView.as_view()(request)
        # Before Python 3.6 json.loads cannot accept bytes input.
        # The input needs to be decoded to str before loads to json.
        if sys.version_info[0] == 3 and sys.version_info < (3, 6):
            result = json.loads(response.content.decode('utf-8'))
        else:
            result = json.loads(response.content)

        assert response.status_code == 200
        assert result['success'] == True
        assert result['path'] == '%s%s/%s' % (settings.UPLOAD_DIR, post_data['qquuid'], post_data['qqfilename'])
        assert result['uuid'] == post_data['qquuid']
        assert os.path.exists(file_path) == True

    def tearDown(self):
        path = '{}/{}'.format(os.getcwd(), settings.UPLOAD_DIR)
        if os.path.isdir(path):
            shutil.rmtree(path)
