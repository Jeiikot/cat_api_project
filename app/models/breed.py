from pydantic import BaseModel
from typing import Optional


class WeightModel(BaseModel):
    """
    Represents the weight of a breed in imperial and metric units.
    """
    imperial: Optional[str]
    metric: Optional[str]


class BreedModel(BaseModel):
    """
    Represents the data model for a cat breed retrieved from TheCatAPI.
    All fields are optional except 'id' and 'name', which are required.
    """
    id: str
    name: str
    origin: Optional[str] = None
    description: Optional[str] = None
    temperament: Optional[str] = None
    weight: Optional[WeightModel] = None
    life_span: Optional[str] = None
    adaptability: Optional[int] = None
    affection_level: Optional[int] = None
    child_friendly: Optional[int] = None
    dog_friendly: Optional[int] = None
    energy_level: Optional[int] = None
    grooming: Optional[int] = None
    intelligence: Optional[int] = None
    health_issues: Optional[int] = None
    stranger_friendly: Optional[int] = None
    vocalisation: Optional[int] = None
    experimental: Optional[int] = None
    hairless: Optional[int] = None
    natural: Optional[int] = None
    rare: Optional[int] = None
    rex: Optional[int] = None
    suppressed_tail: Optional[int] = None
    short_legs: Optional[int] = None
    wikipedia_url: Optional[str] = None
    hypoallergenic: Optional[int] = None
    reference_image_id: Optional[str] = None
    alt_names: Optional[str] = None
    indoor: Optional[int] = None
    lap: Optional[int] = None
    cfa_url: Optional[str] = None
    vetstreet_url: Optional[str] = None
    vcahospitals_url: Optional[str] = None
    country_codes: Optional[str] = None
    country_code: Optional[str] = None
    social_needs: Optional[int] = None
