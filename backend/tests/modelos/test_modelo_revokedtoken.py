import pytest
from backend.app.modelos import RevokedToken, db

def test_add_revoked_token(session):
    """
    Test adding a revoked token to the database.
    """
    jti = 'testjti123'
    revoked_token = RevokedToken(jti=jti)
    session.add(revoked_token)
    session.commit()

    assert RevokedToken.query.count() == 1
    assert RevokedToken.query.first().jti == jti

def test_is_jti_blacklisted_true(session):
    """
    Test the is_jti_blacklisted method returns True when the JTI is present in the database.
    """
    jti = 'testjti123'
    revoked_token = RevokedToken(jti=jti)
    session.add(revoked_token)
    session.commit()

    assert RevokedToken.is_jti_blacklisted(jti) is True

def test_is_jti_blacklisted_false(session):
    """
    Test the is_jti_blacklisted method returns False when the JTI is not present in the database.
    """
    jti = 'testjti123'
    assert RevokedToken.is_jti_blacklisted(jti) is False
