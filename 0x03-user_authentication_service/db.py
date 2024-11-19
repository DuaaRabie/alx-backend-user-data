#!/usr/bin/env python3
"""
DB class
"""
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import MultipleResultsFound

from user import Base, User

from typing import Any, Union


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # Create the engine without echo
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ add user to the database """
        new_user =\
            User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Any) -> User:
        """
        Find a user by arbitrary keyword arguments
        Args:
            kwargs: Arbitrary keyword arguments to filter the user table
        Returns:
            user: The first user that matches the provided filters
        Raises:
            NoResultFound: If no user is found with the given attributes.
            InvalidRequestError: If an invalid query is attempted
        """
        try:
            if kwargs:
                user = self._session.query(User).filter_by(**kwargs).one()
                if user is not None:
                    return user
        except MultipleResultsFound:
            return self._session.query(User).filter_by(**kwargs).first()
        except NoResultFound:
            raise NoResultFound("Not found")
        except InvalidRequestError as e:
            raise InvalidRequestError("{e}")

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """
        To locate the user to update
        Args:
            user_id: The user's id for user needs update.
            kwargs: Arbitrary keyword arguments to be updated.
        Returns:
            None
        Raises:
             ValueError: If an argument that does not correspond
             to a user attribute is passed.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError("ValueError")
            setattr(user, key, value)
        self._session.commit()
