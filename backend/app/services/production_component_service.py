from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from typing import List
from app.schemas.production_components import DeductByComponentRequest, ProductionComponentOut
from app.repositories.production_component_repository import ProductionComponentRepository

class ProductionComponentService:
    def __init__(self, db: Session):
        self.repo = ProductionComponentRepository(db)

    def get_all(self) -> List[ProductionComponentOut]:
        components = self.repo.get_all()
        return [ProductionComponentOut.from_orm(c) for c in components]

    def get_by_component(self, component: str) -> List[ProductionComponentOut]:
        components = self.repo.get_by_component(component)
        if not components:
            raise HTTPException(status_code=404, detail="No matching rows found.")
        return [ProductionComponentOut.from_orm(c) for c in components]

    def deduct_by_component(self, data: DeductByComponentRequest) -> ProductionComponentOut:
        row = self.repo.get_filtered(
            component=data.component,
            material_name=data.material_name,
            material_type=data.material_type,
            color=data.color,
            color_code=data.color_code,
            dimensions=data.dimensions
        )

        if not row:
            raise HTTPException(status_code=404, detail="No matching row found.")

        if row.quantity < data.quantity_to_deduct or row.weight < data.weight_to_deduct:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock to deduct. "
                       f"Available quantity: {row.quantity}, weight: {row.weight}"
            )

        row.quantity -= data.quantity_to_deduct
        row.weight -= data.weight_to_deduct
        row.updated_at = datetime.utcnow()

        updated_row = self.repo.save(row)

        return ProductionComponentOut.from_orm(updated_row)
