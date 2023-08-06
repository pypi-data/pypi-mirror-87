from aim.ql.parse_tree.base import Tree
from aim.ql.lexer import parse
from aim.ql.lexer.utils import is_token_in_operator
from aim.ql.lexer.tokens import Keyword, String
from aim.ql.ql import Comparison, Token, Identifier


class SyntacticTree(Tree):
    def build_from_statement(self, statement):
        tokens = parse(statement)[0]
        self.head = self.NODE(tokens, 0, 0)
        self.append_tokens(tokens, self.head)

    def append_tokens(self, tokens, parent):
        # Find and group IN keyword
        # FIXME: move to lexer
        grouped_tokens = []
        for idx, token in enumerate(tokens):
            if is_token_in_operator(token):
                comp = Comparison([
                    Token(String, 't'),
                    Token(Keyword, 'ind'),
                    Identifier([Token(String, 't')]),
                ])
                grouped_tokens.append(comp)
            else:
                grouped_tokens.append(token)

        for idx, token in enumerate(grouped_tokens):
            token_node = self.NODE(token, idx, parent.level+1, parent)
            if token.is_group:
                self.append_tokens(token.tokens, token_node)
