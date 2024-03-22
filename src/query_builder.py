from typing import Any

from sqlalchemy import Unicode, or_, cast
from sqlalchemy.orm.query import Query


def get_filtered_query(table, query: Query, filter_fields: dict[str, Any]) -> Query:
    if not filter_fields:
        return query

    for attr, value in filter_fields.items():
        filter_obj = getattr(table, attr, None)
        if filter_obj and value:
            query = query.filter(filter_obj == value)

    return query


def search_query(query: Query, selected_table, search_term: str, field_names: list[str]) -> Query:
    search_term = search_term.strip()
    search_list = []
    for field in field_names:
        selected_field = cast(getattr(selected_table, field), Unicode)
        search_list.append(selected_field.ilike(f"%{search_term}%"))
    return query.filter(or_(*search_list))
