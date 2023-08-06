# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2020 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
App Handler
"""

from __future__ import unicode_literals, absolute_import

# import re

import six
from sqlalchemy import orm

from rattail.util import load_object


class AppHandler(object):
    """
    Base class and default implementation for top-level Rattail app handler.

    aka. "the handler to handle all handlers"

    aka. "one handler to bind them all"
    """

    def __init__(self, config):
        self.config = config

    def get_board_handler(self, **kwargs):
        if not hasattr(self, 'board_handler'):
            from rattail.board import get_board_handler
            self.board_handler = get_board_handler(self.config, **kwargs)
        return self.board_handler

    def get_clientele_handler(self, **kwargs):
        if not hasattr(self, 'clientele_handler'):
            from rattail.clientele import get_clientele_handler
            self.clientele_handler = get_clientele_handler(self.config, **kwargs)
        return self.clientele_handler

    def get_employment_handler(self, **kwargs):
        if not hasattr(self, 'employment_handler'):
            from rattail.employment import get_employment_handler
            self.employment_handler = get_employment_handler(self.config, **kwargs)
        return self.employment_handler

    def get_session(self, obj):
        """
        Returns the SQLAlchemy session with which the given object is
        associated.  Simple convenience wrapper around
        ``sqlalchemy.orm.object_session()``.
        """
        return orm.object_session(obj)

    def phone_number_is_invalid(self, number):
        """
        This method should validate the given phone number string, and if the
        number is *not* considered valid, this method should return the reason
        as string.  If the number is valid, returns ``None``.
        """
        from rattail.db.util import normalize_phone_number, validate_phone_number

        # strip non-numeric chars, and make sure we have 10 left
        normal = normalize_phone_number(number)
        if len(normal) != 10:
            return "Phone number must have 10 digits"

        # run it through the "traditional" validation, from FormEncode
        try:
            number = validate_phone_number(number, error=True)
        except Exception as error:
            return six.text_type(error)


class GenericHandler(object):
    """
    Base class for misc. "generic" feature handlers.

    Most handlers which exist for sake of business logic, should inherit from
    this.
    """

    def __init__(self, config, **kwargs):
        self.config = config
        self.enum = self.config.get_enum()
        self.model = self.config.get_model()
        self.app = self.config.get_app()

    def get_session(self, obj):
        """
        Convenience wrapper around :meth:`AppHandler.get_session()`.
        """
        return self.app.get_session(obj)


def make_app(config, **kwargs):
    """
    Create and return the configured :class:`AppHandler` instance.
    """
    spec = config.get('rattail', 'app.handler')
    if spec:
        factory = load_object(spec)
    else:
        factory = AppHandler
    return factory(config, **kwargs)
