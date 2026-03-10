from dataclasses import dataclass


@dataclass
class BrandInput:
    brand_name: str
    website_url: str
    location: str
    product_service: str
    current_problem: str
    brand_stage: str
