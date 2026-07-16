"""SQLAlchemy implementation of aggregate/statistics queries."""
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from common.dao.interfaces.stats_dao import StatsDaoInterface
from models.entities import Project, ProjectTechStack


class StatsDao(StatsDaoInterface):
    def count_projects(self, db: Session) -> int:
        return db.scalar(select(func.count()).select_from(Project)) or 0

    def top_tech_stacks(self, db: Session, limit: int = 10) -> list[dict[str, Any]]:
        # Distinct number of projects using each tech-stack name, highest first.
        project_count = func.count(func.distinct(ProjectTechStack.project_id))
        stmt = (
            select(ProjectTechStack.name, project_count.label("project_count"))
            .group_by(ProjectTechStack.name)
            .order_by(project_count.desc(), ProjectTechStack.name.asc())
            .limit(limit)
        )
        return [{"name": name, "project_count": count} for name, count in db.execute(stmt).all()]
