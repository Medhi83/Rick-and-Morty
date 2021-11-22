import marshmallow as ma

class EpisodeQueryArgsSchema(ma.Schema):
    name = ma.fields.String()
    episode = ma.fields.String()

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
    air_date = ma.fields.DateTime("%B %d, %Y")
    episode = ma.fields.String()
    characters = ma.fields.Nested(CharacterSchemaWithoutEpisodes(many=True))
