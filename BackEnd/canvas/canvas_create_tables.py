# create_tables.py
from canvas_databases import Base, engine
import canvas_models   # ensures all models are registered with Base.metadata

## -TODO 
# We need to create a workflow that executes this python file.
print("Creating tables...")
Base.metadata.create_all(engine)
print("Done.")