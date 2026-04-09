from canvas_models import SyntheticData, ControlDictionary, ControlLogic, ControlException


class table_mapping():
    def get_orm_model(table:str):
        table_mapping = {
                    "data":SyntheticData,
                    "dictionary":ControlDictionary,
                    "logic":ControlLogic,
                    "exception":ControlException
                    }
        result = table_mapping.get(table) 
        return result
        



