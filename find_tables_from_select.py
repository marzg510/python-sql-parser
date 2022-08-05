"""
テーブル名を抽出する
"""
import sqlparse

IS_SHOW_TOKEN = False


def show_tokens(tokens, title=None):
    """
    tokenを表示する
    """
    if not IS_SHOW_TOKEN:
        return
    print("<<%s>>" % title)
    for token in tokens:
        if token.is_whitespace:
            continue
        print("%s %s ttype=%s" % (token.value, type(token), token.ttype))


def find_tables_from_select(tokens):
    """
    SELECT文からテーブルを抽出する
    """
    after_from = False
    tables = list()
    for token in tokens:
        if token.match(sqlparse.tokens.Keyword, "FROM"):
            after_from = True
        if after_from is True:
            if isinstance(token, sqlparse.sql.Identifier):
                tables.append(token)
            if isinstance(tokens, sqlparse.sql.IdentifierList):
                for i in token.get_identifiers():
                    if token.match(sqlparse.tokens.Punctuation, "*", regex=True):
                        continue
                    tables.append(i)
        if isinstance(token, sqlparse.sql.Where):
            tables.extend(find_tables_from_where(token.tokens))
    return tables


def find_tables_from_where(tokens):
    """
    WHERE句からテーブルを抽出する
    """
    tables = list()
    show_tokens(tokens)
    for token in tokens:
        if isinstance(token, sqlparse.sql.Comparison):
            tables.extend(find_tables_from_parenthesis(token.tokens))
    return tables


def find_tables_from_parenthesis(tokens):
    """
    カッコ内のSELECT文からテーブルを抽出する
    """
    tables = list()
    show_tokens(tokens, "Comparison")
    for token in tokens:
        if isinstance(token, sqlparse.sql.Parenthesis):
            show_tokens(token.tokens, "Parenthesis")
            tables.extend(find_tables_from_select(token.tokens))
    return tables


def main():
    """
    main
    """
    with open('sample05.sql') as f:
        query = f.read()
    parsed_queries = sqlparse.parse(query)

    statement = parsed_queries[0]
    tokens = statement.tokens

    # Show Statement Tokens
    show_tokens(tokens, "Statement")

    # Find Tables
    tables = list()

    tables.extend(find_tables_from_select(tokens))

    print("<<detected tables>>")
    for tbl in tables:
        print("%s(alias=%s) %s(ttype=%s)" % (tbl.get_real_name(), tbl.get_alias(), type(tbl), tbl.ttype))


if __name__ == "__main__":
    main()
