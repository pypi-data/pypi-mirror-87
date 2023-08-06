from collections import namedtuple
from functools import reduce
from inspect import signature, isclass

from sqlalchemy import join, select, func, alias
from sqlalchemy.sql import and_, or_
from pydantic import BaseModel

from fsu.internal.error import ObjectNotExist, FieldNotExist, UnsupportedOperator

_LOGICAL_OPERATORS = {
    "AND" : and_,
    "OR"  : or_,
}
_COMPARISON_OPERATORS = {
    "EQ"          : lambda v : ("=", v),
    "LIKE"        : lambda v : ("like", f"%{v}%"),
    "STARTS_WITH" : lambda v : ("like", f"{v}%"),
    "IN"          : lambda v : ("in", v),
    "GT"          : lambda v : (">", v),
    "GE"          : lambda v : (">=", v),
    "LT"          : lambda v : ("<", v),
    "LE"          : lambda v : ("<=", v),
}

def _schema_names(schema):
    ret = []

    for n, p in signature(schema).parameters.items():
        if issubclass(p.annotation, BaseModel):
            ret.append((n, _schema_names(p.annotation)))
        else:
            ret.append(n)

    return ret


def _get_fields_and_tables(table_name, models, schema_names):
    if table_name not in models:
        raise ObjectNotExist(table_name)

    model = models[table_name]

    tables = [model]
    fields = []

    for n in schema_names:
        if isinstance(n, tuple):
            n, s = n
            sub_tables, sub_fields = _get_fields_and_tables(n, models, s)

            tables.extend(sub_tables)
            fields.extend(sub_fields)
        else:
            if n not in model.c:
                raise FieldNotExist(table_name, n)

            fields.append(model.c[n])

    return tables, fields


def _row_to_dict(row, table_name, models, schema_names):
    model = models[table_name]

    ret = {}

    for n in schema_names:
        if isinstance(n, tuple):
            n, s = n
            ret[n] = _row_to_dict(row, n, models, s)
        else:
            ret[n] = row[model.c[n]]

    return ret


def _get_field_from_path(path, tables):
    table_name, field_name = path[-2:]

    if table_name not in tables:
        raise ObjectNotExist(table_name)

    table = tables[table_name]

    if field_name not in table.c:
        raise FieldNotExist(table_name, field_name)

    return table, table.c[field_name]


Mapper = namedtuple("Mapper", ["select", "count", "dict", "where", "order_by"])

def make_mapper(table_name, metadata, schema_def):
    models = metadata.tables

    if isclass(schema_def) and issubclass(schema_def, BaseModel):
        schema_names = _schema_names(schema_def)
    else:
        schema_names = schema_def

    tables, fields = _get_fields_and_tables(table_name, models, schema_names)

    where_clause  = None
    order_clauses = None

    def select_():
        sql = select(fields).select_from(reduce(join, tables))

        if where_clause is not None:
            sql = sql.where(where_clause)

        if order_clauses is not None:
            sql = sql.order_by(*order_clauses)

        return sql

    def count():
        sql = select([func.count()]).select_from(reduce(join, tables))

        if where_clause is not None:
            sql = sql.where(where_clause)

        return sql

    def dict_(row):
        return _row_to_dict(row, table_name, models, schema_names)

    # I used a trick to assign the where_clause, there DO have some intermediate assignments
    # but will be overrided with the outermost value which is the final where clause
    def where(filter_expr):
        nonlocal where_clause

        op_name = filter_expr[0]

        if op_name in _LOGICAL_OPERATORS:
            op       = _LOGICAL_OPERATORS[op_name]
            operands = map(where, filter_expr[1])

            where_clause = op(*operands)
        elif op_name in _COMPARISON_OPERATORS:
            op_fn = _COMPARISON_OPERATORS[op_name]

            path         = [table_name, *filter_expr[1]]
            table, field = _get_field_from_path(path, models)

            if table not in tables:
                tables.append(table)

            op, value = op_fn(filter_expr[2])

            where_clause = field.op(op)(value)
        else:
            raise UnsupportedOperator(op_name)

    def order_by(order_expr):
        nonlocal order_clauses

        os = []
        for ordering, path in order_expr:
            path         = [table_name, *path]
            table, field = _get_field_from_path(path, models)

            if table not in tables:
                tables.append(table)

            if ordering == "ASC":
                os.append(field.asc())
            elif ordering == "DESC":
                os.append(field.desc())

        order_clauses = os

    mapper = Mapper(
        select   = select_,
        dict     = dict_,
        where    = where,
        order_by = order_by,
        count    = count,
    )

    return mapper


