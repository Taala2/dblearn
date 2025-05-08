import json
import sqlite3
import time
import asyncio
from typing import Any, Dict, List, Optional

from app.core.config import settings
from app.schemas import RunResult


def execute_query(conn: sqlite3.Connection, query: str) -> List[Dict[str, Any]]:
    """Execute SQL query and return results as a list of dictionaries."""
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Get column names
        columns = [col[0] for col in cursor.description] if cursor.description else []
        
        # Fetch rows with limit
        rows = cursor.fetchmany(settings.SQL_MAX_ROWS)
        
        # Convert to list of dictionaries
        results = [dict(zip(columns, row)) for row in rows]
        return results
    except sqlite3.Error as e:
        raise Exception(f"SQL execution error: {str(e)}")


def normalize_results(results: List[Dict[str, Any]]) -> str:
    """Normalize and convert results to JSON string for comparison."""
    # JSON dump with sorted keys for consistent comparison
    return json.dumps(results, sort_keys=True)


def evaluate_sql(init_sql: str, expected_sql: str, submitted_sql: str) -> RunResult:
    """
    Evaluate submitted SQL against expected SQL.
    
    Args:
        init_sql: SQL to initialize the database environment
        expected_sql: The reference SQL solution
        submitted_sql: The SQL submitted by the user
    
    Returns:
        RunResult object with evaluation results
    """
    try:
        # Create in-memory database
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        
        # Initialize database with setup SQL
        conn.executescript(init_sql)
        conn.commit()
        
        # Execute expected SQL
        expected_results = execute_query(conn, expected_sql)
        expected_json = normalize_results(expected_results)
        
        # Execute submitted SQL with timeout
        submitted_results = execute_query(conn, submitted_sql)
        submitted_json = normalize_results(submitted_results)
        
        # Compare results
        is_correct = (expected_json == submitted_json)
        
        # Close connection
        conn.close()
        
        return RunResult(
            is_correct=is_correct,
            result_json=submitted_json,
            time_ms=0,  # Will be set by the router
            rows=submitted_results,
            error=None
        )
        
    except Exception as e:
        return RunResult(
            is_correct=False,
            result_json="",
            time_ms=0,
            rows=None,
            error=str(e)
        )


async def evaluate_sql_with_timeout(init_sql: str, expected_sql: str, submitted_sql: str) -> RunResult:
    """
    Evaluate SQL with a timeout to prevent long-running queries.
    
    This function runs the evaluation in a separate thread to allow timeout enforcement.
    """
    try:
        # Run evaluation with timeout
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(
                None, evaluate_sql, init_sql, expected_sql, submitted_sql
            ),
            timeout=settings.SQL_TIMEOUT_SECONDS
        )
        return result
    except asyncio.TimeoutError:
        return RunResult(
            is_correct=False,
            result_json="",
            time_ms=int(settings.SQL_TIMEOUT_SECONDS * 1000),
            rows=None,
            error=f"Query execution timed out after {settings.SQL_TIMEOUT_SECONDS} seconds"
        )
    

def evaluate_sql_with_restrictions(init_sql, expected_sql, submitted_sql):
    # Проверка на запрещенные операции
    forbidden_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'UPDATE', 'INSERT', 'CREATE DATABASE', 'GRANT', 'REVOKE']
    for keyword in forbidden_keywords:
        if keyword in submitted_sql.upper() and 'SELECT' not in submitted_sql.upper():
            raise Exception(f"Операция {keyword} запрещена в учебном режиме")
    
    # Далее ваш существующий код


# Улучшенная функция сравнения результатов
def compare_query_results(expected_results, submitted_results, ignore_order=False):
    # Если нужно игнорировать порядок строк (для запросов без ORDER BY)
    if ignore_order:
        expected_sorted = sorted(expected_results, key=lambda x: json.dumps(x, sort_keys=True))
        submitted_sorted = sorted(submitted_results, key=lambda x: json.dumps(x, sort_keys=True))
        return expected_sorted == submitted_sorted
    
    # Иначе прямое сравнение с учетом порядка
    return expected_results == submitted_results