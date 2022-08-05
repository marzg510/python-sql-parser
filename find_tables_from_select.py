"""
テーブル名を抽出する
"""
import sqlparse
import logging
import os
import sys


global log
log = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
# log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
log.addHandler(handler)


def show_tokens(tokens, title=None):
    """
    tokenを表示する
    """
    if log.level > logging.DEBUG:
        return
    log.debug("<<%s>>" % title)
    for tok in tokens:
        if tok.is_whitespace:
            continue
        log.debug("%s %s ttype=%s" % (repr(tok.value), type(tok), tok.ttype))


def find_tables(query):
    """
    SQL文からテーブルを抽出する
    """
    parsed_queries = sqlparse.parse(query)
    statement = parsed_queries[0]
    tables = list()
    tokens = statement.tokens
    # Show Statement Tokens
    show_tokens(tokens, "Statement")

    # SQL文のタイプを調べて処理分岐
    for tok in tokens:
        if tok.match(sqlparse.tokens.DML, "SELECT"):
            log.info("SELECT文を検出")
            tables.extend(find_tables_from_select(tokens))
            break

    # 文字列のリストに詰めなおす
    log.info("<<detected tables>>")
    ret = list()
    for tbl in tables:
        log.info("%s(alias=%s) %s(ttype=%s)" % (tbl.get_real_name(), tbl.get_alias(), type(tbl), tbl.ttype))
        ret.append(tbl.get_real_name())

    return ret


def find_tables_from_select(tokens):
    """
    SELECT文からテーブルを抽出する
    """
    in_from = False
    tables = list()
    for tok in tokens:
        if tok.match(sqlparse.tokens.Keyword, "FROM"):
            log.info("FROM句を検出")
            in_from = True
        if in_from is True:
            if isinstance(tok, sqlparse.sql.Identifier):
                log.info("FROM句内に単一のオブジェクト識別子を検出")
                tables.append(tok)
            if isinstance(tok, sqlparse.sql.IdentifierList):
                log.info("FROM句内に複数のオブジェクト識別子を検出")
                show_tokens(tok.tokens, "IdentifierList")
                for i in tok.get_identifiers():
                    if tok.match(sqlparse.tokens.Punctuation, "*", regex=True):
                        continue
                    tables.append(i)
        if isinstance(tok, sqlparse.sql.Where):
            log.info("WHERE句を検出")
            tables.extend(find_tables_from_where(tok.tokens))
            in_from = False
            log.info("FROM句を離脱")
    return tables


def find_tables_from_where(tokens):
    """
    WHERE句からテーブルを抽出する
    """
    tables = list()
    show_tokens(tokens, "WHERE")
    for tok in tokens:
        if isinstance(tok, sqlparse.sql.Comparison):
            log.info("Comparisonトークンを検出(WHERE句内)")
            tables.extend(find_tables_from_parenthesis(tok.tokens))
    return tables


def find_tables_from_parenthesis(tokens):
    """
    カッコ内のSELECT文からテーブルを抽出する
    """
    tables = list()
    show_tokens(tokens, "Comparison")
    for tok in tokens:
        if isinstance(tok, sqlparse.sql.Parenthesis):
            log.info("カッコ内のトークンを検出(Comparison内)")
            show_tokens(tok.tokens, "Parenthesis")
            tables.extend(find_tables_from_select(tok.tokens))
    return tables


def main():
    """
    main
    """
    with open('sample06.sql') as f:
        query = f.read()

    # Find Tables
    tables = list()

    log.info("statement = %s" % repr(query))
    tables.extend(find_tables(query))


if __name__ == "__main__":
    main()
