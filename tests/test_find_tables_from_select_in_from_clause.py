import unittest
import find_tables_from_select as ft


class TestFindTablesFromSelectInFromClause(unittest.TestCase):
    def test_single(self):
        query = """
SELECT
  ID
  ,USER_NAME
FROM
  USERS
WHERE
  ID > 10
;
"""
        correct_tables = ["USERS"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)

    def test_comma_separated(self):
        query = """
SELECT ID ,USER_NAME
FROM
  USERS U
  ,ITEMS I
WHERE U.ID > 10
;
"""
        correct_tables = ["USERS", "ITEMS"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)

    def test_inner_join(self):
        query = """
SELECT ID ,USER_NAME
FROM
  USERS U
  INNER JOIN ITEMS I ON U.ID = I.BUYER_USER_ID
WHERE U.ID > 10
;
"""
        correct_tables = ["USERS", "ITEMS"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)

    def test_3tables_join(self):
        query = """
SELECT ID ,USER_NAME
FROM
  USERS U
  INNER JOIN ITEMS I ON U.ID = I.BUYER_USER_ID
  LEFT JOIN ITEM_DETAILS ID ON I.ID = ID.ITEM_ID
WHERE U.ID > 10
;
"""
        correct_tables = ["USERS", "ITEMS", "ITEM_DETAILS"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)


if __name__ == '__main__':
    unittest.main()