# generate implicit join conditions by hand
def verbose_where(table_name, metadata, filter_expr):
    tables  = metadata.tables

    if table_name not in tables:
        raise ObjectNotExist(table_name)

    def verbose_where_(fexpr):
        op_name = fexpr[0]

        if op_name in _LOGICAL_OPERATORS:
            op       = _LOGICAL_OPERATORS[op_name]
            operands = map(verbose_where_, fexpr[1])

            return op(*operands)
        elif op_name in _COMPARISON_OPERATORS:
            op_fn = _COMPARISON_OPERATORS[op_name]

            where_clauses = []
            path = fexpr[1][:-1]

            current_table = tables[table_name]
            # NOTE the loop below may generate redundant where clauses which is necessary cuz we need
            #      to ensure tables along the path are connected via those where clauses correctly
            for x in path:
                x_id = x + "_id"

                if x in current_table.c:
                    fkey_col = x
                elif x_id in current_table.c:
                    fkey_col = x_id
                else:
                    raise FieldNotExist(current_table.name, x_id)

                fkey = next((fkey for fkey in current_table.c[fkey_col].foreign_keys), None)

                if fkey is None:
                    raise ObjectNotExist(f"{current_table.name}.{x}")

                target_table_alias = alias(tables[fkey.column.table.name])
                where_clauses.append(current_table.c[fkey_col] == target_table_alias.c[fkey.column.name])
                current_table = target_table_alias

            field_name = fexpr[1][-1]
            if field_name not in current_table.c:
                raise FieldNotExist(current_table.name, field_name)

            field = current_table.c[field_name]

            op, value = op_fn(fexpr[2])
            # precedence=100 means do not add parenthesis
            where_clauses.append(field.op(op, precedence=100)(value))

            return and_(*where_clauses)
        else:
            raise UnsupportedOperator(op_name)

    return verbose_where_(filter_expr)


def find_table(metadata, left, p):
    tables = metadata.tables

    current_table = tables[left]
    for x in p:
        x_id = x + "_id"

        if x in current_table.c:
            fkey_col = x
        elif x_id in current_table.c:
            fkey_col = x_id
        else:
            raise FieldNotExist(current_table.name, x_id)

        fkey = next((fkey for fkey in current_table.c[fkey_col].foreign_keys), None)

        if fkey is None:
            raise ObjectNotExist(f"{current_table.name}.{x}")

        current_table = fkey.column.table

    return current_table

EnhQ = namedtuple("EnhQ", ["query", "count", "filter", "sort", "dict"])

