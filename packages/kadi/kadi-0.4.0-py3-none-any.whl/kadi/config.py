# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import socket

from celery.schedules import crontab

import kadi.lib.constants as const


class BaseConfig:
    """Base configuration."""

    ##########
    # Celery #
    ##########

    CELERY_BROKER_TRANSPORT_OPTIONS = {
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.5,
    }

    CELERY_BROKER_URL = "redis://"

    CELERY_TASK_ANNOTATIONS = {
        "kadi.records.merge_chunks": {"soft_time_limit": const.ONE_HOUR},
        "kadi.records.package_files": {"soft_time_limit": const.ONE_HOUR},
        "kadi.records.publish_record": {"soft_time_limit": const.ONE_HOUR},
        "kadi.notifications.send_mail": {"max_retries": 10},
    }

    CELERY_WORKER_REDIRECT_STDOUTS = False

    CELERY_BEAT_SCHEDULE = {
        "clean-files-periodically": {
            "task": "kadi.records.clean_files",
            "schedule": crontab(minute="*/30"),
        },
        "clean-resources-periodically": {
            "task": "kadi.main.clean_resources",
            "schedule": crontab(minute="*/30"),
        },
    }

    #########
    # Flask #
    #########

    SESSION_COOKIE_DOMAIN = False

    SESSION_COOKIE_NAME = "kadi_session"

    SESSION_COOKIE_SAMESITE = "Lax"

    ###########
    # Limiter #
    ###########

    RATELIMIT_HEADERS_ENABLED = True

    RATELIMIT_STORAGE_URL = "redis://"

    #########
    # Login #
    #########

    # Makes a stolen cookie much harder to use. Should work without problems as we do
    # not use the remember cookie.
    SESSION_PROTECTION = "strong"

    ##############
    # SQLAlchemy #
    ##############

    SQLALCHEMY_DATABASE_URI = None

    # Pessimistic disconnect handling.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ############
    # Talisman #
    ############

    FLASK_TALISMAN_OPTIONS = {
        "content_security_policy": {
            "default-src": "'self'",
            "frame-ancestors": "'self'",
            "frame-src": "'self'",
            "img-src": ["'self'", "data:"],
            "script-src": ["'self'", "'unsafe-eval'"],
            "style-src": ["'self'", "'unsafe-inline'", "data:"],
        },
        "content_security_policy_nonce_in": "script-src",
        "force_https": False,
        "session_cookie_secure": False,
    }

    ###########
    # WTForms #
    ###########

    WTF_CSRF_TIME_LIMIT = None

    ########
    # Kadi #
    ########

    API_SCOPES = {"user": ["read"]}

    API_VERSIONS = ["1.0"]

    AUTH_PROVIDERS = [{"type": "local"}]

    AUTH_PROVIDER_TYPES = {
        "local": {
            "provider": "kadi.modules.accounts.providers.LocalProvider",
            "identity": "kadi.modules.accounts.models.LocalIdentity",
            "form": "kadi.modules.accounts.forms.CredentialsLoginForm",
        },
        "ldap": {
            "provider": "kadi.modules.accounts.providers.LDAPProvider",
            "identity": "kadi.modules.accounts.models.LDAPIdentity",
            "form": "kadi.modules.accounts.forms.CredentialsLoginForm",
        },
        "shib": {
            "provider": "kadi.modules.accounts.providers.ShibProvider",
            "identity": "kadi.modules.accounts.models.ShibIdentity",
            "form": "kadi.modules.accounts.forms.ShibLoginForm",
        },
    }

    BACKEND_TRANSLATIONS_PATH = os.path.join("{root_path}", "translations")

    EXPERIMENTAL_FEATURES = True

    FOOTER_NAV_ITEMS = []

    FRONTEND_TRANSLATIONS_PATH = os.path.join("{root_path}", "assets", "translations")

    IMAGE_MIMETYPES = ["image/jpeg", "image/png"]

    INACTIVE_FILES_MAX_AGE = const.ONE_DAY

    LICENSE_URL = "https://licenses.opendefinition.org/licenses/groups/all.json"

    LOCALES = {
        "de": "Deutsch (beta)",
        "en": "English",
    }

    LOCALE_COOKIE_SECURE = False

    LOCALE_DEFAULT = "en"

    MAIL_ERROR_LOGS = []

    MAIL_NO_REPLY = "no-reply@" + socket.getfqdn()

    MANIFEST_PATH = os.path.join("{static_path}", "manifest.json")

    MAX_IMAGE_SIZE = 10 * const.ONE_MB

    MAX_UPLOAD_SIZE = const.ONE_GB

    MAX_UPLOAD_USER_QUOTA = 10 * const.ONE_GB

    MIGRATIONS_PATH = os.path.join("{root_path}", "migrations")

    MISC_UPLOADS_PATH = None

    PREVIEW_MAX_SIZE = 10 * const.ONE_MB

    PREVIEW_MIMETYPES = {
        "archive": [
            "application/zip",
            "application/gzip",
            "application/x-tar",
            "application/x-bzip2",
        ],
        "image": ["image/jpeg", "image/png"],
        "pdf": ["application/pdf"],
    }

    PLUGIN_CONFIG = {}

    PLUGIN_ENTRYPOINT = "kadi_plugins"

    PLUGINS = []

    PROXY_FIX_ENABLE = False

    PROXY_FIX_HEADERS = {
        "x_for": 1,
        "x_proto": 1,
        "x_host": 1,
        "x_port": 0,
        "x_prefix": 0,
    }

    # Global rate limit for anonymous users.
    RATELIMIT_ANONYMOUS_USER = "50/minute;5/second"

    # Global rate limit for authenticated users.
    RATELIMIT_AUTHENTICATED_USER = "1000/minute;100/second"

    RATELIMIT_IP_WHITELIST = ["127.0.0.1"]

    RESOURCES_MAX_AGE = const.ONE_WEEK

    SENTRY_DSN = None

    SMTP_HOST = "localhost"

    SMTP_PASSWORD = ""

    SMTP_PORT = 25

    SMTP_TIMEOUT = 60

    SMTP_USE_TLS = False

    SMTP_USERNAME = ""

    STORAGE_PATH = None

    SYSTEM_ROLES = {
        "admin": {
            "record": ["create", "read", "update", "link", "permissions", "delete"],
            "collection": ["create", "read", "update", "link", "permissions", "delete"],
            "group": ["create", "read", "update", "members", "delete"],
            "template": ["create", "read", "update", "permissions", "delete"],
        },
        "member": {
            "record": ["create"],
            "collection": ["create"],
            "group": ["create"],
            "template": ["create"],
        },
        "guest": {},
    }

    TEMPORARY_FILES_MAX_AGE = const.ONE_HOUR

    UPLOAD_CHUNK_SIZE = 10 * const.ONE_MB

    UPLOADS_MAX_AGE = const.ONE_DAY


