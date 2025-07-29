import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from eco_bot.repositories.models import Base
from eco_bot.repositories.db import engine

@pytest.fixture(scope='session', autouse=True)
def init_test_db():
    Base.metadata.create_all(bind=engine)
