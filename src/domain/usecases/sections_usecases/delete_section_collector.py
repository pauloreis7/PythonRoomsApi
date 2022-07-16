from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class DeleteSectionCollectorInterface(ABC):
    """Delete Section Collector Usecase Interface"""

    @abstractmethod
    async def delete_section(self, db_session: AsyncSession, section_id: int) -> None:
        """Must implement"""

        raise Exception("Must implement delete_section method")
