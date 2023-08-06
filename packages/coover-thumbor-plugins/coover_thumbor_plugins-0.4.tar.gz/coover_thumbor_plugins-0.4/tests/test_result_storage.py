# coding: utf-8

# Copyright (c) 2015, thumbor-community
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

from datetime import datetime, timedelta
from hashlib import sha1
from unittest import TestCase

import botocore.session
from dateutil.tz import tzutc
from thumbor.config import Config
from thumbor.context import Context
from tornado.testing import gen_test

from fixtures.storage_fixture import IMAGE_BYTES, get_server, s3_bucket
from coover_thumbor_plugins.result_storages.s3_storage import Storage
from tests import S3MockedAsyncTestCase


class Request(object):
    url = None


class S3StorageTestCase(S3MockedAsyncTestCase):

    @gen_test
    def test_can_store_image(self):
        config = Config(TC_AWS_RESULT_STORAGE_BUCKET=s3_bucket)
        ctx = Context(config=config, server=get_server('ACME-SEC'))
        ctx.request = Request
        ctx.request.url = 'foo/my-image.jpg'

        storage = Storage(ctx)

        yield storage.put(IMAGE_BYTES)

        client = botocore.session.get_session().create_client('s3')
        response = client.get_object(Bucket=s3_bucket, Key="foo/my-image.jpg")

        self.assertEqual(response['Body'].read(), IMAGE_BYTES)

    @gen_test
    def test_can_store_image_randomly(self):
        config = Config(TC_AWS_RESULT_STORAGE_BUCKET=s3_bucket, TC_AWS_RANDOMIZE_KEYS=True)
        ctx = Context(config=config, server=get_server('ACME-SEC'))
        ctx.request = Request
        ctx.request.url = 'foo/my-image.jpg'

        storage = Storage(ctx)

        yield storage.put(IMAGE_BYTES)

        expected_path = '/'.join([sha1("foo/my-image.jpg".encode('utf-8')).hexdigest(), 'foo/my-image.jpg'])

        client = botocore.session.get_session().create_client('s3')
        response = client.get_object(Bucket=s3_bucket, Key=expected_path)

        self.assertEqual(response['Body'].read(), IMAGE_BYTES)

    @gen_test
    def test_can_get_image(self):
        config = Config(TC_AWS_RESULT_STORAGE_BUCKET=s3_bucket)
        ctx = Context(config=config, server=get_server('ACME-SEC'))
        ctx.request = Request
        ctx.request.url = 'my-image-2.jpg'

        storage = Storage(ctx)
        yield storage.put(IMAGE_BYTES)

        topic = yield storage.get()

        self.assertEqual(topic.buffer, IMAGE_BYTES)

    @gen_test
    def test_can_get_randomized_image(self):
        config = Config(TC_AWS_RESULT_STORAGE_BUCKET=s3_bucket, TC_AWS_RANDOMIZE_KEYS=True)
        ctx = Context(config=config, server=get_server('ACME-SEC'))
        ctx.request = Request
        ctx.request.url = 'my-image-2.jpg'

        storage = Storage(ctx)
        yield storage.put(IMAGE_BYTES)

        topic = yield storage.get()

        self.assertEqual(topic.buffer, IMAGE_BYTES)

    @gen_test
    def test_can_get_image_with_metadata(self):
        config = Config(TC_AWS_RESULT_STORAGE_BUCKET=s3_bucket, TC_AWS_STORE_METADATA=True)
        ctx = Context(config=config, server=get_server('ACME-SEC'))
        ctx.headers = {'Content-Type': 'image/webp', 'Some-Other-Header': 'doge-header'}
        ctx.request = Request
        ctx.request.url = 'my-image-meta.jpg'

        storage = Storage(ctx)
        yield storage.put(IMAGE_BYTES)

        file_abspath = storage._normalize_path(ctx.request.url)
        topic = yield storage.get(file_abspath)

        self.assertIn('Some-Other-Header', topic.metadata['Metadata'])
        self.assertEqual(topic.metadata['Metadata']['Content-Type'], 'image/webp')
        self.assertEqual(topic.buffer, IMAGE_BYTES)


class ExpiredTestCase(TestCase):

    @property
    def expired_enabled(self):
        return Storage(Context(config=Config(RESULT_STORAGE_EXPIRATION_SECONDS=3600)))

    def test_should_check_invalid_key(self):
        self.assertTrue(self.expired_enabled.is_expired(None))
        self.assertTrue(self.expired_enabled.is_expired(False))
        self.assertTrue(self.expired_enabled.is_expired(dict()))
        self.assertTrue(self.expired_enabled.is_expired({'Error': ''}))

    def test_should_tell_when_not_expired(self):
        key = {
            'LastModified': datetime.now(tzutc()),
            'Body': 'foobar',
        }
        self.assertFalse(self.expired_enabled.is_expired(key))

    def test_should_tell_when_expired(self):
        key = {
            'LastModified': (datetime.now(tzutc()) - timedelta(seconds=3601)),
            'Body': 'foobar',
        }
        self.assertTrue(self.expired_enabled.is_expired(key))

    def test_expire_disabled_should_not_tell_when_expired(self):
        topic = Storage(Context(config=Config(RESULT_STORAGE_EXPIRATION_SECONDS=0)))
        key = {
            'LastModified': (datetime.now(tzutc()) - timedelta(seconds=3601)),
            'Body': 'foobar',
        }
        self.assertFalse(topic.is_expired(key))


class PrefixTestCase(TestCase):

    def test_should_check_invalid_key(self):
        config = Config(TC_AWS_RESULT_STORAGE_BUCKET=s3_bucket, TC_AWS_RESULT_STORAGE_ROOT_PATH='tata')
        ctx = Context(config=config, server=get_server('ACME-SEC'))

        storage = Storage(ctx)

        topic = storage._normalize_path('toto')

        self.assertEqual(topic, "tata/toto")
