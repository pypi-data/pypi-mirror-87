from argparse import ArgumentParser
from pathlib import Path
from sqlalchemy import inspection
import sys
import importlib


def main():
    parser = ArgumentParser('viz_alchemy')
    parser.add_argument('-i', '--input', type=Path,
                        required=True, help='Input script path')
    parser.add_argument('-o', '--output', default=None,
                        type=Path, help='Output file')
    parser.add_argument('-n', '--name', default='Base',
                        type=str, help='class name at the input file')
    parser.add_argument('-f', '--format', type=str, default='stdout')
    args = parser.parse_args()

    # inspect_result = inspect_module(args.input, args.name)
    sys.path.append(str(Path().absolute()))
    path_to_file = str(args.input.relative_to(
        Path()).with_name(args.input.stem))
    module = importlib.import_module(path_to_file.replace('\\', '.'))
    base_class = getattr(module, args.name)

    dot_relation_builder = DotRelationshipBuilder()

    dot_tables = []
    for table_name, table_class in base_class.metadata.tables.items():
        types = []
        names = []
        for col, col_type in table_class.columns.items():
            names.append(col)
            types.append(str(col_type.type))

            for foreign_key in col_type.foreign_keys:
                dot_relation_builder.add(
                    table_name, col,
                    str(foreign_key.column.table), foreign_key.column.name,
                )
                # print(
                #     table_name, col,
                #     str(foreign_key.column.table), foreign_key.column.name,
                # )
        table_str = TableBuilder(table_name, names, types).build()
        dot_str = f'{table_name} [label=<{table_str}>];'
        dot_tables.append(dot_str)

    dot_table = 'digraph {\n' \
        'graph [pad="0.5", nodesep="0.5", ranksep="2"];\n'\
        'node [shape=plaintext];\n'\
        'rankdir=LR;\n'
    dot_table += '\n'.join(dot_tables)
    dot_table += dot_relation_builder.build()
    dot_table += '}'

    if args.output is None:
        output_filename = f'{args.input.name}.dot'
    else:
        output_filename = args.output
    with open(output_filename, 'w+') as fp:
        fp.write(dot_table)


class DotRelationshipBuilder:
    def __init__(self):
        self.relationships = []

    def add(self, table_name, foreign_key, target_table, target_key):
        self.relationships.append(
            (table_name, foreign_key, target_table, target_key)
        )

    def build(self):
        output_lines = []
        for table_name, foreign_key, target_table, target_key in self.relationships:
            output_lines.append(
                f'{table_name}:{foreign_key}->{target_table}:{target_key};'
            )
        return '\n'.join(output_lines)


class TableBuilder:
    def __init__(self, table_name, columns, types):
        self.table_name = table_name
        self.columns = columns
        self.types = types

    def build(self):
        table_str = '<table border="0" cellborder="1" cellspacing="0">'
        table_str += f'<tr><td BGCOLOR="lightgray" colspan="2">{self.table_name}</td></tr>'
        table_str += '<tr><td BGCOLOR="lightgray">Column</td><td BGCOLOR="lightgray">Type</td></tr>'
        for col, t in zip(self.columns, self.types):
            table_str += f'<tr><td port="{col}">{col}</td><td>{t}</td></tr>'
        table_str += '</table>'
        return table_str


def inspect_module(file, name):
    sys.path.append(str(Path().absolute()))
    local = {}
    with open(file, 'r') as fp:
        exec(compile(fp.read(), str(file), 'exec'), globals(), local)
    print(local[name])
    return inspection.inspect(local[name])


if __name__ == "__main__":
    main()
