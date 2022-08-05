import unittest
import find_tables as ft


class TestFindTablesFromSelectInFromClause(unittest.TestCase):
    def test_simple_union(self):
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

    def test_exists_subquery(self):
        self.assertTrue("not implemented" == "")

if __name__ == '__main__':
    unittest.main()
