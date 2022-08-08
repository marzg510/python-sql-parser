import unittest
import find_tables as ft


class TestFindTablesFromSelectScholar(unittest.TestCase):
    def test_scholar_single(self):
        query = """
SELECT
  (SELECT COUNT(*) FROM FAMILY F WHERE F.USER_ID=U.ID) AS FAMILY_COUNT
FROM
  USERS U
WHERE
    U.ID > 10
;
"""
        correct_tables = ["FAMILY", "USERS"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)

    def test_scholar_mixed(self):
        query = """
SELECT
  ID 
  ,USER_NAME
  ,(SELECT COUNT(*) FROM FAMILY F WHERE F.USER_ID=U.ID) AS FAMILY_COUNT
FROM
  USERS U
WHERE
    U.ID > 10
;
"""
        correct_tables = ["FAMILY", "USERS"]
        result = ft.find_tables(query)
        self.assertEqual(result, correct_tables)

    def test_scholar_multi(self):
        query = ""
        self.assertEqual("not implemented", query)


if __name__ == '__main__':
    unittest.main()
