from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from subdomains.portfolio.domain.errors import InvalidStateError

_ASSET_CLASSES = {"주식", "채권", "통화", "금", "부동산", "가상자산", "기타자산"}
_REGIONS = {"대한민국", "미국"}
_CURRENCIES = {"KRW", "USD"}
_INVESTMENT_TYPES = {"직접", "ETF"}
_RISK_LEVELS = {"안전", "위험"}


@dataclass
class Product:
    product_id: int | None
    product_name: str
    asset_class: str
    region: str
    currency: str
    investment_type: str
    characteristics: list[str] | None
    risk_level: str
    allow_snapshot_input: bool
    display_order: int
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.product_name:
            raise InvalidStateError("product", "product_name is required")
        if self.asset_class not in _ASSET_CLASSES:
            raise InvalidStateError("product", "invalid asset_class")
        if self.region not in _REGIONS:
            raise InvalidStateError("product", "invalid region")
        if self.currency not in _CURRENCIES:
            raise InvalidStateError("product", "invalid currency")
        if self.investment_type not in _INVESTMENT_TYPES:
            raise InvalidStateError("product", "invalid investment_type")
        if self.risk_level not in _RISK_LEVELS:
            raise InvalidStateError("product", "invalid risk_level")

    @classmethod
    def create(
        cls,
        product_name: str,
        asset_class: str,
        region: str,
        currency: str,
        investment_type: str,
        characteristics: list[str] | None,
        risk_level: str,
        allow_snapshot_input: bool = True,
        display_order: int = 0,
    ) -> "Product":
        return cls(
            product_id=None,
            product_name=product_name,
            asset_class=asset_class,
            region=region,
            currency=currency,
            investment_type=investment_type,
            characteristics=characteristics,
            risk_level=risk_level,
            allow_snapshot_input=allow_snapshot_input,
            display_order=display_order,
            created_at=datetime.utcnow(),
        )

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "asset_class": self.asset_class,
            "region": self.region,
            "currency": self.currency,
            "investment_type": self.investment_type,
            "characteristics": self.characteristics,
            "risk_level": self.risk_level,
            "allow_snapshot_input": self.allow_snapshot_input,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def update(
        self,
        *,
        product_name: str,
        asset_class: str,
        region: str,
        currency: str,
        investment_type: str,
        characteristics: list[str] | None,
        risk_level: str,
        allow_snapshot_input: bool,
    ) -> None:
        self.product_name = product_name
        self.asset_class = asset_class
        self.region = region
        self.currency = currency
        self.investment_type = investment_type
        self.characteristics = characteristics
        self.risk_level = risk_level
        self.allow_snapshot_input = allow_snapshot_input
        self.__post_init__()
