import shutil, uuid
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.american_box import AmericanBox
from app.schemas.american_box import AmericanBoxCreate
from app.repositories.american_box_repository import AmericanBoxRepository

UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class AmericanBoxService:
    def __init__(self, db: Session):
        self.repo = AmericanBoxRepository(db)

    def create_box(self, data: AmericanBoxCreate) -> AmericanBox:
        new_box = AmericanBox(**data.dict(exclude={"flutes"}))
        self.repo.db.add(new_box)
        self.repo.db.commit()
        self.repo.db.refresh(new_box)

        if data.flutes:
            self.repo.add_flutes(new_box.id, [flute.dict() for flute in data.flutes])
            self.repo.db.refresh(new_box)

        return new_box

    def get_clients(self):
        clients = self.repo.get_clients()
        if not clients:
            raise HTTPException(status_code=404, detail="No clients found")
        return clients

    def get_box(self, box_id: int) -> AmericanBox:
        box = self.repo.get(box_id)
        if not box:
            raise HTTPException(status_code=404, detail="American box not found")
        return box
    
    def get_boxes_by_client(self, client_id: int) -> list[AmericanBox]:
        box = self.repo.get_by_client(client_id)
        if not box:
            raise HTTPException(status_code=404, detail="American box not found")
        return box
    
    def update_waste(self, box_id: int, waste: float) -> AmericanBox:
        box = self.repo.update_waste(box_id, waste)
        if not box:
            raise HTTPException(status_code=404, detail="American box not found")
        return box

    def update_box(self, box_id: int, **kwargs) -> AmericanBox:
        box = self.repo.get(box_id)
        if not box:
            raise HTTPException(status_code=404, detail="American box not found")

        box.sheet_length = (kwargs["carton_length"] + kwargs["carton_width"]) * 2 + kwargs["tounge_dimension"]
        if kwargs["polygon_type"] == "single":
            box.sheet_width = kwargs["carton_height"] + kwargs["carton_width"]
            box.flap_dimension = kwargs["carton_width"] / 2
        elif kwargs["polygon_type"] in ["double 4", "double 5"]:
            box.sheet_width = (kwargs["carton_width"] + kwargs["carton_height"]) + 4
            box.flap_dimension = kwargs["carton_width"] / 2 + 2
        else:
            box.sheet_width = None
            box.flap_dimension = None
        design: UploadFile = kwargs.get("design")
        if design:
            if box.design:
                old_file_path = UPLOAD_DIR / Path(box.design).name
                if old_file_path.exists():
                    old_file_path.unlink()
            unique_suffix = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
            file_name = f"american_box_{unique_suffix}_{design.filename}"
            file_path = UPLOAD_DIR / file_name
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(design.file, buffer)
            box.design = f"/static/uploads/{file_name}"

        for field, value in kwargs.items():
            if hasattr(box, field) and field != "design":
                setattr(box, field, value)

        self.repo.db.commit()
        self.repo.db.refresh(box)
        return box
    


    def delete_box(self, box_id: int):
        box = self.repo.get(box_id)
        if not box:
            raise HTTPException(status_code=404, detail="American box not found")
        self.repo.delete(box_id)
        return {"detail": "American box deleted successfully"}
