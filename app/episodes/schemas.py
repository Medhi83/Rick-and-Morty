import marshmallow as ma


class CharacterSchemaWithoutEpisodes(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    status = ma.fields.String()
    species = ma.fields.String()
    type = ma.fields.String()
    gender = ma.fields.String()


class EpisodeSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    air_date = ma.fields.String()
    episode = ma.fields.String()
    characters = ma.fields.Nested(CharacterSchemaWithoutEpisodes(many=True))


class EpisodesPaginationSchema(ma.Schema):
    objects = ma.fields.Nested(EpisodeSchema(many=True))
    page = ma.fields.Int()
    per_page = ma.fields.Int()
    total_pages = ma.fields.Int()
    total_objects = ma.fields.Int()