def bind_enhq(metadata):
    tables = metadata.tables

    def get_aliases_and_fields(table_name, schema_names, path):
        if table_name not in tables:
            raise ObjectNotExist(table_name)

        table_alias = alias(tables[table_name])

        aliases = { path : table_alias }
        fields  = []
        frefs   = []

        for s in schema_names[1]:
            if isinstance(s, tuple):
                s0_id = s[0] + "_id"

                if s[0] in table_alias.c:
                    fkey_col = s[0]
                elif s0_id in table_alias.c:
                    fkey_col = s0_id
                else:
                    raise FieldNotExist(table_name, s0_id)

                fkey = next((fkey for fkey in table_alias.c[fkey_col].foreign_keys), None)

                if fkey is None:
                    raise ObjectNotExist(f"{table_name}.{s[0]}")

                sub_path = (*path, s[0])
                sub_aliases, sub_fields, sub_frefs = get_aliases_and_fields(str(fkey.column.table.name), s, sub_path)

                aliases.update(sub_aliases)

                fields.append(table_alias.c[fkey_col])
                fields.extend(sub_fields)

                frefs.append((table_alias.c[fkey_col], sub_aliases[sub_path]))
                frefs.extend(sub_frefs)
            else:
                if s not in table_alias.c:
                    raise FieldNotExist(table_name, s)

                fields.append(table_alias.c[s])

        return aliases, fields, frefs


    def make_enhq(left_most, schema_def, isouter = True):
        if isclass(schema_def) and issubclass(schema_def, BaseModel):
            schema_names = _schema_names(schema_def)
        else:
            schema_names = schema_def

        table_aliases, fields, frefs = get_aliases_and_fields(left_most, (left_most, schema_names), ())

        final_table = table_aliases[()]
        for fref in frefs:
            fcol, target_table = fref
            fkey = next(fkey for fkey in fcol.foreign_keys)

            final_table = join(final_table, target_table, fcol == target_table.c[fkey.column.name], isouter=isouter)

        where_clause     = None
        order_by_clauses = None

        def query():
            s = select(fields).select_from(final_table)

            if where_clause is not None:
                s = s.where(where_clause)

            if order_by_clauses is not None:
                s = s.order_by(*order_by_clauses)

            return s

        def count():
            s = select([func.count()]).select_from(final_table)

            if where_clause is not None:
                s = s.where(where_clause)

            return s

        def where(filter_def):
            op_name = filter_def[0]

            if op_name in _LOGICAL_OPERATORS:
                op       = _LOGICAL_OPERATORS[op_name]
                operands = map(where, filter_def[1])

                return op(*operands)
            elif op_name in _COMPARISON_OPERATORS:
                op_fn = _COMPARISON_OPERATORS[op_name]

                path       = tuple(filter_def[1][:-1])
                field_name = filter_def[1][-1]

                obj_dot_path   = ".".join(path)
                field_dot_path = ".".join(filter_def[1])

                if path not in table_aliases:
                    raise ObjectNotExist(obj_dot_path)

                table_alias = table_aliases[path]

                if field_name not in table_alias.c:
                    raise FieldNotExist(obj_dot_path, field_dot_path)

                field = table_alias.c[field_name]

                op, value = op_fn(filter_def[2])
                return field.op(op)(value)
            else:
                raise UnsupportedOperator(op_name)

        # NOTE will raise exception if filtered a field not defined inside `fields`
        #      its the caller's responsibility to defined that field.
        def filter_(filter_def):
            nonlocal where_clause

            where_clause = where(filter_def)

            return enhq

        def sort(sort_def):
            nonlocal order_by_clauses

            order_by_clauses = []

            for x in sort_def:
                m          = x[0]
                path       = tuple(x[1][:-1])
                field_name = x[1][-1]

                obj_dot_path   = ".".join(path)
                field_dot_path = ".".join(x[1])

                if path not in table_aliases:
                    raise ObjectNotExist(obj_dot_path)

                table_alias = table_aliases[path]

                if field_name not in table_alias.c:
                    raise FieldNotExist(obj_dot_path, field_dot_path)

                field = table_alias.c[field_name]

                if m == "ASC":
                    order_by_clauses.append(field.asc())
                elif m == "DESC":
                    order_by_clauses.append(field.desc())

            return enhq

        def dict_(r):
            def row_to_dict(ss, p):
                table = table_aliases[p]

                ret = {}

                for s in ss:
                    if isinstance(s, tuple):
                        # don't need to check twice for the field existence
                        if s[0] in table.c:
                            fkey_col = s[0]
                        else:
                            fkey_col = s[0] + "_id"

                        if r[table.c[fkey_col]] is None:
                            ret[s[0]] = None
                        else:
                            ret[s[0]] = row_to_dict(s[1], (*p, s[0]))
                    else:
                        ret[s] = r[table.c[s]]

                return ret

            return row_to_dict(schema_names, ())

        enhq = EnhQ(
            query  = query,
            count  = count,
            filter = filter_,
            sort   = sort,
            dict   = dict_,
        )

        return enhq

    return make_enhq
