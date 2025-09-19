from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy import create_engine
from alembic import context
from app.database import DATABASE_URL, Base
from app.models.raw_materials import RawMaterial
from app.models.paper_roll import PaperRoll
from app.models.adhesives_glue import AdhesivesGlue
from app.models.stitching_material import StitchingMaterial
from app.models.chemicals import Chemicals
from app.models.packaging import Packaging
from app.models.ink_and_solvents import InksandSolvents
from app.models.production_components import ProductionComponents
from app.models.employee import Employee
from app.models.employee_department import EmployeeDepartment
from app.models.department import Department
from app.models.client import ClientAccount
from app.models.american_box import AmericanBox
from app.models.sheet_carton import SheetCarton
from app.models.rolls import Rolls
from app.models.flut import Flut 
from app.models.job_order import JobOrder
from app.models.job_order_item import JobOrderItem
from app.models.gsm import Gsm
from app.models.paper_type import PaperType
from app.models.client_job_orders import ClientJobOrder
from app.models.router_access import RouterAccess
from app.models.job_order_flut_rolls import JobOrderFlutRoll
from app.models.tape import Tape

# Alembic Config object
config = context.config

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# point Alembic at your models metadata
target_metadata = Base.metadata

# --------------------------------------------------
# Include object function to ignore identity columns
def include_object(object, name, type_, reflected, compare_to):
    # Ignore id columns (identity primary keys)
    if type_ == "column" and name == "id":
        return False
    return True
# --------------------------------------------------

def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
