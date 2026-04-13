from supabase_models import SyntheticData, ControlDictionary, ControlLogic, ControlException, ControlSummary



def get_orm_model(table: str):
    table_mapping = {
                    "data":SyntheticData,
                    "dictionary":ControlDictionary,
                    "logic":ControlLogic,
                    "exception":ControlException,
                    "summary": ControlSummary
                    }
    result = table_mapping.get(table) 
    return result
        



