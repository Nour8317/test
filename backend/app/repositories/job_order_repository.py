from sqlalchemy.orm import Session
from app.models.job_order import JobOrder
from app.models.job_order_item import JobOrderItem
from app.models.client_job_orders import ClientJobOrder

class JobOrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_job_order(self, job_order: JobOrder):
        self.db.add(job_order)
        self.db.commit()
        self.db.refresh(job_order)
        return job_order

    def add_client_link(self, client_id: int, job_order_id: int):
        link = ClientJobOrder(client_id=client_id, job_order_id=job_order_id)
        self.db.add(link)
        return link

    def add_job_order_item(self, job_order_item: JobOrderItem):
        self.db.add(job_order_item)
        return job_order_item

    def get_by_id(self, order_id: int):
        return self.db.query(JobOrder).filter(JobOrder.id == order_id).first()
