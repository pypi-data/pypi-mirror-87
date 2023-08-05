import typing

from enum import Enum


class UserRole(Enum):
    """
    Enum representing the Role that a user could have

    A user can have one or more roles at the same time (based on CAS attributes)
    """
    STUDENT = 1 << 0
    LECTURER = 1 << 1
    ADMIN = 1 << 2
    CTI = 1 << 3

    @staticmethod
    def assert_user_role(object):
        """
        Check if a given object or value is instance of UserRole

        Throws AssertionError on invalid instance
        """
        
        assert isinstance(object, UserRole), f"Unknown role {object}"

    @staticmethod
    def assert_user_roles(iterable):
        """
        Check if a given list of object or value is instance of UserRole

        Throws AssertionError on invalid instance
        """
        assert isinstance(iterable, typing.Iterable), f"Not iterable {list}"

        for item in iterable:
            UserRole.assert_user_role(item)
