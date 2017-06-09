from django.test import TestCase, RequestFactory
from django.test.client import Client

from django_fine_uploader import widgets


class TestDjango_fine_uploader_form(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_fineuploaderwidget_no_attrs(self):
        """Test the widget without attrs.
        """
        widget = widgets.FineUploaderWidget()

        self.assertEqual(widget.itemLimit, 0)
        self.assertEqual(widget.input_type, 'hidden')

    def test_fineuploaderwidget_attrs_admin(self):
        """Test the widget with attrs contains admin value.
        """
        widget = widgets.FineUploaderWidget(attrs={'admin': True})

        self.assertEqual(widget.input_type, '')

    def test_fineuploaderwidget_attrs_itemLimit(self):
        """Test the widget with attrs contains itemLimit value.
        """
        itemLimit = 2
        widget = widgets.FineUploaderWidget(attrs={'itemLimit': itemLimit})

        self.assertEqual(widget.itemLimit, itemLimit)
