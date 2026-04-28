"""Shared models for udemy_enroller."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from udemy_enroller.logger import get_logger

logger = get_logger()


class UdemyStatus(Enum):
    """Possible statuses of udemy course."""

    ALREADY_ENROLLED = "ALREADY_ENROLLED"
    ENROLLED = "ENROLLED"
    EXPIRED = "EXPIRED"
    UNWANTED_LANGUAGE = "UNWANTED_LANGUAGE"
    UNWANTED_CATEGORY = "UNWANTED_CATEGORY"
    UNWANTED_AUTHOR = "UNWANTED_AUTHOR"
    UNWANTED_YEAR = "UNWANTED_YEAR"


@dataclass(unsafe_hash=True)
class RunStatistics:
    """Gather statistics on courses enrolled in."""

    prices: list[Decimal] = field(default_factory=list)

    expired: int = 0
    enrolled: int = 0
    already_enrolled: int = 0
    unwanted_language: int = 0
    unwanted_category: int = 0
    unwanted_author: int = 0
    unwanted_year: int = 0

    course_ids_start: int = 0
    course_ids_end: int = 0

    start_time: datetime | None = None
    end_time: datetime | None = None

    currency_symbol: str | None = None

    def savings(self) -> Decimal:
        """Calculate the savings made from enrolling to these courses."""
        return sum(self.prices) or Decimal(0)

    def table(self) -> None:
        """Log table of statistics to output."""
        if self.currency_symbol is None:
            self.currency_symbol = "$"
        logger.info("================== Run Statistics ==================")
        logger.info(f"Enrolled:                   {self.enrolled}")
        logger.info(f"Unwanted Category:          {self.unwanted_category}")
        logger.info(f"Unwanted Language:          {self.unwanted_language}")
        logger.info(f"Unwanted Author:            {self.unwanted_author}")
        logger.info(f"Unwanted Year:              {self.unwanted_year}")
        logger.info(f"Already Claimed:            {self.already_enrolled}")
        logger.info(f"Expired:                    {self.expired}")
        logger.info(f"Total Enrolments:           {self.course_ids_end}")
        logger.info(
            f"Savings:                    {self.currency_symbol}{self.savings():.2f}"
        )
        if self.start_time is not None:
            end = self.end_time or datetime.now(timezone.utc)
            run_time = int((end - self.start_time).total_seconds())
            logger.info(f"Total run time (seconds):   {run_time}s")
        logger.info("================== Run Statistics ==================")
