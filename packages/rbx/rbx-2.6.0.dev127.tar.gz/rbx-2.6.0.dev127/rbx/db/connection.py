import warnings

from sqlalchemy import create_engine, text


class Singleton(type):
    """Singleton type.

    For testing, the 'clear' flag may be provided to bypass the pattern and re-instantiate the
    class with a new instance.
    """
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None or kwargs.get('clear', False):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Connection(metaclass=Singleton):
    """Wraps a connection to a MySQL instance."""

    def __init__(self, db_engine_url, clear=False):
        """Create a connection engine with default connection pooling.

        As a Singleton, the connection engine will only be created once for the entire process.
        SqlAlchemy will then chekout a new connection from the pool as needed.
        """
        self.engine = create_engine(
            db_engine_url,
            max_overflow=2,
            pool_pre_ping=True,
            pool_recycle=1800,  # 30 minutes
            pool_size=5,
            pool_timeout=30
        )

    def __enter__(self):
        self.conn = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'conn'):
            self.conn.close()
            del self.conn

    @property
    def dialect(self):
        return self.engine.dialect

    def execute(self, *args, **kwargs):
        if self.dialect.name == 'mysql':
            self.conn.execute('SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci')
        return self.conn.execute(*args, **kwargs)

    def has_table(self, table_name):
        return self.engine.dialect.has_table(self.engine, table_name)

    def query(self, statement, scalar=False, total=None):
        """Run a SQL statement and return the results.

        When a 'total' SQL statement is provided, the total scalar is also returned, and the
        return object is then a tuple.

        When 'scalar' is True, a scalar type is returned.
        """
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', '.*Division by 0.*', category=Warning)
            results = self.conn.execute(text(statement))
            if scalar:
                data = results.scalar()
            else:
                data = results.fetchall()

        if total:
            totals = self.conn.execute(total).scalar()
            return data, totals

        return data
