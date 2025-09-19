from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.production_components import ProductionComponents
from app.repositories.base import BaseRepository

class ProductionComponentRepository(BaseRepository[ProductionComponents]):
    def __init__(self, db: Session):
        super().__init__(ProductionComponents,db)

    def get_all(self) -> List[ProductionComponents]:
        return self.db.query(ProductionComponents).all()

    def get_by_component(self, component: str) -> List[ProductionComponents]:
        return self.db.query(ProductionComponents).filter(
            ProductionComponents.component == component
        ).all()

    def get_filtered(
        self,
        component: str,
        material_name: str,
        material_type: str,
        color: Optional[str] = None,
        color_code: Optional[str] = None,
        dimensions: Optional[str] = None
    ) -> Optional[ProductionComponents]:
        query = self.db.query(ProductionComponents).filter(
            ProductionComponents.component == component,
            ProductionComponents.material_name == material_name,
            ProductionComponents.material_type == material_type
        )

        if color and color_code:
            query = query.filter(
                ProductionComponents.color == color,
                ProductionComponents.color_code == color_code
            )

        if dimensions:
            query = query.filter(ProductionComponents.dimensions == dimensions)

        return query.first()
