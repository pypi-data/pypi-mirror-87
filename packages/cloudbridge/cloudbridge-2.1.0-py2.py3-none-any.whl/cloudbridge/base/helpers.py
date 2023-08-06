import fnmatch
import functools
import os
import re
import sys
import traceback
from contextlib import contextmanager

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization as crypt_serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from deprecation import deprecated

import six

import cloudbridge

from ..interfaces.exceptions import InvalidParamException


def generate_key_pair():
    """
    This method generates a keypair and returns it as a tuple
    of (public, private) keys.
    The public key format is OpenSSH and private key format is PEM.
    """
    key_pair = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=2048)
    private_key = key_pair.private_bytes(
        crypt_serialization.Encoding.PEM,
        crypt_serialization.PrivateFormat.PKCS8,
        crypt_serialization.NoEncryption()).decode('utf-8')
    public_key = key_pair.public_key().public_bytes(
        crypt_serialization.Encoding.OpenSSH,
        crypt_serialization.PublicFormat.OpenSSH).decode('utf-8')
    return public_key, private_key


def filter_by(prop_name, kwargs, objs):
    """
    Utility method for filtering a list of objects by a property.
    If the given property has a non empty value in kwargs, then
    the list of objs is filtered by that value. Otherwise, the
    list of objs is returned as is.
    """
    prop_val = kwargs.pop(prop_name, None)
    if prop_val:
        if isinstance(prop_val, six.string_types):
            regex = fnmatch.translate(prop_val)
            results = [o for o in objs
                       if getattr(o, prop_name)
                       and re.search(regex, getattr(o, prop_name))]
        else:
            results = [o for o in objs
                       if getattr(o, prop_name) == prop_val]
        return results
    else:
        return objs


def generic_find(filter_names, kwargs, objs):
    """
    Utility method for filtering a list of objects by a list of filters.
    """
    matches = objs
    for name in filter_names:
        matches = filter_by(name, kwargs, matches)

    # All kwargs should have been popped at this time.
    if len(kwargs) > 0:
        raise InvalidParamException(
            "Unrecognised parameters for search: %s. Supported attributes: %s"
            % (kwargs, filter_names))

    return matches


@contextmanager
def cleanup_action(cleanup_func):
    """
    Context manager to carry out a given
    cleanup action after carrying out a set
    of tasks, or when an exception occurs.
    If any errors occur during the cleanup
    action, those are ignored, and the original
    traceback is preserved.

    :params func: This function is called if
    an exception occurs or at the end of the
    context block. If any exceptions raised
        by func are ignored.
    Usage:
        with cleanup_action(lambda e: print("Oops!")):
            do_something()
    """
    try:
        yield
    except Exception:
        ex_class, ex_val, ex_traceback = sys.exc_info()
        try:
            cleanup_func()
        except Exception as e:
            print("Error during exception cleanup: {0}".format(e))
            traceback.print_exc()
        six.reraise(ex_class, ex_val, ex_traceback)
    try:
        cleanup_func()
    except Exception as e:
        print("Error during cleanup: {0}".format(e))
        traceback.print_exc()


def get_env(varname, default_value=None):
    """
    Return the value of the environment variable or default_value.

    This is a helper method that wraps ``os.environ.get`` to ensure type
    compatibility across py2 and py3. For py2, any value obtained from an
    environment variable, ensure ``unicode`` type and ``str`` for py3. The
    casting is done only for string variables.

    :type varname: ``str``
    :param varname: Name of the environment variable for which to check.

    :param default_value: Return this value is the env var is not found.
                          Defaults to ``None``.

    :return: Value of the supplied environment if found; value of
             ``default_value`` otherwise.
    """
    value = os.environ.get(varname, default_value)
    if isinstance(value, six.string_types) and not isinstance(
            value, six.text_type):
        return six.u(value)
    return value


# Alias deprecation decorator, following:
# https://stackoverflow.com/questions/49802412/
# how-to-implement-deprecation-in-python-with-argument-alias
def deprecated_alias(**aliases):
    def deco(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            rename_kwargs(f.__name__, kwargs, aliases)
            return f(*args, **kwargs)
        return wrapper
    return deco


def rename_kwargs(func_name, kwargs, aliases):
    for alias, new in aliases.items():
        if alias in kwargs:
            if new in kwargs:
                raise InvalidParamException(
                    '{} received both {} and {}'.format(func_name, alias, new))
            # Manually invoke the deprecated decorator with an empty lambda
            # to signal deprecation
            deprecated(deprecated_in='1.1',
                       removed_in='2.0',
                       current_version=cloudbridge.__version__,
                       details='{} is deprecated, use {} instead'.format(
                           alias, new))(lambda: None)()
            kwargs[new] = kwargs.pop(alias)


NON_ALPHA_NUM = re.compile(r"[^A-Za-z0-9]+")


def to_resource_name(value, replace_with="-"):
    """
    Converts a given string to a valid resource name by stripping
    all characters that are not alphanumeric.

    :param value: the value to strip
    :param replace_with: the value to replace mismatching characters with
    :return: a string with all mismatching characters removed.
    """
    val = re.sub(NON_ALPHA_NUM, replace_with, value)
    return val.strip("-")