class ProductionConfig(BaseConfig):
    """Production configuration."""

    #########
    # Flask #
    #########

    FLASK_SKIP_DOTENV = True

    PREFERRED_URL_SCHEME = "https"

    SESSION_COOKIE_SECURE = True

    USE_X_SENDFILE = True

    ########
    # Kadi #
    ########

    EXPERIMENTAL_FEATURES = False

    LOCALE_COOKIE_SECURE = True


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    #########
    # Flask #
    #########

    SECRET_KEY = "s3cr3t"

    SERVER_NAME = "localhost:5000"

    ##############
    # SQLAlchemy #
    ##############

    SQLALCHEMY_DATABASE_URI = "postgresql://kadi:kadi@localhost:5432/kadi"

    ########
    # Kadi #
    ########

    AUTH_PROVIDERS = [{"type": "local", "allow_registration": True}]

    MISC_UPLOADS_PATH = os.path.join("{instance_path}", "uploads")

    SMTP_PORT = 8025

    STORAGE_PATH = os.path.join("{instance_path}", "storage")


class TestingConfig(BaseConfig):
    """Testing configuration."""

    ##########
    # Celery #
    ##########

    CELERY_BROKER_URL = None

    #################
    # Elasticsearch #
    #################

    ELASTICSEARCH_HOSTS = None

    #########
    # Flask #
    #########

    FLASK_SKIP_DOTENV = True

    SECRET_KEY = "s3cr3t"

    SERVER_NAME = "localhost"

    TESTING = True

    ###########
    # Limiter #
    ###########

    RATELIMIT_STORAGE_URL = "memory://"

    ##############
    # SQLAlchemy #
    ##############

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://kadi_test:kadi_test@localhost:5432/kadi_test"
    )

    ###########
    # WTForms #
    ###########

    WTF_CSRF_ENABLED = False

    ########
    # Kadi #
    ########

    AUTH_PROVIDERS = [
        {"type": "local", "allow_registration": True},
        {"type": "ldap"},
        {
            "type": "shib",
            "idps": [{"name": "Test", "entity_id": "https://idp.example.com"}],
        },
    ]


configs = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
