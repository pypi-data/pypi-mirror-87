from typing import List, Optional, Type

from django.db import models
from manager_utils import bulk_upsert as original_bulk_upsert


def get_bulk_update_fields(cls: Type[models.Model], unique_fields: List[str]) -> List[str]:
    """
        Return list of all model fields that can be updated in bulk,
        excluding unique_fields
    """

    def _should_be_updated(field):
        return (
            field.name not in unique_fields and
            not (field.many_to_many or field.one_to_many)
            and not field.auto_created
        )

    return [
        field.name for field in cls._meta.get_fields()
        if _should_be_updated(field)
    ]


not_provided = object()


def bulk_upsert(
    queryset: models.QuerySet, model_objs: List[models.Model],
    unique_fields: List[str], update_fields: Optional[List[str]] = not_provided,
    return_upserts: bool = False, return_upserts_distinct: bool = False,
    sync: bool = False, native: bool = False
):
    if update_fields is not_provided:
        update_fields = get_bulk_update_fields(queryset.model, unique_fields)

    # noinspection PyTypeChecker
    return original_bulk_upsert(
        queryset,
        model_objs=model_objs,
        unique_fields=unique_fields,
        update_fields=update_fields,
        return_upserts=return_upserts,
        return_upserts_distinct=return_upserts_distinct,
        sync=sync,
        native=native
    )
