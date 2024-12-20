import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Session
from typing import Optional


class ScyllaDBConnection:
    def __init__(
        self,
        contact_points: Optional[list] = None,
        port: int = 9042,
        keyspace: str = "myapp",
    ) -> None:
        self.cluster = None
        self.session = None
        self.keyspace = keyspace
        self.contact_points = contact_points or ["scylla"]
        self.port = port

    def connect(self) -> None:
        try:
            username = os.getenv("SCYLLA_USERNAME")
            password = os.getenv("SCYLLA_PASSWORD")

            auth_provider = (
                PlainTextAuthProvider(username=username, password=password)
                if username and password
                else None
            )

            self.cluster = Cluster(
                contact_points=self.contact_points,
                port=self.port,
                auth_provider=auth_provider,
            )
            self.session = self.cluster.connect()
            self._create_keyspace()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to ScyllaDB: {e}")

    def _create_keyspace(self) -> None:
        try:
            keyspace_query = f"""
            CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
            WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': 1 }}
            """
            self.session.execute(keyspace_query)
            self.session.set_keyspace(self.keyspace)
        except Exception as e:
            raise RuntimeError(f"Failed to create keyspace '{self.keyspace}': {e}")

    def get_session(self) -> Session:
        if not self.session:
            raise RuntimeError("Session not initialized. Call `connect()` first.")
        return self.session

    def close(self) -> None:
        if self.cluster:
            self.cluster.shutdown()


def create_keyspace_and_table():
    try:
        db = ScyllaDBConnection()
        db.connect()
        session = db.get_session()

        table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id uuid PRIMARY KEY,
            name text,
            email text,
            age int
        )
        """
        session.execute(table_query)
        print("Keyspace and table created successfully.")
    except Exception as e:
        print(f"Error creating keyspace and table: {e}")


def get_db_session() -> Optional[Session]:
    try:
        db = ScyllaDBConnection()
        db.connect()
        return db.get_session()
    except Exception as e:
        print(f"Failed to get database session: {e}")
        return None
