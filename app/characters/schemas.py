import marshmallow as ma


class CharacterQueryArgsSchema(ma.Schema):
    name = ma.fields.String()
    status = ma.fields.String()
    species = ma.fields.String()
    type = ma.fields.String()
    gender = ma.fields.String()

class EpisodeSchemaWithoutCharacters(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    air_date = ma.fields.DateTime("%B %d, %Y")
    episode = ma.fields.String()


class CharacterSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    status = ma.fields.String()
    species = ma.fields.String()
    type = ma.fields.String()
    gender = ma.fields.String()
    episodes = ma.fields.Nested(EpisodeSchemaWithoutCharacters(many=True))
