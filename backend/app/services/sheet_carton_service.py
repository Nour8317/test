from fastapi import HTTPException
from app.models.sheet_carton import SheetCarton
from app.repositories.sheet_carton_repository import SheetCartonRepository
from app.schemas.sheet_carton import SheetCartonCreate
from pathlib import Path
import shutil
from datetime import datetime
import uuid
from typing import Optional, List
from fastapi import UploadFile

UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class SheetCartonService:
    def __init__(self, repo: SheetCartonRepository):
        self.repo = repo

    def create_sheet_carton(self, carton: SheetCartonCreate) -> SheetCarton:
        sheet_data = carton.dict(exclude={"flutes"})
        sheet = self.repo.create(sheet_data)
        if carton.flutes:
            self.repo.add_flutes(sheet.id, [f.dict() for f in carton.flutes])
        return sheet

    def get_all_sheet_cartons(self):
        return self.repo.get_all()

    def get_by_client(self, client_id: int) -> List[SheetCarton]:
        sheet = self.repo.get_by_client(client_id)
        if not sheet:
            raise HTTPException(status_code=404, detail="SheetCarton not found")
        return sheet
    def get_clients(self):
        return self.repo.get_clients()
    
    def get_sheet_carton(self, sheet_id: int):
        sheet = self.repo.get_by_id(sheet_id)
        if not sheet:
            raise HTTPException(status_code=404, detail="SheetCarton not found")
        return sheet

    def update_waste(self, sheet_id: int, waste: float):
        sheet = self.repo.get_by_id(sheet_id)
        if not sheet:
            raise HTTPException(status_code=404, detail="SheetCarton not found")
        sheet.waste_weight = waste
        return self.repo.update(sheet)

    def delete_sheet_carton(self, sheet_id: int):
        sheet = self.repo.get_by_id(sheet_id)
        if not sheet:
            raise HTTPException(status_code=404, detail="SheetCarton not found")
        self.repo.delete(sheet)

    def update_sheet_carton(
        self,
        sheet_id: int,
        client_id: int,
        polygon_type: Optional[str] = None,
        polygon_category: Optional[str] = None,
        form: Optional[str] = None,
        notes: Optional[str] = None,
        cost: Optional[float] = None,
        currency: Optional[float] = None,
        sheet_length: Optional[float] = None,
        sheet_width: Optional[float] = None,
        design: Optional[UploadFile] = None
    ):
        sheet = self.repo.get_by_id(sheet_id)
        if not sheet:
            raise HTTPException(status_code=404, detail="SheetCarton not found")

        sheet.client_id = client_id
        sheet.polygon_type = polygon_type
        sheet.polygon_category = polygon_category
        sheet.form = form
        sheet.notes = notes
        sheet.cost = cost
        sheet.currency = currency
        sheet.sheet_length = sheet_length
        sheet.sheet_width = sheet_width

        if design:
            if sheet.design:
                old_file = UPLOAD_DIR / Path(sheet.design).name
                if old_file.exists():
                    old_file.unlink()
            suffix = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
            file_name = f"sheet_carton_{suffix}_{design.filename}"
            file_path = UPLOAD_DIR / file_name
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(design.file, buffer)
            sheet.design = f"/static/uploads/{file_name}"

        return self.repo.update(sheet)
