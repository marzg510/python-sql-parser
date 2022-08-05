import unittest
import find_tables_from_select as ft


class TestFindTablesFromSelectInFromClause(unittest.TestCase):
    def test_in_subquery(self):
        query = """
SELECT ID ,USER_NAME
FROM
  USERS U
WHERE
    U.ID > 10
AND I.TYPE IN (SELECT TYPE FROM M_ITEM WHERE ID > 50)
;
"""
        correct_tables = ["USERS", "M_ITEM"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)

    def test_exists_subquery(self):
        pass


if __name__ == '__main__':
    unittest.main()
