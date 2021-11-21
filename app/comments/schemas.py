from typing import Dict

import marshmallow as ma
from marshmallow.decorators import post_load

from ..characters.models import CharacterModel
from ..characters.schemas import EpisodeSchemaWithoutCharacters
from ..episodes.models import EpisodeModel
from ..episodes.schemas import CharacterSchemaWithoutEpisodes


class CommentSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    content = ma.fields.String()
    character = ma.fields.Nested(CharacterSchemaWithoutEpisodes())
    episode = ma.fields.Nested(EpisodeSchemaWithoutCharacters())
    created_time = ma.fields.String()
    updated_time = ma.fields.String()


class CommentsPaginationSchema(ma.Schema):
    objects = ma.fields.Nested(CommentSchema(many=True))
    page = ma.fields.Int()
    per_page = ma.fields.Int()
    total_pages = ma.fields.Int()
    total_objects = ma.fields.Int()


class CommentCreateArgsSchema(ma.Schema):
    content = ma.fields.String(required=True)
    character_id = ma.fields.Int()
    episode_id = ma.fields.Int()

    @ma.validates_schema
    def validate_requires(self, data, **kwargs) -> None:
        if "character_id" not in data and "episode_id" not in data:
            raise ma.ValidationError("One of these fields is required: [episode_id, character_id]")

    @ma.validates_schema
    def check_character_or_episode_exist(self, data, **kwargs) -> None:
        if "character_id" in data:
            character = CharacterModel.query.get(data["character_id"])
            if character is None:
                raise ma.ValidationError(f"Character doesn't exist")
            data["character"] = character

        if "episode_id" in data:
            episode = EpisodeModel.query.get(data["episode_id"])
            if episode is None:
                raise ma.ValidationError(f"Episode doesn't exist")
            data["episode"] = episode

    @post_load
    def clean_data(self, data, **kwargs) -> Dict:
        if "character_id" in data:
            del data["character_id"]
        if "episode_id" in data:
            del data["episode_id"]
        return data
