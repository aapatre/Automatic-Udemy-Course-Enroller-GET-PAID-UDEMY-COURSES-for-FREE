from dataclasses import dataclass
from typing import Optional


@dataclass
class RunConfig:
    browser: Optional[str]
    idownloadcoupon_enabled: bool
    freebiesglobal_enabled: bool
    tutorialbar_enabled: bool
    discudemy_enabled: bool
    coursevania_enabled: bool
    max_pages: Optional[int]
    delete_settings: bool
    delete_cookie: bool
    experimental_fuzz: bool
    fuzz_seed: Optional[int]
    max_concurrency: int
