from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.job_order import JobOrder
from app.models.job_order_item import JobOrderItem

from app.models.american_box import AmericanBox
from app.models.sheet_carton import SheetCarton
from app.models.flut import Flut
from app.models.rolls import Rolls
from app.models.raw_materials import RawMaterial
from app.models.paper_roll import PaperRoll
from app.models.job_order_flut_rolls import JobOrderFlutRoll
from app.schemas.job_order import JobOrderCreate, RollJobOrderCreate
from app.schemas.job_order_flut_rolls import FlutAssociationCreate
from app.repositories.job_order_repository import JobOrderRepository


class JobOrderService:
    def __init__(self, db: Session):
        self.repo = JobOrderRepository(db)
        self.db = db

    def create_job_order(self, data: JobOrderCreate):
        polygon_types = set()
        polygon_categories = set()
        all_flutes_by_layer = {}

        # validate polygon types/categories and flutes
        for item in data.items:
            if item.item_type == "american_box":
                box = self.db.query(AmericanBox).filter(AmericanBox.id == item.item_id).first()
                if not box:
                    raise HTTPException(status_code=404, detail="AmericanBox not found")
                polygon_types.add(box.polygon_type)
                polygon_categories.add(box.polygon_category)
                flutes = self.db.query(Flut).filter(Flut.american_box_id == box.id).order_by(Flut.layer_number).all()

            elif item.item_type == "sheet_carton":
                sheet = self.db.query(SheetCarton).filter(SheetCarton.id == item.item_id).first()
                if not sheet:
                    raise HTTPException(status_code=404, detail="SheetCarton not found")
                polygon_types.add(sheet.polygon_type)
                polygon_categories.add(sheet.polygon_category)
                flutes = self.db.query(Flut).filter(Flut.sheet_carton_id == sheet.id).order_by(Flut.layer_number).all()
            else:
                continue

            for idx, flute in enumerate(flutes):
                if idx not in all_flutes_by_layer:
                    all_flutes_by_layer[idx] = []
                all_flutes_by_layer[idx].append((flute.paper_type, flute.weight, flute.supplier))

        if len(polygon_types) > 1 or len(polygon_categories) > 1:
            raise HTTPException(status_code=400, detail="All items must have the same polygon_type and polygon_category.")

        for layer, flutes in all_flutes_by_layer.items():
            paper_types = {str(f[0]).strip().lower() for f in flutes}
            weights = {float(f[1]) for f in flutes}
            suppliers = {str(f[2]).strip().lower() for f in flutes}
            if len(paper_types) > 1 or len(weights) > 1 or len(suppliers) > 1:
                raise HTTPException(
                    status_code=400,
                    detail=f"All flutes in layer {layer+1} must have the same paper_type, weight, and supplier."
                )

        # calculate working width
        order_working_width = 0
        for item in data.items:
            if item.item_type == "american_box":
                sheet_width = self.db.query(AmericanBox).filter(AmericanBox.id == item.item_id).first().sheet_width
            else:
                sheet_width = self.db.query(SheetCarton).filter(SheetCarton.id == item.item_id).first().sheet_width

            if item.number_of_outs is None or sheet_width is None:
                raise HTTPException(status_code=400, detail=f"Missing number_of_outs or sheet_width for item_id {item.item_id}.")

            order_working_width += item.number_of_outs * sheet_width

        # calculate meter length
        order_meter_length = 0
        for item in data.items:
            if item.item_id == data.itemId_for_quantity:
                if item.item_type == "american_box":
                    sheet_length = self.db.query(AmericanBox).filter(AmericanBox.id == item.item_id).first().sheet_length
                else:
                    sheet_length = self.db.query(SheetCarton).filter(SheetCarton.id == item.item_id).first().sheet_length

                order_meter_length = (item.quantity / item.number_of_outs) * sheet_length

        job_order = JobOrder(
            order_type=data.order_type,
            working_width=order_working_width,
            meter_length=order_meter_length,
            calculated_weight=0,
        )

        job_order = self.repo.create(job_order)

        # link clients
        for client_id in data.client_ids:
            self.repo.add_client_link(client_id, job_order.id)

        # add items
        for item in data.items:
            if item.item_type == "american_box":
                sheet = self.db.query(AmericanBox).filter(AmericanBox.id == item.item_id).first()
                sheet_l, sheet_w = sheet.sheet_length, sheet.sheet_width
            elif item.item_type == "sheet_carton":
                sheet = self.db.query(SheetCarton).filter(SheetCarton.id == item.item_id).first()
                sheet_l, sheet_w = sheet.sheet_length, sheet.sheet_width
            else:
                sheet_l, sheet_w = 0, 0

            if item.item_id != data.itemId_for_quantity:
                item.quantity = (order_meter_length * item.number_of_outs) // sheet_l

            job_order_item = JobOrderItem(
                job_order_id=job_order.id,
                item_type=item.item_type,
                item_id=item.item_id,
                sheet_length=sheet_l,
                sheet_width=sheet_w,
                quantity=item.quantity,
                number_of_outs=item.number_of_outs,
            )
            self.repo.add_item(job_order_item)

        self.repo.save_changes()
        return job_order

    def create_roll_job_order(self, data: RollJobOrderCreate):
        roll = self.db.query(Rolls).filter(Rolls.id == data.roll_id).first()
        if not roll:
            raise HTTPException(status_code=404, detail="Roll not found.")

        fluts = self.db.query(Flut).filter(Flut.roll_id == roll.id).all()
        if len(fluts) != 2:
            raise HTTPException(status_code=400, detail="Exactly 2 fluts must be associated with this roll.")

        gsm1, gsm2 = fluts[0].weight, fluts[1].weight
        calculated_weight = (gsm1 + gsm2 * 1.4) * data.meter_length * roll.roll_width

        job_order = JobOrder(
            order_type="roll",
            working_width=roll.roll_width,
            meter_length=data.meter_length,
            calculated_weight=calculated_weight,
        )
        job_order = self.repo.create(job_order)

        for client_id in data.client_ids:
            self.repo.add_client_link(client_id, job_order.id)

        job_order_item = JobOrderItem(job_order_id=job_order.id, item_type="rolls", item_id=roll.id)
        self.repo.add_item(job_order_item)

        self.repo.save_changes()
        return job_order

    def associate_flut_with_job_order(self, job_order_id: int, data: FlutAssociationCreate):
        job_order = self.repo.get_by_id(job_order_id)
        if not job_order:
            raise HTTPException(status_code=404, detail="Job Order not found")

        job_order_items = self.db.query(JobOrderItem).filter(
            JobOrderItem.job_order_id == job_order_id,
            JobOrderItem.item_type == data.item_type,
            JobOrderItem.item_id.in_(data.item_ids)
        ).all()

        if not job_order_items:
            raise HTTPException(status_code=404, detail="No job order items found")

        paper_roll = self.db.query(PaperRoll).filter(PaperRoll.serial_number == data.paper_roll_serial).first()
        if not paper_roll:
            raise HTTPException(status_code=404, detail="Paper roll not found")

        rawmaterial = self.db.query(RawMaterial).filter(RawMaterial.id == paper_roll.raw_id).first()

        associations = []
        for item_id in data.item_ids:
            flut = self.db.query(Flut).filter(
                Flut.layer_number == data.layer_number,
                ((Flut.american_box_id == item_id) if data.item_type == "american_box" else True),
                ((Flut.sheet_carton_id == item_id) if data.item_type == "sheet_carton" else True),
                ((Flut.roll_id == item_id) if data.item_type == "rolls" else True)
            ).first()

            if not flut:
                raise HTTPException(status_code=404, detail=f"Flut not found for item ID {item_id}")

            if paper_roll.roll_width < job_order.working_width:
                raise HTTPException(status_code=400, detail="Paper roll width is less than job order working width")
            elif rawmaterial.supplier_name != flut.supplier:
                raise HTTPException(status_code=400, detail="Supplier mismatch")
            elif paper_roll.paper_type != flut.paper_type:
                raise HTTPException(status_code=400, detail="Paper type mismatch")
            elif paper_roll.gsm != flut.weight:
                raise HTTPException(status_code=400, detail="GSM mismatch")

            calculated_weight = (
                job_order.meter_length * paper_roll.gsm * paper_roll.roll_width
                if data.layer_number % 2 == 1
                else (job_order.meter_length * 1.4) * paper_roll.gsm * paper_roll.roll_width
            )

            association = JobOrderFlutRoll(
                job_order_item_id=next((item.id for item in job_order_items if item.item_id == item_id), None),
                flut_id=flut.id,
                paper_roll_id=paper_roll.id,
                allocated_width=job_order.working_width,
                calculated_weight=calculated_weight
            )
            self.repo.add_flut_roll_association(association)
            associations.append(association)

        self.repo.save_changes()
        return associations

    def get_job_order(self, order_id: int):
        order = self.repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Job Order not found")
        return order
