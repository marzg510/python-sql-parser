import unittest
import find_tables as ft


class TestFindTablesFromSelectUnion(unittest.TestCase):
    def test_union_all(self):
        query = """
SELECT ID ,USER_NAME
FROM
  USERS U
WHERE U.ID > 10
UNION ALL
SELECT ID ,USER_NAME
FROM
  USERS2
;
"""
        correct_tables = ["USERS", "USERS2"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)

    def test_union(self):
        query = """
SELECT ID ,USER_NAME
FROM
  USERS U
WHERE U.ID > 10
UNION
SELECT ID ,USER_NAME
FROM
  USERS2
;
"""
        correct_tables = ["USERS", "USERS2"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)

    def test_minus(self):
        query = """
SELECT ID ,USER_NAME
FROM
  USERS U
WHERE U.ID > 10
MINUS
SELECT ID ,USER_NAME
FROM
  USERS2
;
"""
        correct_tables = ["USERS", "USERS2"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)
    
    def test_intersect(self):
        query = """
SELECT ID ,USER_NAME
FROM
  USERS U
WHERE U.ID > 10
INTERSECT
SELECT ID ,USER_NAME
FROM
  USERS2
;
"""
        correct_tables = ["USERS", "USERS2"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)


if __name__ == '__main__':
    unittest.main()
