import os
import pytest
from sqlalchemy import create_engine
import psycopg2
postgresql_dict = {}
def pytest_configure(config):
    print("inside pytest_configure")

@pytest.fixture(scope="session", autouse= True)
def postgres_db_engine(request):
    print("\n session fixture")
    global  postgresql_dict
    postgresql_dict["db_url"] = os.getenv("postgresql_dict.db_url")
    postgresql_dict["db_name"] = os.getenv("postgresql_dict.db_name")
    postgresql_dict["db_username"] = os.getenv("postgresql_dict.db_username")
    postgresql_dict["db_password"] = os.getenv("postgresql_dict.db_password")
    postgresql_dict["db_dialect"] = os.getenv("postgresql_dict.db_dialect")
    postgresql_dict["db_dbapi"] = os.getenv("postgresql_dict.db_dbapi")

    connection_string = f'{postgresql_dict["db_dialect"]}+{postgresql_dict["db_dbapi"]}://{postgresql_dict["db_username"]}:{postgresql_dict["db_password"]}@{postgresql_dict["db_url"]}/{postgresql_dict["db_name"] }'
    postgres_db_engine = create_engine( connection_string ) #"postgresql+psycopg2://postgres:password@localhost/dvdrental" , echo=True)
    seen = {None}
    for item in request.node.items:
        cls = item.getparent(pytest.Class)
        if cls not in seen:
            cls.obj.postgres_db_engine = postgres_db_engine
            seen.add(cls)

    yield
    postgres_db_engine.dispose()

