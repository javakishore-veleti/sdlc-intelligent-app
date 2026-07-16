"""Registers a CRUD router for every master-data entity under a single api_router.

Each tuple binds: url prefix, Swagger tag, ORM model, and Create/Update/Read schemas.
"""
from fastapi import APIRouter

from api.crud_router import build_crud_router
from facades.registry import build_facade
from models import entities as m
from schemas import entities as s

# (prefix, tag, model, create_schema, update_schema, read_schema)
_ENTITY_CONFIG = [
    ("/employees", "Employees", m.Employee, s.EmployeeCreate, s.EmployeeUpdate, s.EmployeeRead),
    ("/projects", "Projects", m.Project, s.ProjectCreate, s.ProjectUpdate, s.ProjectRead),
    ("/project-roles", "Project Roles", m.ProjectRole, s.ProjectRoleCreate, s.ProjectRoleUpdate, s.ProjectRoleRead),
    ("/project-employees", "Project Employees", m.ProjectEmployee, s.ProjectEmployeeCreate, s.ProjectEmployeeUpdate, s.ProjectEmployeeRead),
    ("/project-artifacts", "Project Artifacts", m.ProjectArtifact, s.ProjectArtifactCreate, s.ProjectArtifactUpdate, s.ProjectArtifactRead),
    ("/project-capabilities", "Project Capabilities", m.ProjectCapability, s.ProjectCapabilityCreate, s.ProjectCapabilityUpdate, s.ProjectCapabilityRead),
    ("/project-domains", "Project Domains", m.ProjectDomain, s.ProjectDomainCreate, s.ProjectDomainUpdate, s.ProjectDomainRead),
    ("/project-knowledge-bases", "Project Knowledge Bases", m.ProjectKnowledgeBase, s.ProjectKnowledgeBaseCreate, s.ProjectKnowledgeBaseUpdate, s.ProjectKnowledgeBaseRead),
    ("/project-tech-stacks", "Project Tech Stacks", m.ProjectTechStack, s.ProjectTechStackCreate, s.ProjectTechStackUpdate, s.ProjectTechStackRead),
    ("/project-dependency-groups", "Project Dependency Groups", m.ProjectDependencyGroup, s.ProjectDependencyGroupCreate, s.ProjectDependencyGroupUpdate, s.ProjectDependencyGroupRead),
    ("/project-dependencies", "Project Dependencies", m.ProjectDependency, s.ProjectDependencyCreate, s.ProjectDependencyUpdate, s.ProjectDependencyRead),
    ("/project-client-groups", "Project Client Groups", m.ProjectClientGroup, s.ProjectClientGroupCreate, s.ProjectClientGroupUpdate, s.ProjectClientGroupRead),
    ("/project-clients", "Project Clients", m.ProjectClient, s.ProjectClientCreate, s.ProjectClientUpdate, s.ProjectClientRead),
]

api_router = APIRouter()

for prefix, tag, model, create_schema, update_schema, read_schema in _ENTITY_CONFIG:
    api_router.include_router(
        build_crud_router(
            prefix=prefix,
            tags=[tag],
            facade=build_facade(model),
            create_schema=create_schema,
            update_schema=update_schema,
            read_schema=read_schema,
        )
    )
