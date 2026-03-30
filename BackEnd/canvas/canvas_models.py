from canvas_databases import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, FLOAT,TIMESTAMP
from dotenv import load_dotenv
import os
# A user can use this script to create a new table without needing configure it on supabase
SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA")

class SyntheticData(Base):
    __tablename__= "synthetic_data"
    __table_args__ = {"schema":SUPABASE_SCHEMA}

    account_number = Column(String,primary_key=True)
    email = Column(String)
    name= Column(String)
    phone = Column(String)
    registration_date = Column(String)
    status = Column(String)
    timestamp = Column(String, )
    usage_amount = Column(FLOAT)
    user_id = Column(String)
    ingestion_timestamp = Column(TIMESTAMP)
    modified_timestamp = Column(TIMESTAMP)


class ControlDictionary(Base):
    __tablename__= "control_dictionary"
    __table_args__ = {"schema":SUPABASE_SCHEMA}

    anomaly_indicators = Column(String,primary_key=True)
    data_type = Column(String)
    description = Column(String)
    field_name = Column(String)
    normal_pattern = Column(String)
    ingestion_timestamp = Column(String)
    modified_timestamp = Column(TIMESTAMP)

class ControlLogic(Base):
    __tablename__= "control_logic"
    __table_args__ = {"schema":SUPABASE_SCHEMA}

    reference_number = Column(String, primary_key=True, nullable=False)
    control_logic = Column(String)
    control_logic_description = Column(String)
    control_logic_status = Column(String)
    created_timestamp = Column(TIMESTAMP)

class ControlException(Base):
    __tablename__= "control_exception"
    __table_args__ = {"schema":SUPABASE_SCHEMA}

    account_number = Column(String, nullable=False,primary_key=True)
    email = Column(String)
    name= Column(String)
    phone = Column(String)
    registration_date = Column(String)
    status = Column(String)
    timestamp = Column(String)
    usage_amount = Column(FLOAT)
    user_id = Column(String)
    detection_time = Column(TIMESTAMP, nullable=False)


class test(Base):
    __tablename__= "control_test"
    __table_args__ = {"schema":SUPABASE_SCHEMA}

    account_number = Column(String, nullable=False,primary_key=True)
    email = Column(String)
    name= Column(String)
    phone = Column(String)
    registration_date = Column(String)
    status = Column(String)
    timestamp = Column(String)
    usage_amount = Column(FLOAT)
    user_id = Column(String)
    detection_time = Column(TIMESTAMP, nullable=False)