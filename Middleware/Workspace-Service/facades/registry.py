"""Wires the layered stack (DAO -> Service -> Facade) for a given ORM model."""
from typing import Type, TypeVar

from dao.base_dao_impl import BaseDao
from facades.crud_facade import CrudFacade
from services.base_service_impl import BaseService

ModelT = TypeVar("ModelT")


def build_facade(model: Type[ModelT]) -> CrudFacade[ModelT]:
    """Assemble a ready-to-use CRUD facade for ``model``."""
    dao = BaseDao(model)
    service = BaseService(dao)
    return CrudFacade(service)
