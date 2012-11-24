import re

LIST_RE = re.compile('^\s-\s')
DICT_RE = re.compile('^.+\s+\|\s+.+$')

filter_non_empty = lambda x: filter(lambda y: len(y) > 0, x)

def _parse_dict(lines):
    res = {}
    for line in filter_non_empty(lines):
        key, value = re.findall('^(\w+)\s+\|\s+(.+)$', line)[0]
        res[key] = unicode(value)
    return res

def _parse_list(lines):
    parsed_lines = map(lambda x: x.strip(' - '), lines)
    return filter_non_empty(parsed_lines)

PARSER_OPTS = {
    'str' : lambda lines : reduce(_reduce_lines, lines, ''),
    'dict' : _parse_dict,
    'list' : _parse_list
}

def _reduce_lines(memo, line):
    if len(line) > 0:
        sep = '' if len(memo) == 0 else ' '
        return sep.join([memo, line])
    return memo

class MarkdownParser(dict):
    def __init__(self, file_content, directive_spec = '^-+$'):
        self.directive = re.compile(directive_spec)
        self.file_content = str(file_content)
        self._parse()

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return None

    def _parse(self):
        lines = []; current_directive = None; current_directive_type = None
        for line in self.file_content.split('\n'):
            if self.directive.match(line):
                if current_directive:
                    self[current_directive.lower()] = PARSER_OPTS[current_directive_type](lines[:-1])
                current_directive = lines[-1]
                lines = []
                current_directive_type = None
            else:
                lines.append(line)
                if not current_directive_type:
                    if LIST_RE.match(line):
                        current_directive_type = 'list'
                    elif DICT_RE.match(line):
                        current_directive_type = 'dict'
                    else:
                        current_directive_type = 'str'

        if current_directive:
            self[current_directive.lower()] = PARSER_OPTS[current_directive_type](lines[:-1])
