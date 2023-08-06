# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['SchemaHelpersTypeCase::test_create_fields 1'] = [
    'username',
    'password',
    'email',
    'is_superuser',
    'first_name',
    'last_name',
    'is_staff',
    'is_active'
]

snapshots['SchemaHelpersTypeCase::test_create_fields 2'] = [
    'key',
    'name',
    'created_at',
    'updated_at',
    'data',
    'user',
    'geojson'
]

snapshots['SchemaHelpersTypeCase::test_query_fields 1'] = [
    'id',
    'username',
    'email',
    'is_superuser',
    'first_name',
    'last_name',
    'is_staff',
    'is_active',
    'date_joined'
]

snapshots['SchemaHelpersTypeCase::test_query_fields 2'] = [
    'key',
    'name',
    'created_at',
    'updated_at',
    'data',
    'user',
    'geojson',
    'geo_collection'
]

snapshots['SchemaHelpersTypeCase::test_update_fields 1'] = [
    'id',
    'username',
    'password',
    'email',
    'is_superuser',
    'first_name',
    'last_name',
    'is_staff',
    'is_active'
]

snapshots['SchemaHelpersTypeCase::test_update_fields 2'] = [
    'key',
    'name',
    'created_at',
    'updated_at',
    'data',
    'user',
    'geojson'
]

snapshots['SchemaHelpersTypeCase::test_update_fields_for_create_or_update 1'] = {
    'defaults': {
        'email': 'dino@barn.farm',
        'first_name': 'T',
        'last_name': 'Rex',
        'password': 'pbkdf2_sha256$100000$not_random$kd71bQn3ng/uGJ/MfuNbDORGyd6XCsWpTCdFOtr+5F0=',
        'username': 'dino'
    }
}

snapshots['SchemaHelpersTypeCase::test_update_fields_for_create_or_update 2'] = {
    'defaults': {
        'data': {
            'example': 2.2
        },
        'key': 'fooKey',
        'name': 'Foo Name',
        'user_id': 5
    }
}
