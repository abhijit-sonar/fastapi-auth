from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, object_id):
        if not ObjectId.is_valid(object_id):
            raise ValueError("Invalid objectid")
        return ObjectId(object_id)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
