import unittest

from yeswehack.api import Attachment, Category


class TestAttachment(unittest.TestCase):

    def test_defaults(self):
        attachment = Attachment(
            ywh_api=None,
            id=1,
            lazy=True
        )
        self.assertEqual(1, attachment.id)
        self.assertIsNone(attachment.name)
        self.assertIsNone(attachment.original_name)
        self.assertIsNone(attachment.mime_type)
        self.assertIsNone(attachment.size)
        self.assertIsNone(attachment.url)
        self.assertIsNone(attachment.data)

    def test_arguments(self):
        attachment = Attachment(
            ywh_api=None,
            id=2,
            lazy=True,
            name="attachment",
            original_name="attachment-original-name",
            mime_type="mime/type",
            size=42069,
            url="http://foo.bar/",
            data=bytes("attachment data", encoding="utf-8"),
        )
        self.assertEqual(2, attachment.id)
        self.assertEqual("attachment", attachment.name)
        self.assertEqual("attachment-original-name", attachment.original_name)
        self.assertEqual("mime/type", attachment.mime_type)
        self.assertEqual(42069, attachment.size)
        self.assertEqual("http://foo.bar/", attachment.url)
        self.assertEqual(bytes("attachment data", encoding="utf-8"), attachment.data)


class TestCategory(unittest.TestCase):

    def test_defaults(self):
        category = Category()
        self.assertIsNone(category.name)
        self.assertIsNone(category.slug)

    def test_arguments(self):
        category = Category(
            name="Category 1",
            slug="category-1"
        )
        self.assertEqual("Category 1", category.name)
        self.assertEqual("category-1", category.slug)
