"""Portfolio application service implementing admin/report use cases."""

import asyncio
import html
import json
import random
import re
from datetime import date, datetime, time, timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from subdomains.portfolio.application.dtos import (
    CreateInstitutionCommand,
    UpdateInstitutionCommand,
    DeleteInstitutionCommand,
    UpdateInstitutionDisplayOrdersCommand,
    CreateProductCommand,
    UpdateProductCommand,
    DeleteProductCommand,
    UpdateProductDisplayOrdersCommand,
    CreateAccountCommand,
    UpdateAccountCommand,
    DeleteAccountCommand,
    UpdateAccountDisplayOrdersCommand,
    CreateHoldingCommand,
    DeleteHoldingCommand,
    CreateSnapshotCommand,
    UpsertSnapshotHoldingCommand,
    LockSnapshotCommand,
    UnlockSnapshotCommand,
    CreateWeeklySnapshotCommand,
    CreateAnnualSnapshotCommand,
    CreateAccountGroupCommand,
    UpdateAccountGroupCommand,
    DeleteAccountGroupCommand,
    UpdateAccountGroupDisplayOrdersCommand,
    WeeklyAccountReportQuery,
    AnnualAccountReportQuery,
    WeeklyAccountGroupReportQuery,
    AnnualAccountGroupReportQuery,
    AssetClassReportQuery,
    WeeklyPivotReportQuery,
    AnnualPivotReportQuery,
    InstitutionResult,
    ProductResult,
    ProductBetaCollectionItemResult,
    ProductBetaCollectionResult,
    ProductTickerResolveResult,
    AccountResult,
    AccountGroupResult,
    HoldingResult,
    SnapshotHoldingResult,
    SnapshotResult,
    WeeklySnapshotResult,
    AnnualSnapshotResult,
    ReportItem,
    ReportResult,
    WeeklyPivotWeekInfo,
    WeeklyPivotAccountValuation,
    WeeklyPivotAccountRow,
    WeeklyPivotAccountGroupRow,
    WeeklyPivotReportResult,
    AnnualMddItem,
    WeeklyPivotAssetClassRow,
)
from subdomains.portfolio.domain import (
    Institution,
    Product,
    Account,
    AccountGroup,
    Holding,
    Snapshot,
    SnapshotHolding,
    DuplicateEntityError,
    NotFoundError,
    SnapshotLockedError,
    InvalidStateError,
    DeletionConflictError,
)
from subdomains.portfolio.domain.protocols import (
    InstitutionRepository,
    ProductRepository,
    AccountRepository,
    AccountGroupRepository,
    HoldingRepository,
    SnapshotRepository,
    ReportQueryRepository,
)
from subdomains.portfolio.application.services.target_allocation_app_service import (
    TargetAllocationAppService,
)
from shared.decorators import transactional
from shared.protocols.transaction import TransactionManager


