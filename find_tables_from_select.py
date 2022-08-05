"""
テーブル名を抽出する
"""
import sqlparse


def show_statement(tokens):
    """
    Statementを表示する
    """
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
                for id in token.get_identifiers():
                    if token.match(sqlparse.tokens.Punctuation, "*", regex=True):
                        continue
                    tables.append(id)
        if isinstance(token, sqlparse.sql.Where):
            print("<<where>>")
            show_statement(token.tokens)
            for wt in token.tokens:
                if isinstance(wt, sqlparse.sql.Comparison):
                    print("<<Comparison>>")
                    show_statement(wt.tokens)
                    for ct in wt.tokens:
                        if isinstance(ct, sqlparse.sql.Parenthesis):
                            print("<<Parenthesis>>")
                            show_statement(ct.tokens)
                            tables.extend(find_tables_from_select(ct.tokens))
    return tables


def main():
    """
    main
    """
    with open('sample04.sql') as f:
        query = f.read()
    parsed_queries = sqlparse.parse(query)
    
    statement = parsed_queries[0]
    tokens = statement.tokens
    
    # Show Statement Tokens
    print("<<Statement>>")
    show_statement(tokens)
    
    # print("<<Statement>>")
    # for t in tokens:
    #     if t.is_whitespace:
    #         continue
    #     print("%s %s ttype=%s" % (t.value,type(t),t.ttype))
    
    # Find Tables
    tables = list()

    tables.extend(find_tables_from_select(tokens))
    
    print("<<detected tables>>")
    for tbl in tables:
        print("%s(alias=%s) %s(ttype=%s)" % (tbl.get_real_name(),tbl.get_alias(),type(tbl),tbl.ttype))


if __name__ == "__main__":
    main()
