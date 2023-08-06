from aim.ql.eval.utils import get_expression_tree_from_stmt


def pprint(statement: str):
    e_tree = get_expression_tree_from_stmt(statement)
    print(e_tree)
