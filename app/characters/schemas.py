import marshmallow as ma


class EpisodeSchemaWithoutCharacters(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    air_date = ma.fields.String()
    episode = ma.fields.String()


class CharacterSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    status = ma.fields.String()
    species = ma.fields.String()
    type = ma.fields.String()
    gender = ma.fields.String()
    episodes = ma.fields.Nested(EpisodeSchemaWithoutCharacters(many=True))


class CharactersPaginationSchema(ma.Schema):
    objects = ma.fields.Nested(CharacterSchema(many=True))
    page = ma.fields.Int()
    per_page = ma.fields.Int()
    total_pages = ma.fields.Int()
    total_objects = ma.fields.Int()