class PortfolioAppService:
    """Application service for portfolio domain."""

    _krx_market_cache: dict[str, str] | None = None
    _krx_market_cache_expires_at: datetime | None = None
    _krx_market_cache_ttl = timedelta(hours=12)
    _krx_market_cache_lock: asyncio.Lock | None = None

    def __init__(
        self,
        institution_repo: InstitutionRepository,
        product_repo: ProductRepository,
        account_repo: AccountRepository,
        account_group_repo: AccountGroupRepository,
        holding_repo: HoldingRepository,
        snapshot_repo: SnapshotRepository,
        report_repo: ReportQueryRepository,
        transaction_manager: TransactionManager,
        target_allocation_service: TargetAllocationAppService | None = None,
    ):
        self._institution_repo = institution_repo
        self._product_repo = product_repo
        self._account_repo = account_repo
        self._account_group_repo = account_group_repo
        self._holding_repo = holding_repo
        self._snapshot_repo = snapshot_repo
        self._report_repo = report_repo
        self._txm = transaction_manager
        self.target_allocation_service = target_allocation_service

    # ------------------------------------------------------------------
    # Institutions
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_institution(
        self, command: CreateInstitutionCommand
    ) -> InstitutionResult:
        if await self._institution_repo.exists_by_name(command.name):
            raise DuplicateEntityError("institution", command.name)
        model = Institution.create(
            name=command.name,
            type=command.type,
            display_order=command.display_order,
        )
        saved = await self._institution_repo.add(model)
        return InstitutionResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_institution(
        self, command: UpdateInstitutionCommand
    ) -> InstitutionResult:
        existing = await self._institution_repo.find_by_id(command.institution_id)
        if not existing:
            raise NotFoundError("institution", command.institution_id)
        if (
            existing.name != command.name
            and await self._institution_repo.exists_by_name(command.name)
        ):
            raise DuplicateEntityError("institution", command.name)
        updated = Institution(
            institution_id=command.institution_id,
            name=command.name,
            type=command.type,
            display_order=command.display_order,
            created_at=existing.created_at,
        )
        saved = await self._institution_repo.update(updated)
        return InstitutionResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_institution_display_orders(
        self, command: UpdateInstitutionDisplayOrdersCommand
    ) -> int:
        orders = [(item.institution_id, item.display_order) for item in command.items]
        return await self._institution_repo.update_display_orders(orders)

    @transactional(mode="writable")
    async def delete_institution(self, command: DeleteInstitutionCommand) -> None:
        existing = await self._institution_repo.find_by_id(command.institution_id)
        if existing is None:
            raise NotFoundError("institution", command.institution_id)

        reference_count = await self._institution_repo.count_referencing_accounts(
            command.institution_id
        )
        if reference_count > 0:
            raise DeletionConflictError(
                "institution",
                f"institution '{command.institution_id}' is referenced by {reference_count} accounts",
            )

        await self._institution_repo.delete(command.institution_id)

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_ticker(product: Product) -> str | None:
        if product.ticker:
            normalized = product.ticker.strip().upper()
            if normalized:
                return normalized
        return None

    @staticmethod
    def _extract_krx_code(ticker: str) -> str | None:
        if len(ticker) == 7 and ticker.startswith("A") and ticker[1:].isdigit():
            return ticker[1:]
        if len(ticker) == 6 and ticker.isdigit():
            return ticker
        return None

    @staticmethod
    def _download_krx_master_html(market_type: str) -> str:
        url = (
            "https://kind.krx.co.kr/corpgeneral/corpList.do"
            f"?method=download&marketType={market_type}"
        )
        req = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
            },
        )
        with urlopen(req, timeout=15) as resp:
            raw = resp.read()
        try:
            return raw.decode("euc-kr", errors="ignore")
        except LookupError:
            return raw.decode("utf-8", errors="ignore")

    @staticmethod
    def _extract_krx_codes_from_html(document: str) -> set[str]:
        unescaped = html.unescape(document)
        matches = re.findall(
            r"mso-number-format:'@';text-align:center;\">\s*([A-Z0-9]+)\s*<",
            unescaped,
        )
        return {code for code in matches if len(code) == 6 and code.isdigit()}

    def _load_krx_market_map(self) -> dict[str, str]:
        stock_html = self._download_krx_master_html("stockMkt")
        kosdaq_html = self._download_krx_master_html("kosdaqMkt")

        stock_codes = self._extract_krx_codes_from_html(stock_html)
        kosdaq_codes = self._extract_krx_codes_from_html(kosdaq_html)

        market_map: dict[str, str] = {}
        for code in stock_codes:
            market_map[code] = ".KS"
        for code in kosdaq_codes:
            # 코스피 우선 매핑을 유지하고, 미매핑 코드만 코스닥으로 채움
            market_map.setdefault(code, ".KQ")
        return market_map

    async def _get_krx_market_map_cached(self) -> dict[str, str]:
        now = datetime.utcnow()
        cache = self.__class__._krx_market_cache
        expires_at = self.__class__._krx_market_cache_expires_at
        if cache is not None and expires_at is not None and now < expires_at:
            return cache

        if self.__class__._krx_market_cache_lock is None:
            self.__class__._krx_market_cache_lock = asyncio.Lock()

        async with self.__class__._krx_market_cache_lock:
            now = datetime.utcnow()
            cache = self.__class__._krx_market_cache
            expires_at = self.__class__._krx_market_cache_expires_at
            if cache is not None and expires_at is not None and now < expires_at:
                return cache

            loaded = await asyncio.to_thread(self._load_krx_market_map)
            self.__class__._krx_market_cache = loaded
            self.__class__._krx_market_cache_expires_at = (
                now + self.__class__._krx_market_cache_ttl
            )
            return loaded

    async def _get_krx_market_suffix_for_code(self, code: str) -> str | None:
        market_map = await self._get_krx_market_map_cached()
        return market_map.get(code)

    @staticmethod
    def _estimate_product_beta_fallback(
        product: Product,
    ) -> tuple[float | None, float | None]:
        base_by_asset_class = {
            "주식": 1.00,
            "채권": 0.25,
            "통화": 0.10,
            "금": -0.15,
            "부동산": 0.60,
            "가상자산": 1.80,
            "기타자산": 0.30,
        }
        risk_multiplier = {"안전": 0.70, "위험": 1.20}
        investment_multiplier = {"직접": 1.00, "ETF": 0.95}

        base = base_by_asset_class.get(product.asset_class, 0.30)
        risk = risk_multiplier.get(product.risk_level, 1.00)
        inv = investment_multiplier.get(product.investment_type, 1.00)
        beta = base * risk * inv

        if product.asset_class in {"통화", "채권", "기타자산"}:
            beta = max(min(beta, 0.8), -0.3)

        if product.region == "대한민국":
            domestic_beta = round(beta, 4)
            global_beta = round(beta * 0.55, 4)
        else:
            global_beta = round(beta, 4)
            domestic_beta = round(beta * 0.45, 4)

        return domestic_beta, global_beta

    @staticmethod
    def _fetch_yahoo_close_series(symbol: str, period: str = "2y") -> dict[str, float]:
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            f"?interval=1d&range={period}&includePrePost=false&events=history"
        )
        req = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
            },
        )
        with urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        result = (payload.get("chart", {}) or {}).get("result") or []
        if not result:
            return {}

        frame = result[0]
        timestamps = frame.get("timestamp") or []
        quote = ((frame.get("indicators") or {}).get("quote") or [{}])[0]
        closes = quote.get("close") or []
        if not timestamps or not closes:
            return {}

        series: dict[str, float] = {}
        for ts, close in zip(timestamps, closes):
            if close is None:
                continue
            d = datetime.utcfromtimestamp(ts).date().isoformat()
            series[d] = float(close)
        return series

    async def _fetch_yahoo_close_series_with_retry(
        self,
        symbol: str,
        period: str = "2y",
        max_attempts: int = 4,
        base_delay_sec: float = 1.0,
    ) -> dict[str, float]:
        """Yahoo API 호출에 429/일시 오류 재시도 적용.

        - 429: Retry-After 우선, 없으면 지수 백오프
        - 네트워크 일시 오류: 지수 백오프
        """
        last_error: Exception | None = None
        for attempt in range(max_attempts):
            try:
                return await asyncio.to_thread(
                    self._fetch_yahoo_close_series, symbol, period
                )
            except HTTPError as exc:
                last_error = exc
                is_retryable = exc.code == 429 or 500 <= exc.code < 600
                if not is_retryable or attempt == max_attempts - 1:
                    raise

                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                if retry_after and retry_after.isdigit():
                    delay = float(retry_after)
                else:
                    delay = base_delay_sec * (2**attempt)
            except (URLError, TimeoutError) as exc:
                last_error = exc
                if attempt == max_attempts - 1:
                    raise
                delay = base_delay_sec * (2**attempt)

            # 동일 시점 대량 요청 버스트 완화를 위해 소폭 지터 적용
            jitter = random.uniform(0.0, 0.35)
            await asyncio.sleep(min(delay + jitter, 20.0))

        if last_error:
            raise last_error
        return {}

    @staticmethod
    def _fetch_naver_close_series(symbol: str, count: int = 600) -> dict[str, float]:
        url = (
            "https://fchart.stock.naver.com/sise.nhn"
            f"?symbol={quote(symbol)}&timeframe=day&count={count}&requestType=0"
        )
        req = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
            },
        )
        with urlopen(req, timeout=15) as resp:
            raw = resp.read()

        text = raw.decode("euc-kr", errors="ignore")
        items = re.findall(r'<item\s+data="([^"]+)"\s*/>', text)
        series: dict[str, float] = {}
        for row in items:
            parts = row.split("|")
            if len(parts) < 5:
                continue
            ymd = parts[0]
            close = parts[4]
            if len(ymd) != 8:
                continue
            try:
                close_val = float(close)
            except ValueError:
                continue
            d = f"{ymd[0:4]}-{ymd[4:6]}-{ymd[6:8]}"
            series[d] = close_val
        return series

    @staticmethod
    def _fetch_stooq_close_series(symbol: str) -> dict[str, float]:
        url = f"https://stooq.com/q/d/l/?s={quote(symbol)}&i=d"
        req = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
            },
        )
        with urlopen(req, timeout=15) as resp:
            text = resp.read().decode("utf-8", errors="ignore")

        if text.strip().lower().startswith("no data"):
            return {}

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if len(lines) < 2:
            return {}

        series: dict[str, float] = {}
        for line in lines[1:]:
            parts = line.split(",")
            if len(parts) < 5:
                continue
            d = parts[0]
            close = parts[4]
            try:
                series[d] = float(close)
            except ValueError:
                continue
        return series

    @staticmethod
    def _map_symbol_for_stooq(symbol: str) -> str | None:
        normalized = symbol.strip().upper()
        if normalized == "^GSPC":
            return "^spx"
        if normalized == "^KS11":
            return "^kospi"
        if normalized.endswith(".KS") or normalized.endswith(".KQ"):
            return None
        if normalized.startswith("^"):
            return normalized.lower()
        if normalized.endswith(".US"):
            return normalized.lower()
        if "." in normalized:
            return normalized.lower()
        return f"{normalized.lower()}.us"

    def _fetch_free_close_series(self, symbol: str) -> dict[str, float]:
        normalized = symbol.strip().upper()

        # 국내 종목/국내 지수는 네이버 차트 우선
        if normalized == "^KS11":
            return self._fetch_naver_close_series("KOSPI")
        if normalized.endswith(".KS") or normalized.endswith(".KQ"):
            code = normalized.split(".", 1)[0]
            return self._fetch_naver_close_series(code)
        if len(normalized) == 6 and normalized.isdigit():
            return self._fetch_naver_close_series(normalized)

        # 해외 종목/글로벌 지수는 Stooq 사용
        mapped = self._map_symbol_for_stooq(normalized)
        if mapped:
            return self._fetch_stooq_close_series(mapped)
        return {}

    async def _fetch_close_series_with_fallback(
        self,
        symbol: str,
        period: str = "2y",
    ) -> tuple[dict[str, float], str]:
        try:
            series = await self._fetch_yahoo_close_series_with_retry(symbol, period=period)
            return series, "yahoo"
        except HTTPError as exc:
            if exc.code != 429:
                raise

            series = await asyncio.to_thread(self._fetch_free_close_series, symbol)
            if series:
                return series, "free"
            raise

    @staticmethod
    def _to_returns(prices: dict[str, float]) -> dict[str, float]:
        if len(prices) < 2:
            return {}
        ordered = sorted(prices.items(), key=lambda x: x[0])
        returns: dict[str, float] = {}
        prev = ordered[0][1]
        for d, p in ordered[1:]:
            if prev > 0:
                returns[d] = (p - prev) / prev
            prev = p
        return returns

    @staticmethod
    def _calculate_beta(
        asset_returns: dict[str, float], benchmark_returns: dict[str, float]
    ) -> float | None:
        common_dates = sorted(set(asset_returns.keys()) & set(benchmark_returns.keys()))
        if len(common_dates) < 30:
            return None

        x = [asset_returns[d] for d in common_dates]
        y = [benchmark_returns[d] for d in common_dates]
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / (n - 1)
        var_y = sum((yi - mean_y) ** 2 for yi in y) / (n - 1)
        if abs(var_y) < 1e-12:
            return None
        return round(cov / var_y, 4)

    async def _collect_product_beta_values(
        self,
        product: Product,
        benchmark_cache: dict[str, dict[str, float]],
    ) -> tuple[float | None, float | None, str]:
        ticker = self._resolve_ticker(product)
        if not ticker:
            return 0.0, 0.0, "ticker_missing_defaulted_zero"

        try:
            asset_prices, asset_provider = await self._fetch_close_series_with_fallback(
                ticker
            )
            if not asset_prices:
                return None, None, "asset_price_unavailable"

            # 과도한 연속 호출로 429를 유발하지 않도록 요청 간 짧은 간격 유지
            await asyncio.sleep(0.2)

            if "^GSPC" not in benchmark_cache:
                benchmark_cache["^GSPC"], _ = await self._fetch_close_series_with_fallback(
                    "^GSPC"
                )
                await asyncio.sleep(0.2)
            if "^KS11" not in benchmark_cache:
                benchmark_cache["^KS11"], _ = await self._fetch_close_series_with_fallback(
                    "^KS11"
                )

            asset_returns = self._to_returns(asset_prices)
            global_returns = self._to_returns(benchmark_cache["^GSPC"])
            domestic_returns = self._to_returns(benchmark_cache["^KS11"])

            global_beta = self._calculate_beta(asset_returns, global_returns)
            domestic_beta = self._calculate_beta(asset_returns, domestic_returns)

            if global_beta is None and domestic_beta is None:
                return None, None, "measured_failed_insufficient_overlap"
            if asset_provider == "free":
                return domestic_beta, global_beta, "collected_via_free_fallback"
            return domestic_beta, global_beta, "collected"
        except HTTPError as exc:
            if exc.code == 429:
                return None, None, "measured_failed_rate_limited_429"
            return None, None, f"measured_failed_external_http_{exc.code}"
        except (URLError, TimeoutError):
            return None, None, "measured_failed_external_fetch"

    @transactional(mode="writable")
    async def create_product(self, command: CreateProductCommand) -> ProductResult:
        if await self._product_repo.exists_identity(
            product_name=command.product_name,
            asset_class=command.asset_class,
            region=command.region,
            currency=command.currency,
            investment_type=command.investment_type,
        ):
            raise DuplicateEntityError("product", command.product_name)
        model = Product.create(
            product_name=command.product_name,
            asset_class=command.asset_class,
            region=command.region,
            currency=command.currency,
            investment_type=command.investment_type,
            characteristics=command.characteristics,
            risk_level=command.risk_level,
            allow_snapshot_input=command.allow_snapshot_input,
            ticker=command.ticker,
            display_order=command.display_order,
        )
        saved = await self._product_repo.add(model)
        return ProductResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_product_display_orders(
        self, command: UpdateProductDisplayOrdersCommand
    ) -> int:
        orders = [(item.product_id, item.display_order) for item in command.items]
        return await self._product_repo.update_display_orders(orders)

    @transactional(mode="writable")
    async def update_product(self, command: UpdateProductCommand) -> ProductResult:
        product = await self._product_repo.find_by_id(command.product_id)
        if product is None:
            raise NotFoundError("product", command.product_id)
        identity_changed = (
            product.product_name != command.product_name
            or product.asset_class != command.asset_class
            or product.region != command.region
            or product.currency != command.currency
            or product.investment_type != command.investment_type
        )
        if identity_changed and await self._product_repo.exists_identity(
            product_name=command.product_name,
            asset_class=command.asset_class,
            region=command.region,
            currency=command.currency,
            investment_type=command.investment_type,
        ):
            raise DuplicateEntityError("product", command.product_name)
        product.update(
            product_name=command.product_name,
            asset_class=command.asset_class,
            region=command.region,
            currency=command.currency,
            investment_type=command.investment_type,
            characteristics=command.characteristics,
            risk_level=command.risk_level,
            allow_snapshot_input=command.allow_snapshot_input,
            ticker=command.ticker,
        )
        saved = await self._product_repo.update(product)
        return ProductResult.from_domain(saved)

    @transactional(mode="writable")
    async def delete_product(self, command: DeleteProductCommand) -> None:
        existing = await self._product_repo.find_by_id(command.product_id)
        if existing is None:
            raise NotFoundError("product", command.product_id)

        reference_count = await self._product_repo.count_referencing_holdings(
            command.product_id
        )
        if reference_count > 0:
            raise DeletionConflictError(
                "product",
                f"product '{command.product_id}' is referenced by {reference_count} holdings",
            )

        await self._product_repo.delete(command.product_id)

    @transactional(mode="writable")
    async def collect_product_beta(
        self, product_id: int
    ) -> ProductBetaCollectionItemResult:
        product = await self._product_repo.find_by_id(product_id)
        if product is None:
            raise NotFoundError("product", product_id)

        benchmark_cache: dict[str, dict[str, float]] = {}
        domestic_beta, global_beta, message = await self._collect_product_beta_values(
            product, benchmark_cache
        )
        updated = False
        collected_at: datetime | None = None
        if message in {"collected", "ticker_missing_defaulted_zero"}:
            product.domestic_beta = domestic_beta
            product.global_beta = global_beta
            product.beta_collected_at = datetime.now()
            saved = await self._product_repo.update(product)
            updated = True
            collected_at = saved.beta_collected_at
        else:
            saved = product

        return ProductBetaCollectionItemResult(
            product_id=saved.product_id,
            product_name=saved.product_name,
            domestic_beta=domestic_beta,
            global_beta=global_beta,
            beta_collected_at=collected_at,
            message=message,
            updated=updated,
        )

    @transactional(mode="writable")
    async def collect_all_product_betas(self) -> ProductBetaCollectionResult:
        products = await self._product_repo.get_all()
        items: list[ProductBetaCollectionItemResult] = []
        updated_count = 0
        benchmark_cache: dict[str, dict[str, float]] = {}

        for product in products:
            domestic_beta, global_beta, message = await self._collect_product_beta_values(
                product, benchmark_cache
            )
            updated = False
            collected_at: datetime | None = None
            if message in {"collected", "ticker_missing_defaulted_zero"}:
                product.domestic_beta = domestic_beta
                product.global_beta = global_beta
                product.beta_collected_at = datetime.now()
                saved = await self._product_repo.update(product)
                updated = True
                collected_at = saved.beta_collected_at
                updated_count += 1
            else:
                saved = product
            items.append(
                ProductBetaCollectionItemResult(
                    product_id=saved.product_id,
                    product_name=saved.product_name,
                    domestic_beta=domestic_beta,
                    global_beta=global_beta,
                    beta_collected_at=collected_at,
                    message=message,
                    updated=updated,
                )
            )

        return ProductBetaCollectionResult(updated_count=updated_count, items=items)

    @transactional(mode="writable")
    async def resolve_product_ticker(self, product_id: int) -> ProductTickerResolveResult:
        product = await self._product_repo.find_by_id(product_id)
        if product is None:
            raise NotFoundError("product", product_id)

        old_ticker = product.ticker
        normalized = self._resolve_ticker(product)
        if not normalized:
            return ProductTickerResolveResult(
                product_id=product_id,
                old_ticker=old_ticker,
                new_ticker=old_ticker,
                message="ticker_missing",
                updated=False,
            )

        code = self._extract_krx_code(normalized)
        if not code:
            return ProductTickerResolveResult(
                product_id=product_id,
                old_ticker=old_ticker,
                new_ticker=normalized,
                message="ticker_not_krx_code",
                updated=False,
            )

        try:
            suffix = await self._get_krx_market_suffix_for_code(code)
        except Exception:
            return ProductTickerResolveResult(
                product_id=product_id,
                old_ticker=old_ticker,
                new_ticker=old_ticker,
                message="ticker_resolve_krx_master_unavailable",
                updated=False,
            )

        if not suffix:
            resolved_fallback = f"{code}.KS"
            if normalized == resolved_fallback:
                return ProductTickerResolveResult(
                    product_id=product_id,
                    old_ticker=old_ticker,
                    new_ticker=normalized,
                    message="ticker_already_resolved_default_ks",
                    updated=False,
                )

            product.ticker = resolved_fallback
            saved = await self._product_repo.update(product)
            return ProductTickerResolveResult(
                product_id=product_id,
                old_ticker=old_ticker,
                new_ticker=saved.ticker,
                message="ticker_resolved_default_ks",
                updated=True,
            )

        resolved = f"{code}{suffix}"
        if normalized == resolved:
            return ProductTickerResolveResult(
                product_id=product_id,
                old_ticker=old_ticker,
                new_ticker=normalized,
                message="ticker_already_resolved",
                updated=False,
            )

        product.ticker = resolved
        saved = await self._product_repo.update(product)
        return ProductTickerResolveResult(
            product_id=product_id,
            old_ticker=old_ticker,
            new_ticker=saved.ticker,
            message="ticker_resolved",
            updated=True,
        )

    # ------------------------------------------------------------------
    # Accounts
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_account(self, command: CreateAccountCommand) -> AccountResult:
        institution = await self._institution_repo.find_by_id(command.institution_id)
        if institution is None:
            raise NotFoundError("institution", command.institution_id)
        if await self._account_repo.exists_by_name(
            command.institution_id, command.name
        ):
            raise DuplicateEntityError("account", command.name)
        model = Account.create(
            institution_id=command.institution_id,
            name=command.name,
            type=command.type,
            allow_snapshot_input=command.allow_snapshot_input,
            display_order=command.display_order,
        )
        saved = await self._account_repo.add(model)
        return AccountResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_account(self, command: UpdateAccountCommand) -> AccountResult:
        account = await self._account_repo.find_by_id(command.account_id)
        if account is None:
            raise NotFoundError("account", command.account_id)
        if account.name != command.name and await self._account_repo.exists_by_name(
            account.institution_id, command.name
        ):
            raise DuplicateEntityError("account", command.name)
        account.update(
            name=command.name,
            type=command.type,
            display_order=command.display_order,
            allow_snapshot_input=command.allow_snapshot_input,
        )
        saved = await self._account_repo.update(account)
        return AccountResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_account_display_orders(
        self, command: UpdateAccountDisplayOrdersCommand
    ) -> int:
        orders = [(item.account_id, item.display_order) for item in command.items]
        return await self._account_repo.update_display_orders(orders)

    @transactional(mode="writable")
    async def delete_account(self, command: DeleteAccountCommand) -> None:
        existing = await self._account_repo.find_by_id(command.account_id)
        if existing is None:
            raise NotFoundError("account", command.account_id)

        reference_count = await self._account_repo.count_referencing_holdings(
            command.account_id
        )
        if reference_count > 0:
            raise DeletionConflictError(
                "account",
                f"account '{command.account_id}' is referenced by {reference_count} holdings",
            )

        await self._account_repo.delete(command.account_id)

    # ------------------------------------------------------------------
    # Account Groups
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_account_group(
        self, command: CreateAccountGroupCommand
    ) -> AccountGroupResult:
        if await self._account_group_repo.exists_by_name(command.name):
            raise DuplicateEntityError("account_group", command.name)
        accounts = await self._account_repo.find_many(command.account_ids)
        if len(accounts) != len(command.account_ids):
            raise NotFoundError("account", "one or more missing")
        model = AccountGroup.create(
            name=command.name,
            account_ids=command.account_ids,
            include_in_report=command.include_in_report,
        )
        saved = await self._account_group_repo.add(model)
        return AccountGroupResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_account_group(
        self, command: UpdateAccountGroupCommand
    ) -> AccountGroupResult:
        existing = await self._account_group_repo.find_by_id(command.account_group_id)
        if existing is None:
            raise NotFoundError("account_group", command.account_group_id)

        if (
            existing.name != command.name
            and await self._account_group_repo.exists_by_name(command.name)
        ):
            raise DuplicateEntityError("account_group", command.name)

        accounts = await self._account_repo.find_many(command.account_ids)
        if len(accounts) != len(command.account_ids):
            raise NotFoundError("account", "one or more missing")

        updated = AccountGroup(
            account_group_id=existing.account_group_id,
            name=command.name,
            account_ids=command.account_ids,
            include_in_report=command.include_in_report,
            display_order=existing.display_order,
            created_at=existing.created_at,
        )
        saved = await self._account_group_repo.update(updated)
        return AccountGroupResult.from_domain(saved)

    @transactional(mode="writable")
    async def delete_account_group(self, command: DeleteAccountGroupCommand) -> None:
        try:
            existing = await self._account_group_repo.find_by_id(
                command.account_group_id
            )
        except InvalidStateError as exc:
            # Some legacy/corrupted rows may have no linked account.
            # Allow deletion flow to proceed for these rows.
            if "at least one account is required" in str(exc):
                existing = True
            else:
                raise
        if existing is None:
            raise NotFoundError("account_group", command.account_group_id)
        await self._account_group_repo.delete(command.account_group_id)

    @transactional(mode="writable")
    async def update_account_group_display_orders(
        self, command: UpdateAccountGroupDisplayOrdersCommand
    ) -> int:
        orders = [(item.account_group_id, item.display_order) for item in command.items]
        return await self._account_group_repo.update_display_orders(orders)

    # ------------------------------------------------------------------
    # Holdings
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_holding(self, command: CreateHoldingCommand) -> HoldingResult:
        account = await self._account_repo.find_by_id(command.account_id)
        if account is None:
            raise NotFoundError("account", command.account_id)
        product = await self._product_repo.find_by_id(command.product_id)
        if product is None:
            raise NotFoundError("product", command.product_id)
        if await self._holding_repo.exists_by_account_product(
            command.account_id, command.product_id
        ):
            raise DuplicateEntityError(
                "holding", f"{command.account_id}-{command.product_id}"
            )
        model = Holding.create(
            account_id=command.account_id, product_id=command.product_id
        )
        saved = await self._holding_repo.add(model)
        return HoldingResult.from_domain(saved)

    @transactional(mode="writable")
    async def delete_holding(
        self, command: DeleteHoldingCommand
    ) -> HoldingResult | None:
        holding = await self._holding_repo.find_by_id(command.holding_id)
        if holding is None:
            raise NotFoundError("holding", command.holding_id)
        action = command.action
        if action == "hide":
            holding.hide(command.reason)
            saved = await self._holding_repo.hide(holding, command.reason)
            return HoldingResult.from_domain(saved)
        if action == "hard_delete":
            reference_count = (
                await self._holding_repo.count_referencing_snapshot_holdings(
                    command.holding_id
                )
            )
            if reference_count > 0:
                raise DeletionConflictError(
                    "holding",
                    f"holding '{command.holding_id}' is referenced by {reference_count} snapshot holdings",
                )
            await self._holding_repo.hard_delete(command.holding_id)
            return None
        raise ValueError("Unsupported action for delete_holding")

    # ------------------------------------------------------------------
    # Snapshots
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_snapshot(self, command: CreateSnapshotCommand) -> SnapshotResult:
        existing = await self._snapshot_repo.find_by_reference(
            command.user_id, command.reference_date
        )
        if existing:
            raise DuplicateEntityError("snapshot", str(command.reference_date))
        model = Snapshot.create(
            user_id=command.user_id, reference_date=command.reference_date
        )
        saved = await self._snapshot_repo.add(model)
        return SnapshotResult.from_domain(saved)

    @transactional(mode="writable")
    async def upsert_snapshot_holding(
        self, command: UpsertSnapshotHoldingCommand
    ) -> SnapshotHoldingResult:
        snapshot = await self._snapshot_repo.find_by_id(command.snapshot_id)
        if snapshot is None:
            raise NotFoundError("snapshot", command.snapshot_id)

        holding = await self._holding_repo.find_by_id(command.holding_id)
        if holding is None:
            raise NotFoundError("holding", command.holding_id)

        product = await self._product_repo.find_by_id(holding.product_id)
        if product is None:
            raise NotFoundError("product", holding.product_id)

        account = await self._account_repo.find_by_id(holding.account_id)
        if account is None:
            raise NotFoundError("account", holding.account_id)
        if not product.allow_snapshot_input:
            raise InvalidStateError(
                "snapshot_holding",
                f"snapshot input is disabled for product '{product.product_name}'",
            )
        if not account.allow_snapshot_input:
            raise InvalidStateError(
                "snapshot_holding",
                f"snapshot input is disabled for account '{account.name}'",
            )

        snapshot.upsert_holding(
            holding_id=command.holding_id,
            valuation_amount=command.valuation_amount,
            data_source=command.data_source,
        )
        sh = SnapshotHolding(
            holding_id=command.holding_id,
            valuation_amount=command.valuation_amount,
            data_source=command.data_source,
        )
        saved = await self._snapshot_repo.save_holding(command.snapshot_id, sh)
        return SnapshotHoldingResult.from_domain(saved)

    @transactional(mode="writable")
    async def lock_snapshot(self, command: LockSnapshotCommand) -> None:
        snapshot = await self._snapshot_repo.find_by_id(command.snapshot_id)
        if snapshot is None:
            raise NotFoundError("snapshot", command.snapshot_id)
        snapshot.lock()
        await self._snapshot_repo.lock(command.snapshot_id)

    @transactional(mode="writable")
    async def unlock_snapshot(self, command: UnlockSnapshotCommand) -> None:
        from subdomains.portfolio.domain.errors import SnapshotUnlockNotAllowedError

        snapshot = await self._snapshot_repo.find_by_id(command.snapshot_id)
        if snapshot is None:
            raise NotFoundError("snapshot", command.snapshot_id)

        # 기준일보다 늦은 잠금된 스냅샷이 있는지 확인
        has_later_locked = await self._snapshot_repo.has_later_locked_snapshots(
            snapshot.user_id, snapshot.reference_date
        )
        if has_later_locked:
            raise SnapshotUnlockNotAllowedError(
                command.snapshot_id,
                "There are locked snapshots with later reference dates",
            )

        # 도메인 규칙 검증 (상태 및 7일 제한)
        snapshot.unlock()
        await self._snapshot_repo.unlock(command.snapshot_id)

    @transactional(mode="writable")
    async def create_weekly_snapshot(self, command: CreateWeeklySnapshotCommand) -> int:
        source = await self._snapshot_repo.find_by_id(command.source_snapshot_id)
        if source is None:
            raise NotFoundError("snapshot", command.source_snapshot_id)
        if source.status != "locked":
            raise SnapshotLockedError(source.snapshot_id or 0)
        editable_until = datetime.combine(command.reference_date, time.min) + timedelta(
            days=7
        )
        return await self._snapshot_repo.clone_weekly(
            source_snapshot_id=command.source_snapshot_id,
            user_id=command.user_id,
            reference_date=command.reference_date,
            status="in_progress",
            editable_until=editable_until,
        )

    @transactional(mode="writable")
    async def create_annual_snapshot(self, command: CreateAnnualSnapshotCommand) -> int:
        source = await self._snapshot_repo.find_by_id(command.source_snapshot_id)
        if source is None:
            raise NotFoundError("snapshot", command.source_snapshot_id)
        if source.status != "locked":
            raise SnapshotLockedError(source.snapshot_id or 0)
        return await self._snapshot_repo.clone_annual(
            source_snapshot_id=command.source_snapshot_id,
            user_id=command.user_id,
            reference_date=command.reference_date,
        )

    # ------------------------------------------------------------------
    # Reports (쿼리 시점 실시간 집계)
    # ------------------------------------------------------------------

    @transactional(mode="readonly")
    async def weekly_account_report(
        self, query: WeeklyAccountReportQuery
    ) -> ReportResult:
        rows = await self._report_repo.weekly_account_report(
            query.user_id, query.start_date, query.end_date
        )
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("total_valuation", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    @transactional(mode="readonly")
    async def annual_account_report(
        self, query: AnnualAccountReportQuery
    ) -> ReportResult:
        rows = await self._report_repo.annual_account_report(query.user_id, query.year)
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("total_valuation", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    @transactional(mode="readonly")
    async def weekly_account_group_report(
        self, query: WeeklyAccountGroupReportQuery
    ) -> ReportResult:
        rows = await self._report_repo.weekly_account_group_report(
            query.user_id, query.start_date, query.end_date
        )
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("group_total", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    @transactional(mode="readonly")
    async def annual_account_group_report(
        self, query: AnnualAccountGroupReportQuery
    ) -> ReportResult:
        rows = await self._report_repo.annual_account_group_report(
            query.user_id, query.year
        )
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("group_total", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    @transactional(mode="readonly")
    async def asset_class_report(self, query: AssetClassReportQuery) -> ReportResult:
        rows = await self._report_repo.asset_class_report(
            query.user_id, query.snapshot_date
        )
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("subtotal", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    @transactional(mode="readonly")
    async def annual_snapshot_holdings_report(
        self, annual_snapshot_id: int
    ) -> ReportResult:
        rows = await self._report_repo.get_annual_snapshot_holdings(annual_snapshot_id)
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("valuation_amount", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    @transactional(mode="readonly")
    async def weekly_pivot_report(
        self, query: WeeklyPivotReportQuery
    ) -> WeeklyPivotReportResult:
        """주간 Pivot 보고서: 연도별 모든 주간 스냅샷을 열로 표시"""
        # 1. 주간 스냅샷 목록 조회
        weekly_snapshots = await self._snapshot_repo.get_weekly_by_user(query.user_id)

        # 2. 해당 연도 필터링
        year_snapshots = [
            snap for snap in weekly_snapshots if snap.reference_date.year == query.year
        ]
        year_snapshots.sort(key=lambda x: x.reference_date)

        # 3. 전년도 12월 마지막 주 스냅샷 추가 (전주/전월 대비 계산용)
        prev_year = query.year - 1
        prev_december_snapshots = [
            snap
            for snap in weekly_snapshots
            if snap.reference_date.year == prev_year and snap.reference_date.month == 12
        ]
        if prev_december_snapshots:
            # 12월의 마지막 스냅샷 찾기
            prev_december_snapshots.sort(key=lambda x: x.reference_date)
            last_prev_december = prev_december_snapshots[-1]
            # year_snapshots 맨 앞에 추가
            year_snapshots.insert(0, last_prev_december)

        if not year_snapshots:
            return WeeklyPivotReportResult(
                year=query.year, weeks=[], account_groups=[], accounts=[]
            )

        # 4. 주차 정보 생성
        weeks = [
            WeeklyPivotWeekInfo(
                weekly_snapshot_id=snap.weekly_snapshot_id,
                reference_date=snap.reference_date,
                week_number=snap.reference_date.isocalendar()[1],  # ISO week number
            )
            for snap in year_snapshots
        ]

        # 5. 각 주간 스냅샷의 보유자산 데이터 조회
        # @use_transaction() 데코레이터가 context_var에서 conn을 자동으로 가져와 주입
        weekly_holdings_data = await self._report_repo.get_weekly_snapshot_holdings(
            [snap.weekly_snapshot_id for snap in year_snapshots]
        )

        # 5-1. Institution의 display_order 정보 조회 (정렬용)
        institutions = await self._institution_repo.get_all()
        inst_display_orders = {
            inst.institution_id: inst.display_order for inst in institutions
        }

        # 6. 계좌별/자산유형별 그룹화
        account_map = {}
        asset_class_map: dict[str, dict] = {}
        for row in weekly_holdings_data:
            account_id = row.get("account_id")
            if account_id not in account_map:
                account_map[account_id] = {
                    "account_id": account_id,
                    "institution_id": row.get("institution_id"),
                    "account_name": row.get("account_name"),
                    "institution_name": row.get("institution_name"),
                    "display_order": row.get("display_order"),
                    "valuations": {},
                }

            weekly_snapshot_id = row.get("weekly_snapshot_id")
            amount = float(row.get("valuation_amount", 0) or 0)

            if weekly_snapshot_id not in account_map[account_id]["valuations"]:
                account_map[account_id]["valuations"][weekly_snapshot_id] = 0
            account_map[account_id]["valuations"][weekly_snapshot_id] += amount

            asset_class = row.get("asset_class", "기타자산")
            if asset_class not in asset_class_map:
                asset_class_map[asset_class] = {"valuations": {}}
            if weekly_snapshot_id not in asset_class_map[asset_class]["valuations"]:
                asset_class_map[asset_class]["valuations"][weekly_snapshot_id] = 0
            asset_class_map[asset_class]["valuations"][weekly_snapshot_id] += amount

        # 7. 계좌별 행 데이터 생성 및 정렬 (institution의 display_order, account의 display_order 순서로)
        accounts = []
        for account_data in sorted(
            account_map.values(),
            key=lambda x: (
                inst_display_orders.get(x["institution_id"], 999),
                x["display_order"],
            ),
        ):
            valuations = [
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=snap.weekly_snapshot_id,
                    amount=account_data["valuations"].get(snap.weekly_snapshot_id, 0.0),
                )
                for snap in year_snapshots
            ]

            accounts.append(
                WeeklyPivotAccountRow(
                    account_id=account_data["account_id"],
                    account_name=account_data["account_name"],
                    institution_name=account_data["institution_name"],
                    valuations=valuations,
                )
            )

        # 8. 계좌그룹 행 데이터 생성 (include_in_report=True인 그룹들)
        account_group_rows = []
        account_groups = await self._account_group_repo.get_all()
        for group in account_groups:
            if not group.include_in_report:
                continue

            # 해당 그룹에 속한 계좌들의 평가액을 주차별로 합산
            group_valuations_by_week = {}
            for account_id in group.account_ids:
                if account_id in account_map:
                    for week_id, amount in account_map[account_id][
                        "valuations"
                    ].items():
                        if week_id not in group_valuations_by_week:
                            group_valuations_by_week[week_id] = 0
                        group_valuations_by_week[week_id] += amount

            valuations = [
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=snap.weekly_snapshot_id,
                    amount=group_valuations_by_week.get(snap.weekly_snapshot_id, 0.0),
                )
                for snap in year_snapshots
            ]

            account_group_rows.append(
                WeeklyPivotAccountGroupRow(
                    account_group_id=group.account_group_id,
                    account_group_name=group.name,
                    display_order=group.display_order,
                    valuations=valuations,
                )
            )

        asset_class_order = ["주식", "채권", "통화", "금", "부동산", "가상자산", "기타자산"]
        asset_class_rows = []
        for asset_class in asset_class_order:
            valuations = [
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=snap.weekly_snapshot_id,
                    amount=asset_class_map.get(asset_class, {"valuations": {}})[
                        "valuations"
                    ].get(snap.weekly_snapshot_id, 0.0),
                )
                for snap in year_snapshots
            ]
            asset_class_rows.append(
                WeeklyPivotAssetClassRow(
                    asset_class=asset_class,
                    valuations=valuations,
                )
            )

        return WeeklyPivotReportResult(
            year=query.year,
            weeks=weeks,
            account_groups=account_group_rows,
            accounts=accounts,
            asset_classes=asset_class_rows,
        )

    @transactional(mode="readonly")
    async def annual_pivot_report(
        self, query: AnnualPivotReportQuery
    ) -> WeeklyPivotReportResult:
        """연간 Pivot 보고서: 모든 연간 스냅샷을 열로 표시 (include_in_report=True인 계좌그룹만)"""
        # 1. 연간 스냅샷 목록 조회
        year_snapshots = await self._snapshot_repo.get_annual_by_user(query.user_id)
        year_snapshots.sort(key=lambda x: x.reference_date)

        if not year_snapshots:
            return WeeklyPivotReportResult(
                year=0, weeks=[], account_groups=[], accounts=[]
            )

        # 2. 연간 스냅샷을 기준으로 열 정보 생성
        weeks = [
            WeeklyPivotWeekInfo(
                weekly_snapshot_id=snap.annual_snapshot_id,
                reference_date=snap.reference_date,
                week_number=snap.reference_date.year - 1,
            )
            for snap in year_snapshots
        ]

        # 3. 각 연간 스냅샷의 보유자산 데이터 조회 및 계좌별/자산유형별 집계
        account_map: dict[int, dict] = {}
        asset_class_map: dict[str, dict] = {}
        for snapshot in year_snapshots:
            annual_holdings_data = await self._report_repo.get_annual_snapshot_holdings(
                snapshot.annual_snapshot_id
            )
            for row in annual_holdings_data:
                account_id = row.get("account_id")
                if account_id not in account_map:
                    account_map[account_id] = {
                        "account_id": account_id,
                        "institution_id": row.get("institution_id"),
                        "account_name": row.get("account_name"),
                        "institution_name": row.get("institution_name"),
                        "display_order": row.get("account_display_order"),
                        "valuations": {},
                    }

                annual_snapshot_id = row.get("annual_snapshot_id")
                amount = float(row.get("valuation_amount", 0) or 0)
                if annual_snapshot_id not in account_map[account_id]["valuations"]:
                    account_map[account_id]["valuations"][annual_snapshot_id] = 0
                account_map[account_id]["valuations"][annual_snapshot_id] += amount

                # 자산유형별 합계 계산
                asset_class = row.get("asset_class", "기타자산")
                if asset_class not in asset_class_map:
                    asset_class_map[asset_class] = {"valuations": {}}
                if annual_snapshot_id not in asset_class_map[asset_class]["valuations"]:
                    asset_class_map[asset_class]["valuations"][annual_snapshot_id] = 0
                asset_class_map[asset_class]["valuations"][annual_snapshot_id] += amount

        # 4. Institution display_order 조회 (정렬용)
        institutions = await self._institution_repo.get_all()
        inst_display_orders = {
            inst.institution_id: inst.display_order for inst in institutions
        }

        # 5. 계좌 행 데이터 생성 및 정렬
        accounts = []
        for account_data in sorted(
            account_map.values(),
            key=lambda x: (
                inst_display_orders.get(x["institution_id"], 999),
                x["display_order"],
            ),
        ):
            valuations = [
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=snap.annual_snapshot_id,
                    amount=account_data["valuations"].get(snap.annual_snapshot_id, 0.0),
                )
                for snap in year_snapshots
            ]

            accounts.append(
                WeeklyPivotAccountRow(
                    account_id=account_data["account_id"],
                    account_name=account_data["account_name"],
                    institution_name=account_data["institution_name"],
                    valuations=valuations,
                )
            )

        # 6. 계좌그룹 행 데이터 생성 (include_in_report=True인 그룹들)
        account_group_rows = []
        account_groups = await self._account_group_repo.get_all()
        for group in account_groups:
            if not group.include_in_report:
                continue

            # 해당 그룹에 속한 계좌들의 평가액을 연간 스냅샷별로 합산
            group_valuations_by_snapshot = {}
            for account_id in group.account_ids:
                if account_id in account_map:
                    for snapshot_id, amount in account_map[account_id][
                        "valuations"
                    ].items():
                        if snapshot_id not in group_valuations_by_snapshot:
                            group_valuations_by_snapshot[snapshot_id] = 0
                        group_valuations_by_snapshot[snapshot_id] += amount

            valuations = [
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=snap.annual_snapshot_id,
                    amount=group_valuations_by_snapshot.get(
                        snap.annual_snapshot_id, 0.0
                    ),
                )
                for snap in year_snapshots
            ]

            account_group_rows.append(
                WeeklyPivotAccountGroupRow(
                    account_group_id=group.account_group_id,
                    account_group_name=group.name,
                    display_order=group.display_order,
                    valuations=valuations,
                )
            )

        # 7. 자산유형별 행 데이터 생성 (고정 순서)
        asset_class_order = ["주식", "채권", "통화", "금", "부동산", "가상자산", "기타자산"]
        asset_class_rows = []
        for asset_class in asset_class_order:
            valuations = [
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=snap.annual_snapshot_id,
                    amount=asset_class_map.get(asset_class, {"valuations": {}})[
                        "valuations"
                    ].get(snap.annual_snapshot_id, 0.0),
                )
                for snap in year_snapshots
            ]
            asset_class_rows.append(
                WeeklyPivotAssetClassRow(
                    asset_class=asset_class,
                    valuations=valuations,
                )
            )

        return WeeklyPivotReportResult(
            year=0,  # 연간 보고서는 연도 구분이 없음
            weeks=weeks,
            account_groups=account_group_rows,
            accounts=accounts,
            asset_classes=asset_class_rows,
            mdd_by_year=await self._compute_annual_mdd(
                user_id=query.user_id,
                year_snapshots=year_snapshots,
                account_groups=[g for g in account_groups if g.include_in_report],
            ),
        )

    @transactional(mode="readonly")
    async def get_institution_assets(self, user_id: int) -> list[dict]:
        """금융기관별 최근 주간스냅샷 기준 자산총합 조회"""
        return await self._report_repo.institution_assets_report(user_id)

    # ------------------------------------------------------------------
    # List/Read Operations
    # ------------------------------------------------------------------

    async def _compute_annual_mdd(
        self,
        user_id: int,
        year_snapshots: list,
        account_groups: list,
    ) -> list[AnnualMddItem]:
        """연도별 MDD(Maximum Drawdown)를 주간 스냅샷으로부터 계산한다.

        각 연간 스냅샷의 데이터 연도(reference_date.year - 1)에 해당하는
        주간 스냅샷들의 include_in_report 계좌그룹 총액을 집계하여
        MDD = (최저총액 - 최고총액) / 최고총액 × 100 을 반환한다.
        """
        if not year_snapshots:
            return []

        # include_in_report 계좌그룹에 속한 계좌 ID 집합
        included_account_ids: set[int] = set()
        for grp in account_groups:
            included_account_ids.update(grp.account_ids)

        # 전체 주간 스냅샷 조회 (@use_transaction이 현재 트랜잭션을 자동으로 주입)
        all_weekly = await self._snapshot_repo.get_weekly_by_user(user_id)

        mdd_items: list[AnnualMddItem] = []
        for snap in year_snapshots:
            data_year = snap.reference_date.year - 1

            year_weekly = sorted(
                [ws for ws in all_weekly if ws.reference_date.year == data_year],
                key=lambda x: x.reference_date,
            )

            if len(year_weekly) < 2:
                mdd_items.append(
                    AnnualMddItem(
                        data_year=data_year,
                        annual_snapshot_id=snap.annual_snapshot_id,
                        peak_amount=0.0,
                        trough_amount=0.0,
                        mdd_percentage=0.0,
                        weekly_snapshot_count=len(year_weekly),
                    )
                )
                continue

            # 해당 연도 주간 스냅샷 보유자산 일괄 조회
            weekly_ids = [ws.weekly_snapshot_id for ws in year_weekly]
            holdings_data = await self._report_repo.get_weekly_snapshot_holdings(weekly_ids)

            # 주간 스냅샷별 include_in_report 계좌 총액 집계
            totals_by_ws: dict[int, float] = {ws_id: 0.0 for ws_id in weekly_ids}
            for row in holdings_data:
                account_id = row.get("account_id")
                ws_id = row.get("weekly_snapshot_id")
                if account_id in included_account_ids and ws_id in totals_by_ws:
                    totals_by_ws[ws_id] += float(row.get("valuation_amount", 0) or 0)

            # 날짜 순서가 보장된 주간 총액 시계열
            ordered_totals = [totals_by_ws[ws.weekly_snapshot_id] for ws in year_weekly]
            nonzero_totals = [v for v in ordered_totals if v > 0]

            if not nonzero_totals:
                mdd_items.append(
                    AnnualMddItem(
                        data_year=data_year,
                        annual_snapshot_id=snap.annual_snapshot_id,
                        peak_amount=0.0,
                        trough_amount=0.0,
                        mdd_percentage=0.0,
                        weekly_snapshot_count=len(year_weekly),
                    )
                )
                continue

            # 올바른 MDD: 시간 순서대로 진행하며 직전 최고점 대비 현재 낙폭의 최댓값
            # 꾸준히 상승하기만 하면 MDD = 0.0%
            running_peak = ordered_totals[0]
            mdd_pct = 0.0
            mdd_peak = running_peak
            mdd_trough = running_peak
            for v in ordered_totals[1:]:
                if v <= 0:
                    continue
                if v > running_peak:
                    running_peak = v
                else:
                    drawdown = (v - running_peak) / running_peak * 100
                    if drawdown < mdd_pct:
                        mdd_pct = drawdown
                        mdd_peak = running_peak
                        mdd_trough = v

            mdd_items.append(
                AnnualMddItem(
                    data_year=data_year,
                    annual_snapshot_id=snap.annual_snapshot_id,
                    peak_amount=mdd_peak,
                    trough_amount=mdd_trough,
                    mdd_percentage=mdd_pct,
                    weekly_snapshot_count=len(year_weekly),
                )
            )

        return mdd_items

    @transactional(mode="readonly")
    async def list_institutions(self) -> list[InstitutionResult]:
        """조회: 모든 금융기관 목록"""
        institutions = await self._institution_repo.get_all()
        return [
            InstitutionResult(
                institution_id=inst.institution_id,
                name=inst.name,
                type=inst.type,
                display_order=inst.display_order,
                created_at=inst.created_at,
            )
            for inst in institutions
        ]

    @transactional(mode="readonly")
    async def list_products(self) -> list[ProductResult]:
        """조회: 모든 상품 목록"""
        products = await self._product_repo.get_all()
        return [
            ProductResult(
                product_id=prod.product_id,
                product_name=prod.product_name,
                asset_class=prod.asset_class,
                region=prod.region,
                currency=prod.currency,
                investment_type=prod.investment_type,
                characteristics=prod.characteristics,
                risk_level=prod.risk_level,
                allow_snapshot_input=prod.allow_snapshot_input,
                ticker=prod.ticker,
                display_order=prod.display_order,
                created_at=prod.created_at,
                domestic_beta=prod.domestic_beta,
                global_beta=prod.global_beta,
                beta_collected_at=prod.beta_collected_at,
            )
            for prod in products
        ]

    @transactional(mode="readonly")
    async def list_accounts(self) -> list[AccountResult]:
        """조회: 모든 계좌 목록"""
        accounts = await self._account_repo.get_all()
        return [
            AccountResult(
                account_id=acc.account_id,
                institution_id=acc.institution_id,
                name=acc.name,
                type=acc.type,
                allow_snapshot_input=acc.allow_snapshot_input,
                display_order=acc.display_order,
                created_at=acc.created_at,
            )
            for acc in accounts
        ]

    @transactional(mode="readonly")
    async def list_account_groups(self) -> list[AccountGroupResult]:
        """조회: 모든 계좌 그룹 목록"""
        groups = await self._account_group_repo.get_all()
        return [AccountGroupResult.from_domain(group) for group in groups]

    @transactional(mode="readonly")
    async def list_snapshots(self, user_id: int) -> list[SnapshotResult]:
        """조회: 사용자의 모든 스냅샷"""
        snapshots = await self._snapshot_repo.get_all()
        # 사용자 필터링
        user_snapshots = [s for s in snapshots if s.user_id == user_id]
        return [
            SnapshotResult(
                snapshot_id=snap.snapshot_id,
                user_id=snap.user_id,
                reference_date=snap.reference_date,
                status=snap.status,
                locked_at=snap.locked_at,
                editable_until=snap.editable_until,
                created_at=snap.created_at,
                holdings=[],
            )
            for snap in user_snapshots
        ]

    @transactional(mode="readonly")
    async def list_weekly_snapshots(self, user_id: int) -> list[WeeklySnapshotResult]:
        """조회: 사용자의 모든 주간 스냅샷"""
        snapshots = await self._snapshot_repo.get_weekly_by_user(user_id)
        return [WeeklySnapshotResult.from_domain(snap) for snap in snapshots]

    @transactional(mode="readonly")
    async def list_annual_snapshots(self, user_id: int) -> list[AnnualSnapshotResult]:
        """조회: 사용자의 모든 연간 스냅샷"""
        snapshots = await self._snapshot_repo.get_annual_by_user(user_id)
        return [AnnualSnapshotResult.from_domain(snap) for snap in snapshots]

    @transactional(mode="readonly")
    async def list_holdings(self) -> list[HoldingResult]:
        """조회: 모든 보유자산 목록"""
        holdings = await self._holding_repo.get_all()
        return [
            HoldingResult(
                holding_id=h.holding_id,
                account_id=h.account_id,
                product_id=h.product_id,
                is_visible=h.is_visible,
                deleted_at=h.deleted_at,
                deletion_reason=h.deletion_reason,
                created_at=h.created_at,
            )
            for h in holdings
        ]

    @transactional(mode="readonly")
    async def list_snapshot_holdings(self) -> list[SnapshotHoldingResult]:
        """조회: 모든 스냅샷 보유자산"""
        snapshots = await self._snapshot_repo.get_all()
        result = []
        for snapshot in snapshots:
            for holding in snapshot.holdings:
                result.append(
                    SnapshotHoldingResult(
                        snapshot_id=snapshot.snapshot_id,
                        holding_id=holding.holding_id,
                        valuation_amount=holding.valuation_amount,
                        data_source=holding.data_source,
                    )
                )
        return result
