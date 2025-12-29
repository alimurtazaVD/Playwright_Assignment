
import os
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, dsn: str = None, **kwargs):
        self.dsn = dsn or os.getenv('DATABASE_URL')
        self.engine = None
        self.SessionLocal = None
        self._setup_connection(**kwargs)
    
    def _setup_connection(self, **kwargs):
        """Setup database connection"""
        try:
            if not self.dsn:
                logger.warning("No database DSN provided, database operations disabled")
                return
            
            # Create engine with connection pooling
            pool_size = kwargs.get('pool_size', 5)
            max_overflow = kwargs.get('max_overflow', 10)
            
            self.engine = create_engine(
                self.dsn,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_pre_ping=True,
                echo=kwargs.get('echo', False)
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("Database connection established successfully")
            
        except SQLAlchemyError as e:
            logger.error(f"Failed to establish database connection: {e}")
            self.engine = None
            self.SessionLocal = None
    
    def get_session(self) -> Optional[Session]:
        """Get a database session"""
        if not self.SessionLocal:
            logger.error("Database not configured")
            return None
        
        try:
            return self.SessionLocal()
        except SQLAlchemyError as e:
            logger.error(f"Failed to create database session: {e}")
            return None
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a raw SQL query and return results"""
        if not self.engine:
            logger.error("Database not configured")
            return []
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                if result.returns_rows:
                    columns = result.keys()
                    return [dict(zip(columns, row)) for row in result.fetchall()]
                return []
                
        except SQLAlchemyError as e:
            logger.error(f"Query execution failed: {e}")
            return []
    
    def execute_scalar(self, query: str, params: Dict[str, Any] = None) -> Any:
        """Execute a query and return a single scalar value"""
        if not self.engine:
            logger.error("Database not configured")
            return None
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                row = result.fetchone()
                return row[0] if row else None
                
        except SQLAlchemyError as e:
            logger.error(f"Scalar query execution failed: {e}")
            return None
    
    def execute_non_query(self, query: str, params: Dict[str, Any] = None) -> bool:
        """Execute a non-query SQL statement (INSERT, UPDATE, DELETE)"""
        if not self.engine:
            logger.error("Database not configured")
            return False
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(query), params or {})
                conn.commit()
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Non-query execution failed: {e}")
            return False
    
    def seed_test_data(self, data_scripts: List[str]) -> bool:
        """Seed test data using provided SQL scripts"""
        if not self.engine:
            logger.error("Database not configured")
            return False
        
        try:
            with self.engine.connect() as conn:
                for script in data_scripts:
                    conn.execute(text(script))
                conn.commit()
                logger.info("Test data seeded successfully")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Failed to seed test data: {e}")
            return False
    
    def cleanup_test_data(self, cleanup_scripts: List[str]) -> bool:
        """Clean up test data using provided SQL scripts"""
        if not self.engine:
            logger.error("Database not configured")
            return False
        
        try:
            with self.engine.connect() as conn:
                for script in cleanup_scripts:
                    conn.execute(text(script))
                conn.commit()
                logger.info("Test data cleaned up successfully")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Failed to cleanup test data: {e}")
            return False
    
    def get_table_count(self, table_name: str) -> int:
        """Get the row count of a table"""
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute_scalar(query)
        return result or 0
    
    def check_table_exists(self, table_name: str) -> bool:
        """Check if a table exists"""
        query = """
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_name = :table_name
        """
        result = self.execute_scalar(query, {'table_name': table_name})
        return result > 0
    
    def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")


class TestDataManager:
    """Manages test data operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create_test_user(self, username: str, email: str, **kwargs) -> bool:
        """Create a test user in the database"""
        query = """
        INSERT INTO users (username, email, created_at) 
        VALUES (:username, :email, NOW())
        """
        params = {
            'username': username,
            'email': email,
            **kwargs
        }
        return self.db.execute_non_query(query, params)
    
    def delete_test_user(self, username: str) -> bool:
        """Delete a test user from the database"""
        query = "DELETE FROM users WHERE username = :username"
        return self.db.execute_non_query(query, {'username': username})
    
    def get_test_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get a test user from the database"""
        query = "SELECT * FROM users WHERE username = :username"
        results = self.db.execute_query(query, {'username': username})
        return results[0] if results else None
    
    def cleanup_all_test_data(self) -> bool:
        """Clean up all test data"""
        cleanup_scripts = [
            "DELETE FROM users WHERE username LIKE 'test_%'",
            "DELETE FROM sessions WHERE created_at < NOW() - INTERVAL '1 hour'",
            "DELETE FROM logs WHERE level = 'DEBUG'"
        ]
        return self.db.cleanup_test_data(cleanup_scripts)


# Global database manager instance
db_manager = None
test_data_manager = None


def initialize_database(dsn: str = None, **kwargs):
    """Initialize the global database manager"""
    global db_manager, test_data_manager
    
    db_manager = DatabaseManager(dsn, **kwargs)
    test_data_manager = TestDataManager(db_manager)
    
    return db_manager


def get_db_manager() -> Optional[DatabaseManager]:
    """Get the global database manager instance"""
    return db_manager


def get_test_data_manager() -> Optional[TestDataManager]:
    """Get the global test data manager instance"""
    return test_data_manager
