'use client';

import React, { useEffect, useRef, useState } from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, ComposedChart, Bar, BarChart } from 'recharts';
import styles from './portfolio.module.css';
import {
  filterSnapshotInputEligibleHoldings,
  filterSnapshotInputVisibleHoldings,
  isAccountAllowedForSnapshotInput,
  isProductAllowedForSnapshotInput,
} from './snapshotInputPolicy';

interface User {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
}

interface Institution {
  institution_id: number;
  name: string;
  type: string;
  display_order: number;
  created_at: string;
  total_assets?: number;
}

interface Product {
  product_id: number;
  product_name: string;
  asset_class: string;
  region: string;
  currency: string;
  investment_type: string;
  characteristics?: string[];
  risk_level: string;
  allow_snapshot_input: boolean;
  ticker?: string | null;
  domestic_beta?: number | null;
  global_beta?: number | null;
  beta_collected_at?: string | null;
  display_order: number;
  created_at: string;
}

interface Account {
  account_id: number;
  institution_id: number;
  name: string;
  type: string;
  allow_snapshot_input: boolean;
  display_order: number;
  created_at: string;
}

interface AccountGroup {
  account_group_id: number;
  name: string;
  account_ids: number[];
  include_in_report: boolean;
  display_order: number;
  created_at: string;
}

interface Snapshot {
  snapshot_id: number;
  user_id: number;
  reference_date: string;
  status: string;
  locked_at: string | null;
  editable_until: string | null;
  created_at: string;
}

interface WeeklySnapshot {
  weekly_snapshot_id: number;
  user_id: number;
  reference_date: string;
  source_snapshot_id: number;
  status: string;
  created_at: string;
}

interface AnnualSnapshot {
  annual_snapshot_id: number;
  user_id: number;
  reference_date: string;
  source_snapshot_id: number;
  status: string;
  created_at: string;
}

interface AnnualSnapshotHolding {
  annual_snapshot_holding_id: number;
  annual_snapshot_id: number;
  holding_id: number;
  valuation_amount: number;
  data_source: string;
  created_at: string;
  institution_id: number;
  institution_name: string;
  institution_display_order: number;
  account_id: number;
  account_name: string;
  account_display_order: number;
  product_id: number;
  product_name: string;
  product_display_order: number;
}

interface WeeklyPivotWeekInfo {
  weekly_snapshot_id: number;
  reference_date: string;
  week_number: number;
}

interface WeeklyPivotAccountValuation {
  weekly_snapshot_id: number;
  amount: number;
}

interface WeeklyPivotAccountRow {
  account_id: number;
  account_name: string;
  institution_name: string;
  valuations: WeeklyPivotAccountValuation[];
}

interface WeeklyPivotAccountGroupRow {
  account_group_id: number;
  account_group_name: string;
  display_order: number;
  valuations: WeeklyPivotAccountValuation[];
}

interface WeeklyPivotAssetClassRow {
  asset_class: string;
  valuations: WeeklyPivotAccountValuation[];
}

interface AnnualMddItem {
  data_year: number;
  annual_snapshot_id: number;
  peak_amount: number;
  trough_amount: number;
  mdd_percentage: number;
  weekly_snapshot_count: number;
}

interface WeeklyPivotReportData {
  year: number;
  weeks: WeeklyPivotWeekInfo[];
  account_groups: WeeklyPivotAccountGroupRow[];
  accounts: WeeklyPivotAccountRow[];
  mdd_by_year?: AnnualMddItem[];
  asset_classes?: WeeklyPivotAssetClassRow[];
}

interface Holding {
  holding_id: number;
  account_id: number;
  product_id: number;
  created_at: string;
  deleted_at: string | null;
}

interface HoldingView {
  holding: Holding;
  account: Account | null;
  institution: Institution | null;
  product: Product | null;
}

interface SnapshotHolding {
  snapshot_holding_id: number | null;
  snapshot_id: number | null;
  holding_id: number;
  valuation_amount: string;
  data_source: string;
  created_at: string | null;
}

interface TargetAllocationAccount {
  target_allocation_account_id: number;
  year: number;
  account_id: number;
  target_amount: string;
}

type SnapshotAnalysisWeeklyRange = '6m' | '1y' | '2y' | '5y' | 'all';

interface SnapshotAnalysisWeeklyPoint {
  weekId: number;
  referenceDate: string;
  xLabel: string;
  amount: number;
}

interface Report {
  period_type: string;
  reference_date: string;
  account_name?: string;
  account_group_name?: string;
  asset_class?: string;
  total_value: string;
}

const API_BASE_URL = '/api';

const ACCOUNT_TYPES = [
  '위탁계좌',
  '연금계좌',
  'ISA계좌',
  '예금계좌',
  '금현물계좌',
  'CMA',
  '기타계좌',
];

const ASSET_CLASS_COLORS: Record<string, string> = {
  주식: '#ef4444',
  채권: '#3b82f6',
  통화: '#14b8a6',
  금: '#f59e0b',
  부동산: '#8b5cf6',
  가상자산: '#111827',
  기타자산: '#6b7280',
};

const ASSET_CLASS_ORDER = [
  '주식',
  '채권',
  '통화',
  '금',
  '부동산',
  '가상자산',
  '기타자산',
];

const SNAPSHOT_ANALYSIS_WEEKLY_RANGE_TO_WEEKS: Record<Exclude<SnapshotAnalysisWeeklyRange, 'all'>, number> = {
  '6m': 26,
  '1y': 52,
  '2y': 104,
  '5y': 260,
};

const getAssetClassColor = (assetClass: string | null | undefined): string => {
  if (!assetClass) {
    return ASSET_CLASS_COLORS['기타자산'];
  }
  return ASSET_CLASS_COLORS[assetClass] || ASSET_CLASS_COLORS['기타자산'];
};

const getDataSourceLabel = (dataSource: string): string => {
  const labels: { [key: string]: string } = {
    manual: '수동입력',
    auto: 'API연동',
    missing: '엑셀업로드',
  };
  return labels[dataSource] || dataSource;
};

const formatBeta = (value: number | null | undefined): string => {
  if (value == null || Number.isNaN(value)) {
    return '-';
  }
  return value.toFixed(3);
};

const formatCollectedDate = (value: string | null | undefined): string => {
  if (!value) {
    return '-';
  }
  return new Date(value).toLocaleString();
};

const truncateToFixed = (value: number, digits: number): string => {
  const factor = 10 ** digits;
  const truncated = Math.trunc(value * factor) / factor;
  return truncated.toFixed(digits);
};

const formatToEokLabel = (value: number): string => {
  const numericValue = Number(value);
  if (!Number.isFinite(numericValue)) {
    return '0.00억';
  }
  return `${truncateToFixed(numericValue / 100000000, 2)}억`;
};

export default function PortfolioPage() {
  const [activeTab, setActiveTab] = useState<'users' | 'institutions' | 'products' | 'accounts' | 'accountGroups' | 'snapshots' | 'weeklySnapshots' | 'annualSnapshots' | 'annualSnapshotHoldings' | 'holdings' | 'snapshotHoldings' | 'weeklyReport' | 'annualReport' | 'snapshotAnalysis' | 'targetAllocations'>('institutions');
  
  // User management states
  const [users, setUsers] = useState<User[]>([]);
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    full_name: ''
  });
  const [showUserForm, setShowUserForm] = useState(false);
  const [institutions, setInstitutions] = useState<Institution[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [accountGroups, setAccountGroups] = useState<AccountGroup[]>([]);
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [weeklySnapshots, setWeeklySnapshots] = useState<WeeklySnapshot[]>([]);
  const [annualSnapshots, setAnnualSnapshots] = useState<AnnualSnapshot[]>([]);
  const [annualSnapshotHoldings, setAnnualSnapshotHoldings] = useState<AnnualSnapshotHolding[]>([]);
  const [holdings, setHoldings] = useState<Holding[]>([]);
  const [snapshotHoldings, setSnapshotHoldings] = useState<SnapshotHolding[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [weeklyReportData, setWeeklyReportData] = useState<WeeklyPivotReportData | null>(null);
  const [weeklyReportYear, setWeeklyReportYear] = useState<number>(new Date().getFullYear());
  const [showMonthEndOnly, setShowMonthEndOnly] = useState(false);
  const [annualReportData, setAnnualReportData] = useState<WeeklyPivotReportData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [targetYear, setTargetYear] = useState<number>(new Date().getFullYear());
  const [accountTargetAllocations, setAccountTargetAllocations] = useState<TargetAllocationAccount[]>([]);
  const [todayAccountTargetAllocations, setTodayAccountTargetAllocations] = useState<TargetAllocationAccount[]>([]);
  const [targetAccountDrafts, setTargetAccountDrafts] = useState<Record<number, string>>({});
  const [savingAllTargetAccounts, setSavingAllTargetAccounts] = useState(false);
  const [assetClassTargets, setAssetClassTargets] = useState<Record<string, string>>({});
  const [savingAssetClassTargets, setSavingAssetClassTargets] = useState(false);
  const [snapshotAnalysisAccountGroupFilter, setSnapshotAnalysisAccountGroupFilter] = useState<number | null>(null);
  const [snapshotAnalysisLogScale, setSnapshotAnalysisLogScale] = useState(false);
  const [snapshotAnalysisWeeklyRange, setSnapshotAnalysisWeeklyRange] = useState<SnapshotAnalysisWeeklyRange>('1y');
  const [snapshotAnalysisWeeklyAccountFilter, setSnapshotAnalysisWeeklyAccountFilter] = useState<string>('all');
  const [snapshotAnalysisWeeklyAssetFilter, setSnapshotAnalysisWeeklyAssetFilter] = useState<string>('all');
  const [snapshotAnalysisWeeklySecondSeriesEnabled, setSnapshotAnalysisWeeklySecondSeriesEnabled] = useState(false);
  const [snapshotAnalysisWeeklySecondAccountFilter, setSnapshotAnalysisWeeklySecondAccountFilter] = useState<string>('all');
  const [snapshotAnalysisWeeklySecondAssetFilter, setSnapshotAnalysisWeeklySecondAssetFilter] = useState<string>('all');
  const [snapshotAnalysisWeeklyWindowStart, setSnapshotAnalysisWeeklyWindowStart] = useState(0);
  const [snapshotAnalysisWeeklyWindowEnd, setSnapshotAnalysisWeeklyWindowEnd] = useState(0);

  // Institution Form
  const [newInstitution, setNewInstitution] = useState({
    name: '',
    type: '증권사',
    display_order: '0',
  });
  const [showInstitutionForm, setShowInstitutionForm] = useState(false);
  const [institutionMaxDisplayOrder, setInstitutionMaxDisplayOrder] = useState(0);
  const [editingInstitution, setEditingInstitution] = useState<{
    institution_id: number;
    name: string;
    type: string;
    display_order: string;
  } | null>(null);
  const [showInstitutionEditForm, setShowInstitutionEditForm] = useState(false);

  // Product Form
  const [newProduct, setNewProduct] = useState({
    product_name: '',
    asset_class: '주식',
    region: '대한민국',
    currency: 'KRW',
    investment_type: '직접',
    risk_level: '위험',
    allow_snapshot_input: true,
    ticker: '',
    characteristics: '',
  });
  const [showProductForm, setShowProductForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState<{
    product_id: number;
    product_name: string;
    asset_class: string;
    region: string;
    currency: string;
    investment_type: string;
    risk_level: string;
    allow_snapshot_input: boolean;
    ticker: string;
    characteristics: string;
  } | null>(null);
  const [showProductEditForm, setShowProductEditForm] = useState(false);

  // Account Form
  const [newAccount, setNewAccount] = useState({
    institution_id: '',
    name: '',
    type: '위탁계좌',
    allow_snapshot_input: true,
    display_order: '0',
  });
  const [showAccountForm, setShowAccountForm] = useState(false);
  const [editingAccount, setEditingAccount] = useState<{
    account_id: number;
    institution_id: number;
    name: string;
    type: string;
    allow_snapshot_input: boolean;
    display_order: string;
  } | null>(null);
  const [showAccountEditForm, setShowAccountEditForm] = useState(false);

  // Account Group Form
  const [newAccountGroup, setNewAccountGroup] = useState<{
    name: string;
    account_ids: number[];
    include_in_report: boolean;
  }>({
    name: '',
    account_ids: [],
    include_in_report: false,
  });
  const [showAccountGroupForm, setShowAccountGroupForm] = useState(false);
  const [editingAccountGroup, setEditingAccountGroup] = useState<{
    account_group_id: number;
    name: string;
    account_ids: number[];
    include_in_report: boolean;
  } | null>(null);
  const [showAccountGroupEditForm, setShowAccountGroupEditForm] = useState(false);

  // Snapshot Form
  const [newSnapshot, setNewSnapshot] = useState({
    user_id: 1,
    reference_date: new Date().toISOString().split('T')[0],
  });
  const [showSnapshotForm, setShowSnapshotForm] = useState(false);

  // Holding Form
  const [newHolding, setNewHolding] = useState({
    account_id: '',
    product_id: '',
  });
  const [showHoldingForm, setShowHoldingForm] = useState(false);
  const [holdingsAccountFilter, setHoldingsAccountFilter] = useState<number | null>(null);
  const [holdingsProductFilter, setHoldingsProductFilter] = useState<number | null>(null);
  const [holdingInstitutionFilter, setHoldingInstitutionFilter] = useState('');

  // Snapshot Holding Form
  const [selectedSnapshotId, setSelectedSnapshotId] = useState('');
  const [selectedAnnualSnapshotId, setSelectedAnnualSnapshotId] = useState('');
  const [snapshotHoldingDrafts, setSnapshotHoldingDrafts] = useState<Record<number, string>>({});
  const [snapshotHoldingDataSource, setSnapshotHoldingDataSource] = useState('manual');
  const [savingSnapshotHoldings, setSavingSnapshotHoldings] = useState(false);
  const snapshotHoldingsTableRef = useRef<HTMLTableElement | null>(null);
  const [draggingInstitutionId, setDraggingInstitutionId] = useState<number | null>(null);
  const [draggingAccountId, setDraggingAccountId] = useState<number | null>(null);
  const [draggingAccountGroupId, setDraggingAccountGroupId] = useState<number | null>(null);
  const [draggingProductId, setDraggingProductId] = useState<number | null>(null);
  const [savingInstitutionOrder, setSavingInstitutionOrder] = useState(false);
  const [savingAccountOrder, setSavingAccountOrder] = useState(false);
  const [savingAccountGroupOrder, setSavingAccountGroupOrder] = useState(false);
  const [savingProductOrder, setSavingProductOrder] = useState(false);
  const [showProductBetaView, setShowProductBetaView] = useState(false);
  const [collectingAllProductBeta, setCollectingAllProductBeta] = useState(false);
  const [collectingProductBetaIds, setCollectingProductBetaIds] = useState<number[]>([]);
  const [resolvingProductTickerIds, setResolvingProductTickerIds] = useState<number[]>([]);

  // 주간보고서 스크롤 동기화용 ref
  const weeklyReportTopScrollRef = useRef<HTMLDivElement>(null);
  const weeklyReportBottomScrollRef = useRef<HTMLDivElement>(null);
  const [weeklyReportScrollWidth, setWeeklyReportScrollWidth] = useState(0);

  // 연간보고서 스크롤 동기화용 ref
  const annualReportTopScrollRef = useRef<HTMLDivElement>(null);
  const annualReportBottomScrollRef = useRef<HTMLDivElement>(null);
  const [annualReportScrollWidth, setAnnualReportScrollWidth] = useState(0);

  const snapshotDraftStorageKey = (snapshotId: number) => `snapshot-holdings-draft:${snapshotId}`;
  const buildSnapshotDrafts = (snapshotId: number, useStored: boolean) => {
    let storedDrafts: Record<number, string> = {};
    if (useStored && typeof window !== 'undefined') {
      const raw = window.localStorage.getItem(snapshotDraftStorageKey(snapshotId));
      if (raw) {
        try {
          storedDrafts = JSON.parse(raw);
        } catch {
          storedDrafts = {};
        }
      }
    }

    const draftMap: Record<number, string> = {};
    filterSnapshotInputEligibleHoldings(holdings, products, accounts)
      .forEach((holding) => {
        const existing = snapshotHoldings.find(
          (item) => item.snapshot_id === snapshotId && item.holding_id === holding.holding_id
        );
        const storedValue = storedDrafts[holding.holding_id];
        draftMap[holding.holding_id] = storedValue ?? (existing?.valuation_amount != null
          ? formatSnapshotAmountInput(String(existing.valuation_amount))
          : '');
      });
    return draftMap;
  };

  const getSortedInstitutions = () =>
    [...institutions].sort((a, b) => a.display_order - b.display_order);

  const getSortedAccounts = () =>
    [...accounts].sort((a, b) => {
      const instA = institutions.find((i) => i.institution_id === a.institution_id);
      const instB = institutions.find((i) => i.institution_id === b.institution_id);
      const instOrderA = instA?.display_order ?? 0;
      const instOrderB = instB?.display_order ?? 0;
      if (instOrderA !== instOrderB) {
        return instOrderA - instOrderB;
      }
      if (a.institution_id !== b.institution_id) {
        return a.institution_id - b.institution_id;
      }
      return a.display_order - b.display_order;
    });

  const getSortedProducts = () =>
    [...products].sort((a, b) => {
      const orderA = a.display_order ?? 0;
      const orderB = b.display_order ?? 0;
      if (orderA !== orderB) {
        return orderA - orderB;
      }
      return a.product_id - b.product_id;
    });

  const handleInstitutionDragStart = (institutionId: number) => {
    setDraggingInstitutionId(institutionId);
  };

  const handleInstitutionDrop = (targetId: number) => {
    if (draggingInstitutionId === null || draggingInstitutionId === targetId) {
      return;
    }

    setInstitutions((prev) => {
      const ordered = [...prev].sort((a, b) => a.display_order - b.display_order);
      const fromIndex = ordered.findIndex((item) => item.institution_id === draggingInstitutionId);
      const toIndex = ordered.findIndex((item) => item.institution_id === targetId);
      if (fromIndex < 0 || toIndex < 0) {
        return prev;
      }
      const [moved] = ordered.splice(fromIndex, 1);
      ordered.splice(toIndex, 0, moved);
      return ordered.map((item, index) => ({
        ...item,
        display_order: index + 1,
      }));
    });
    setDraggingInstitutionId(null);
  };

  const handleAccountDragStart = (accountId: number) => {
    setDraggingAccountId(accountId);
  };

  const handleAccountDrop = (targetAccountId: number) => {
    if (draggingAccountId === null || draggingAccountId === targetAccountId) {
      return;
    }

    setAccounts((prev) => {
      const dragging = prev.find((item) => item.account_id === draggingAccountId);
      const target = prev.find((item) => item.account_id === targetAccountId);
      if (!dragging || !target || dragging.institution_id !== target.institution_id) {
        return prev;
      }

      const group = prev
        .filter((item) => item.institution_id === dragging.institution_id)
        .sort((a, b) => a.display_order - b.display_order);
      const fromIndex = group.findIndex((item) => item.account_id === draggingAccountId);
      const toIndex = group.findIndex((item) => item.account_id === targetAccountId);
      if (fromIndex < 0 || toIndex < 0) {
        return prev;
      }
      const [moved] = group.splice(fromIndex, 1);
      group.splice(toIndex, 0, moved);
      const orderMap = new Map(
        group.map((item, index) => [item.account_id, index + 1])
      );
      return prev.map((item) => {
        const updatedOrder = orderMap.get(item.account_id);
        if (updatedOrder == null) {
          return item;
        }
        return { ...item, display_order: updatedOrder };
      });
    });
    setDraggingAccountId(null);
  };

  const handleAccountGroupDragStart = (accountGroupId: number) => {
    setDraggingAccountGroupId(accountGroupId);
  };

  const handleAccountGroupDrop = (targetAccountGroupId: number) => {
    if (draggingAccountGroupId === null || draggingAccountGroupId === targetAccountGroupId) {
      return;
    }

    setAccountGroups((prev) => {
      const ordered = [...prev].sort((a, b) => {
        const diff = (a.display_order ?? 0) - (b.display_order ?? 0);
        if (diff !== 0) {
          return diff;
        }
        return a.account_group_id - b.account_group_id;
      });

      const fromIndex = ordered.findIndex((item) => item.account_group_id === draggingAccountGroupId);
      const toIndex = ordered.findIndex((item) => item.account_group_id === targetAccountGroupId);
      if (fromIndex < 0 || toIndex < 0) {
        return prev;
      }
      const [moved] = ordered.splice(fromIndex, 1);
      ordered.splice(toIndex, 0, moved);
      const orderMap = new Map(
        ordered.map((item, index) => [item.account_group_id, index + 1])
      );
      return prev.map((item) => ({
        ...item,
        display_order: orderMap.get(item.account_group_id) ?? item.display_order,
      }));
    });
    setDraggingAccountGroupId(null);
  };

  const handleProductDragStart = (productId: number) => {
    setDraggingProductId(productId);
  };

  const handleProductDrop = (targetProductId: number) => {
    if (draggingProductId === null || draggingProductId === targetProductId) {
      return;
    }

    setProducts((prev) => {
      const ordered = [...prev].sort((a, b) => {
        const diff = (a.display_order ?? 0) - (b.display_order ?? 0);
        if (diff !== 0) {
          return diff;
        }
        return a.product_id - b.product_id;
      });
      const fromIndex = ordered.findIndex((item) => item.product_id === draggingProductId);
      const toIndex = ordered.findIndex((item) => item.product_id === targetProductId);
      if (fromIndex < 0 || toIndex < 0) {
        return prev;
      }
      const [moved] = ordered.splice(fromIndex, 1);
      ordered.splice(toIndex, 0, moved);

      const orderMap = new Map(
        ordered.map((item, index) => [item.product_id, index + 1])
      );

      return prev.map((item) => {
        const updatedOrder = orderMap.get(item.product_id);
        if (updatedOrder == null) {
          return item;
        }
        return { ...item, display_order: updatedOrder };
      });
    });
    setDraggingProductId(null);
  };

  const normalizeSnapshotAmountInput = (value: string) =>
    value.replace(/[^0-9.-]/g, '').trim();

  const formatSnapshotAmountInput = (value: string) => {
    const trimmed = normalizeSnapshotAmountInput(value);
    if (trimmed === '') {
      return '';
    }
    const parsed = parseFloat(trimmed);
    if (Number.isNaN(parsed)) {
      return value;
    }
    return parsed.toLocaleString();
  };

  const handleSnapshotAmountKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') {
      return;
    }

    const current = event.currentTarget;
    const currentIndex = Number(current.dataset.index);
    if (Number.isNaN(currentIndex)) {
      return;
    }

    const formatted = formatSnapshotAmountInput(current.value);
    if (formatted !== current.value) {
      current.value = formatted;
      const holdingId = Number(current.dataset.holdingId);
      if (!Number.isNaN(holdingId)) {
        setSnapshotHoldingDrafts((prev) => ({
          ...prev,
          [holdingId]: formatted,
        }));
      }
    }

    const nextIndex = event.key === 'ArrowDown' ? currentIndex + 1 : currentIndex - 1;
    const nextInput = snapshotHoldingsTableRef.current?.querySelector(
      `input[data-index="${nextIndex}"]`
    ) as HTMLInputElement | null;

    if (nextInput) {
      event.preventDefault();
      nextInput.focus();
      nextInput.select();
    }
  };

  // Clone Form
  const [cloneForm, setCloneForm] = useState({
    source_snapshot_id: '',
    period_type: 'weekly',
    reference_date: new Date().toISOString().split('T')[0],
  });
  const [showCloneForm, setShowCloneForm] = useState(false);

  // Report Filter
  const [reportFilter, setReportFilter] = useState({
    report_type: 'weekly_account',
    reference_date: new Date().toISOString().split('T')[0],
    account_id: '',
    account_group_id: '',
  });

  const sortedSnapshots = [...snapshots].sort((a, b) => {
    const dateDiff =
      new Date(b.reference_date).getTime() -
      new Date(a.reference_date).getTime();
    if (dateDiff !== 0) {
      return dateDiff;
    }
    return b.snapshot_id - a.snapshot_id;
  });

  const sortedWeeklySnapshots = [...weeklySnapshots].sort((a, b) => {
    const dateDiff =
      new Date(b.reference_date).getTime() -
      new Date(a.reference_date).getTime();
    if (dateDiff !== 0) {
      return dateDiff;
    }
    return b.weekly_snapshot_id - a.weekly_snapshot_id;
  });

  const sortedAnnualSnapshots = [...annualSnapshots].sort((a, b) => {
    const dateDiff =
      new Date(b.reference_date).getTime() -
      new Date(a.reference_date).getTime();
    if (dateDiff !== 0) {
      return dateDiff;
    }
    return b.annual_snapshot_id - a.annual_snapshot_id;
  });

  const sortedAccountGroups = [...accountGroups].sort((a, b) => {
    const diff = (a.display_order ?? 0) - (b.display_order ?? 0);
    if (diff !== 0) {
      return diff;
    }
    return a.account_group_id - b.account_group_id;
  });

  const sortedAccounts = getSortedAccounts();
  const accountReferenceCountByInstitutionId = new Map<number, number>();
  accounts.forEach((account) => {
    accountReferenceCountByInstitutionId.set(
      account.institution_id,
      (accountReferenceCountByInstitutionId.get(account.institution_id) ?? 0) + 1
    );
  });

  const holdingReferenceCountByAccountId = new Map<number, number>();
  const holdingReferenceCountByProductId = new Map<number, number>();
  holdings.forEach((holding) => {
    holdingReferenceCountByAccountId.set(
      holding.account_id,
      (holdingReferenceCountByAccountId.get(holding.account_id) ?? 0) + 1
    );
    holdingReferenceCountByProductId.set(
      holding.product_id,
      (holdingReferenceCountByProductId.get(holding.product_id) ?? 0) + 1
    );
  });

  const snapshotHoldingReferenceCountByHoldingId = new Map<number, number>();
  snapshotHoldings.forEach((snapshotHolding) => {
    snapshotHoldingReferenceCountByHoldingId.set(
      snapshotHolding.holding_id,
      (snapshotHoldingReferenceCountByHoldingId.get(snapshotHolding.holding_id) ?? 0) + 1
    );
  });

  const reportYears = annualReportData
    ? annualReportData.weeks.map((item) => new Date(item.reference_date).getFullYear())
    : [];
  const targetYearOptions = Array.from(
    new Set([targetYear, ...reportYears, new Date().getFullYear() - 1, new Date().getFullYear(), new Date().getFullYear() + 1])
  ).sort((a, b) => a - b);

  // 같은 연도의 여러 스냅샷이 있다면 가장 최신(마지막)을 사용
  const annualReportYearIndex = annualReportData
    ? annualReportData.weeks.reduce((lastIdx, item, idx) => {
        return new Date(item.reference_date).getFullYear() === targetYear ? idx : lastIdx;
      }, -1)
    : -1;

  // 전년도 평가금액을 기준으로 사용
  // 같은 연도의 여러 스냅샷이 있다면 가장 최신(마지막)을 사용
  // targetYear의 스냅샷이 targetYear-1년 확정 데이터를 담고 있음
  const previousYearIndex = annualReportData
    ? annualReportData.weeks.reduce((lastIdx, item, idx) => {
        return new Date(item.reference_date).getFullYear() === targetYear ? idx : lastIdx;
      }, -1)
    : -1;

  const currentYear = new Date().getFullYear();
  const useLatestDailySnapshotForActual = targetYear === currentYear;
  const latestDailySnapshotForTargetYear = useLatestDailySnapshotForActual
    ? sortedSnapshots.find(
        (snapshot) => new Date(snapshot.reference_date).getFullYear() === targetYear
      ) ?? null
    : null;

  // 계좌 -> 계좌그룹 매핑 먼저 생성
  const accountToGroupIds = new Map<number, number[]>();
  sortedAccountGroups.forEach((group) => {
    group.account_ids.forEach((accountId) => {
      const existing = accountToGroupIds.get(accountId) ?? [];
      existing.push(group.account_group_id);
      accountToGroupIds.set(accountId, existing);
    });
  });

  // 계좌별 목표를 계좌그룹별 목표로 집계
  const targetAmountMap = new Map<number, number>();
  accountTargetAllocations.forEach((accountTarget) => {
    const amount = Number(accountTarget.target_amount);
    if (!Number.isNaN(amount)) {
      const groupIds = accountToGroupIds.get(accountTarget.account_id) ?? [];
      groupIds.forEach((groupId) => {
        targetAmountMap.set(groupId, (targetAmountMap.get(groupId) ?? 0) + amount);
      });
    }
  });

  const actualAmountMap = new Map<number, number>();
  if (useLatestDailySnapshotForActual && latestDailySnapshotForTargetYear) {

    const holdingToAccountId = new Map<number, number>();
    holdings
      .filter((holding) => !holding.deleted_at)
      .forEach((holding) => {
        holdingToAccountId.set(holding.holding_id, holding.account_id);
      });

    snapshotHoldings
      .filter(
        (snapshotHolding) =>
          snapshotHolding.snapshot_id === latestDailySnapshotForTargetYear.snapshot_id
      )
      .forEach((snapshotHolding) => {
        const accountId = holdingToAccountId.get(snapshotHolding.holding_id);
        if (accountId == null) {
          return;
        }

        const groupIds = accountToGroupIds.get(accountId) ?? [];
        if (groupIds.length === 0) {
          return;
        }

        const amount = Number(snapshotHolding.valuation_amount);
        if (!Number.isFinite(amount)) {
          return;
        }

        groupIds.forEach((groupId) => {
          actualAmountMap.set(groupId, (actualAmountMap.get(groupId) ?? 0) + amount);
        });
      });
  } else if (annualReportData) {
    // targetYear가 과거 연도일 때는 targetYear + 1 스냅샷(확정된 연도 데이터)에서 가져옴
    const actualYearForSnapshot = targetYear < currentYear ? targetYear + 1 : targetYear;
    const actualYearIndex = annualReportData.weeks.reduce((lastIdx, item, idx) => {
        return new Date(item.reference_date).getFullYear() === actualYearForSnapshot ? idx : lastIdx;
      }, -1);
    
    if (actualYearIndex >= 0) {
        annualReportData.account_groups.forEach((group) => {
          const value = group.valuations[actualYearIndex]?.amount ?? 0;
          actualAmountMap.set(group.account_group_id, value);
        });
    }
  }

  // 전년도 평가금액 맵 생성 (시작일 평가금액)
  const startingAmountMap = new Map<number, number>();
  if (annualReportData && previousYearIndex >= 0) {
    annualReportData.account_groups.forEach((group) => {
      const value = group.valuations[previousYearIndex]?.amount ?? 0;
      startingAmountMap.set(group.account_group_id, value);
    });
  }

  const targetComparisonRows = sortedAccountGroups.map((group) => {
    const targetAmount = targetAmountMap.get(group.account_group_id) ?? 0;
    const actualAmount = actualAmountMap.get(group.account_group_id) ?? 0;
    const startingAmount = startingAmountMap.get(group.account_group_id) ?? 0;
    const gapAmount = actualAmount - targetAmount;
    const achievementRate = targetAmount > 0 ? (actualAmount / targetAmount) * 100 : null;
    const targetGrowthRate = startingAmount > 0 ? ((targetAmount - startingAmount) / startingAmount) * 100 : null;
    return {
      accountGroupId: group.account_group_id,
      accountGroupName: group.name,
      targetAmount,
      actualAmount,
      startingAmount,
      gapAmount,
      achievementRate,
      targetGrowthRate,
    };
  });

  // 전체 합계 계산 및 전체 목표 성장률
  const totalTargetAmount = targetComparisonRows.reduce(
    (sum, row) => sum + row.targetAmount,
    0
  );
  const totalActualAmount = targetComparisonRows.reduce(
    (sum, row) => sum + row.actualAmount,
    0
  );
  const totalStartingAmount = targetComparisonRows.reduce(
    (sum, row) => sum + row.startingAmount,
    0
  );
  const totalGapAmount = totalActualAmount - totalTargetAmount;
  const totalAchievementRate =
    totalTargetAmount > 0 ? (totalActualAmount / totalTargetAmount) * 100 : null;
  const totalTargetGrowthRate = totalStartingAmount > 0 ? ((totalTargetAmount - totalStartingAmount) / totalStartingAmount) * 100 : null;

  const targetComparisonChartData = [
    ...targetComparisonRows
      .filter((row) => row.targetAmount > 0 || row.actualAmount > 0)
      .map((row) => ({
        그룹: row.accountGroupName,
        목표금액: row.targetAmount,
        실제금액: row.actualAmount,
        달성률: row.achievementRate ?? 0,
      })),
    // 전체 합계 추가
    {
      그룹: '전체 합계',
      목표금액: totalTargetAmount,
      실제금액: totalActualAmount,
      달성률: totalAchievementRate ?? 0,
    },
  ];

  const targetDistributionChartData = targetComparisonRows
    .filter((row) => row.targetAmount > 0)
    .map((row) => ({
      name: row.accountGroupName,
      value: row.targetAmount,
    }));

  const accountTargetByAccountId = new Map<number, TargetAllocationAccount>();
  accountTargetAllocations.forEach((item) => {
    accountTargetByAccountId.set(item.account_id, item);
  });

  const accountTargetInputRows = sortedAccounts.map((account) => {
    const institution = institutions.find(
      (item) => item.institution_id === account.institution_id
    );
    return {
      account,
      institutionName: institution?.name ?? '-',
      existingTarget: accountTargetByAccountId.get(account.account_id) ?? null,
      draftAmount: targetAccountDrafts[account.account_id] ?? '',
    };
  });

  const selectedSnapshot = selectedSnapshotId
    ? snapshots.find((snap) => snap.snapshot_id === Number(selectedSnapshotId)) || null
    : null;
  const cloneSourceSnapshot = cloneForm.source_snapshot_id
    ? snapshots.find((snap) => snap.snapshot_id === Number(cloneForm.source_snapshot_id)) || null
    : null;
  const isSelectedSnapshotLocked = selectedSnapshot?.status === 'locked';

  const institutionById = new Map<number, Institution>();
  institutions.forEach((institution) => {
    institutionById.set(institution.institution_id, institution);
  });

  const getSnapshotAnalysisAccountOptionLabel = (account: Account): string => {
    const institutionName = institutionById.get(account.institution_id)?.name;
    if (!institutionName) {
      return account.name;
    }
    return `${institutionName} - ${account.name}`;
  };

  const snapshotAnalysisWeeklyAccountOptions = sortedAccounts;
  const snapshotAnalysisSelectedWeeklyAccountId =
    snapshotAnalysisWeeklyAccountFilter === 'all' ? null : Number(snapshotAnalysisWeeklyAccountFilter);
  const snapshotAnalysisAssetProductIdSet = new Set<number>(
    holdings
      .filter((holding) => {
        if (snapshotAnalysisSelectedWeeklyAccountId == null) {
          return true;
        }
        return holding.account_id === snapshotAnalysisSelectedWeeklyAccountId;
      })
      .map((holding) => holding.product_id)
  );
  const snapshotAnalysisWeeklyAssetOptions = products
    .filter((product) => snapshotAnalysisAssetProductIdSet.has(product.product_id))
    .sort((a, b) => {
      const displayDiff = (a.display_order ?? 0) - (b.display_order ?? 0);
      if (displayDiff !== 0) {
        return displayDiff;
      }
      return a.product_id - b.product_id;
    });
  const snapshotAnalysisSelectedWeeklyAssetId =
    snapshotAnalysisWeeklyAssetFilter === 'all' ? null : Number(snapshotAnalysisWeeklyAssetFilter);
  const snapshotAnalysisSelectedWeeklySecondAccountId =
    snapshotAnalysisWeeklySecondAccountFilter === 'all' ? null : Number(snapshotAnalysisWeeklySecondAccountFilter);
  const snapshotAnalysisSecondAssetProductIdSet = new Set<number>(
    holdings
      .filter((holding) => {
        if (snapshotAnalysisSelectedWeeklySecondAccountId == null) {
          return true;
        }
        return holding.account_id === snapshotAnalysisSelectedWeeklySecondAccountId;
      })
      .map((holding) => holding.product_id)
  );
  const snapshotAnalysisWeeklySecondAssetOptions = products
    .filter((product) => snapshotAnalysisSecondAssetProductIdSet.has(product.product_id))
    .sort((a, b) => {
      const displayDiff = (a.display_order ?? 0) - (b.display_order ?? 0);
      if (displayDiff !== 0) {
        return displayDiff;
      }
      return a.product_id - b.product_id;
    });
  const snapshotAnalysisSelectedWeeklySecondAssetId =
    snapshotAnalysisWeeklySecondAssetFilter === 'all' ? null : Number(snapshotAnalysisWeeklySecondAssetFilter);

  const snapshotAnalysisWeeklySnapshotRows = [...weeklySnapshots].sort((a, b) => {
    const dateDiff = new Date(a.reference_date).getTime() - new Date(b.reference_date).getTime();
    if (dateDiff !== 0) {
      return dateDiff;
    }
    return a.weekly_snapshot_id - b.weekly_snapshot_id;
  });

  const snapshotHoldingsBySnapshotId = new Map<number, SnapshotHolding[]>();
  snapshotHoldings.forEach((snapshotHolding) => {
    if (snapshotHolding.snapshot_id == null) {
      return;
    }
    const existing = snapshotHoldingsBySnapshotId.get(snapshotHolding.snapshot_id) ?? [];
    existing.push(snapshotHolding);
    snapshotHoldingsBySnapshotId.set(snapshotHolding.snapshot_id, existing);
  });

  const holdingById = new Map<number, Holding>();
  holdings.forEach((holding) => {
    holdingById.set(holding.holding_id, holding);
  });

  const buildSnapshotAnalysisWeeklySeriesData = (
    accountId: number | null,
    assetId: number | null
  ): SnapshotAnalysisWeeklyPoint[] =>
    snapshotAnalysisWeeklySnapshotRows.map((weeklySnapshot) => {
      const sourceSnapshotHoldings = snapshotHoldingsBySnapshotId.get(weeklySnapshot.source_snapshot_id) ?? [];
      let totalAmount = 0;

      sourceSnapshotHoldings.forEach((snapshotHolding) => {
        const holding = holdingById.get(snapshotHolding.holding_id);
        if (!holding) {
          return;
        }

        if (accountId != null && holding.account_id !== accountId) {
          return;
        }

        if (assetId != null && holding.product_id !== assetId) {
          return;
        }

        const amount = Number(snapshotHolding.valuation_amount);
        if (!Number.isFinite(amount)) {
          return;
        }

        totalAmount += amount;
      });

      return {
        weekId: weeklySnapshot.weekly_snapshot_id,
        referenceDate: weeklySnapshot.reference_date,
        xLabel: new Date(weeklySnapshot.reference_date).toLocaleDateString('ko-KR', {
          year: '2-digit',
          month: '2-digit',
          day: '2-digit',
        }),
        amount: totalAmount,
      };
    });

  const snapshotAnalysisWeeklySeriesData = buildSnapshotAnalysisWeeklySeriesData(
    snapshotAnalysisSelectedWeeklyAccountId,
    snapshotAnalysisSelectedWeeklyAssetId
  );
  const snapshotAnalysisWeeklySecondSeriesData = buildSnapshotAnalysisWeeklySeriesData(
    snapshotAnalysisSelectedWeeklySecondAccountId,
    snapshotAnalysisSelectedWeeklySecondAssetId
  );

  const snapshotAnalysisWeeklyWindowLength =
    snapshotAnalysisWeeklyRange === 'all'
      ? snapshotAnalysisWeeklySeriesData.length
      : Math.min(
          SNAPSHOT_ANALYSIS_WEEKLY_RANGE_TO_WEEKS[snapshotAnalysisWeeklyRange],
          snapshotAnalysisWeeklySeriesData.length
        );

  const snapshotAnalysisWeeklyVisibleSeriesData =
    snapshotAnalysisWeeklyWindowLength === 0
      ? []
      : snapshotAnalysisWeeklySeriesData.slice(
          snapshotAnalysisWeeklyWindowStart,
          snapshotAnalysisWeeklyWindowEnd + 1
        );
  const snapshotAnalysisWeeklySecondVisibleSeriesData =
    snapshotAnalysisWeeklyWindowLength === 0
      ? []
      : snapshotAnalysisWeeklySecondSeriesData.slice(
          snapshotAnalysisWeeklyWindowStart,
          snapshotAnalysisWeeklyWindowEnd + 1
        );
  const snapshotAnalysisWeeklyChartData = snapshotAnalysisWeeklyVisibleSeriesData.map((point, index) => ({
    ...point,
    amountPrimary: point.amount,
    amountSecondary: snapshotAnalysisWeeklySecondSeriesEnabled
      ? (snapshotAnalysisWeeklySecondVisibleSeriesData[index]?.amount ?? 0)
      : undefined,
  }));

  const snapshotAnalysisPrimaryAccountName =
    snapshotAnalysisSelectedWeeklyAccountId == null
      ? null
      : (() => {
          const selectedAccount = snapshotAnalysisWeeklyAccountOptions.find(
            (account) => account.account_id === snapshotAnalysisSelectedWeeklyAccountId
          );
          return selectedAccount ? getSnapshotAnalysisAccountOptionLabel(selectedAccount) : null;
        })();
  const snapshotAnalysisPrimaryAssetName =
    snapshotAnalysisSelectedWeeklyAssetId == null
      ? null
      : snapshotAnalysisWeeklyAssetOptions.find((product) => product.product_id === snapshotAnalysisSelectedWeeklyAssetId)?.product_name ?? null;
  const snapshotAnalysisSecondaryAccountName =
    snapshotAnalysisSelectedWeeklySecondAccountId == null
      ? null
      : (() => {
          const selectedAccount = snapshotAnalysisWeeklyAccountOptions.find(
            (account) => account.account_id === snapshotAnalysisSelectedWeeklySecondAccountId
          );
          return selectedAccount ? getSnapshotAnalysisAccountOptionLabel(selectedAccount) : null;
        })();
  const snapshotAnalysisSecondaryAssetName =
    snapshotAnalysisSelectedWeeklySecondAssetId == null
      ? null
      : snapshotAnalysisWeeklySecondAssetOptions.find((product) => product.product_id === snapshotAnalysisSelectedWeeklySecondAssetId)?.product_name ?? null;

  const snapshotAnalysisPrimarySeriesLabel =
    snapshotAnalysisSelectedWeeklyAssetId != null
      ? `${snapshotAnalysisPrimaryAssetName ?? '선택 자산'} 평가금액`
      : snapshotAnalysisSelectedWeeklyAccountId != null
        ? `${snapshotAnalysisPrimaryAccountName ?? '선택 계좌'} 합계 평가금액`
        : '전체 합계 평가금액';
  const snapshotAnalysisSecondarySeriesLabel =
    snapshotAnalysisSelectedWeeklySecondAssetId != null
      ? `비교: ${snapshotAnalysisSecondaryAssetName ?? '선택 자산'} 평가금액`
      : snapshotAnalysisSelectedWeeklySecondAccountId != null
        ? `비교: ${snapshotAnalysisSecondaryAccountName ?? '선택 계좌'} 합계 평가금액`
        : '비교: 전체 합계 평가금액';

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUsers();
    } else if (activeTab === 'institutions') {
      fetchInstitutions();
      fetchAccounts();
    } else if (activeTab === 'products') {
      fetchProducts();
      fetchInstitutions();
      fetchHoldings();
    } else if (activeTab === 'accounts') {
      fetchAccounts();
      fetchInstitutions(); // For dropdown
      fetchHoldings();
    } else if (activeTab === 'accountGroups') {
      fetchAccountGroups();
      fetchAccounts();
      fetchInstitutions();
    } else if (activeTab === 'snapshots') {
      fetchSnapshots();
    } else if (activeTab === 'weeklySnapshots') {
      fetchWeeklySnapshots();
    } else if (activeTab === 'annualSnapshots') {
      fetchAnnualSnapshots();
    } else if (activeTab === 'annualSnapshotHoldings') {
      fetchAnnualSnapshots();
      fetchAnnualSnapshotHoldings();
    } else if (activeTab === 'holdings') {
      fetchHoldings();
      fetchSnapshotHoldings();
      fetchAccounts(); // For dropdown
      fetchProducts(); // For dropdown
      fetchInstitutions(); // For institution labels
    } else if (activeTab === 'snapshotHoldings') {
      fetchSnapshotHoldings();
      fetchSnapshots(); // For dropdown
      fetchHoldings(); // For list
      fetchAccounts();
      fetchProducts();
      fetchInstitutions();
    } else if (activeTab === 'weeklyReport') {
      fetchWeeklyReport();
    } else if (activeTab === 'annualReport') {
      fetchAnnualReport();
    } else if (activeTab === 'snapshotAnalysis') {
      fetchSnapshots();
      fetchWeeklySnapshots();
      fetchSnapshotHoldings();
      fetchAnnualSnapshots();
      fetchAccountGroups();
      fetchInstitutions();
      fetchAccounts();
      fetchHoldings();
      fetchProducts();
      fetchCurrentYearAccountTargetAllocations();
    } else if (activeTab === 'targetAllocations') {
      fetchAccountGroups();
      fetchAccounts();
      fetchProducts();
      fetchAnnualReport();
      fetchSnapshots();
      fetchHoldings();
      fetchSnapshotHoldings();
      fetchAccountTargetAllocations(targetYear);
    }
  }, [activeTab]);

  useEffect(() => {
    if (activeTab === 'targetAllocations') {
      fetchAccountTargetAllocations(targetYear);
      if (targetYear === new Date().getFullYear()) {
        fetchSnapshots();
        fetchHoldings();
        fetchSnapshotHoldings();
      }
    }
  }, [activeTab, targetYear]);

  // snapshotAnalysis 탭에서 annualSnapshots 로드 후 holdings 요청
  useEffect(() => {
    if (activeTab === 'snapshotAnalysis' && annualSnapshots.length > 0) {
      fetchAllAnnualSnapshotHoldings(annualSnapshots);
    }
  }, [activeTab, annualSnapshots]);

  useEffect(() => {
    if (snapshotAnalysisWeeklyAssetFilter === 'all') {
      return;
    }

    const isValidAsset = snapshotAnalysisWeeklyAssetOptions.some(
      (option) => String(option.product_id) === snapshotAnalysisWeeklyAssetFilter
    );
    if (!isValidAsset) {
      setSnapshotAnalysisWeeklyAssetFilter('all');
    }
  }, [snapshotAnalysisWeeklyAssetFilter, snapshotAnalysisWeeklyAssetOptions]);

  useEffect(() => {
    if (snapshotAnalysisWeeklySecondAssetFilter === 'all') {
      return;
    }

    const isValidAsset = snapshotAnalysisWeeklySecondAssetOptions.some(
      (option) => String(option.product_id) === snapshotAnalysisWeeklySecondAssetFilter
    );
    if (!isValidAsset) {
      setSnapshotAnalysisWeeklySecondAssetFilter('all');
    }
  }, [snapshotAnalysisWeeklySecondAssetFilter, snapshotAnalysisWeeklySecondAssetOptions]);

  useEffect(() => {
    const dataLength = snapshotAnalysisWeeklySeriesData.length;
    if (dataLength === 0 || snapshotAnalysisWeeklyWindowLength === 0) {
      setSnapshotAnalysisWeeklyWindowStart(0);
      setSnapshotAnalysisWeeklyWindowEnd(0);
      return;
    }

    const maxStart = Math.max(0, dataLength - snapshotAnalysisWeeklyWindowLength);
    const nextEnd = dataLength - 1;
    const nextStart = Math.max(0, nextEnd - snapshotAnalysisWeeklyWindowLength + 1);
    setSnapshotAnalysisWeeklyWindowStart(Math.min(Math.max(0, nextStart), maxStart));
    setSnapshotAnalysisWeeklyWindowEnd(nextEnd);
  }, [snapshotAnalysisWeeklyRange, snapshotAnalysisWeeklyWindowLength, snapshotAnalysisWeeklySeriesData.length]);

  useEffect(() => {
    if (!selectedSnapshotId) {
      setSnapshotHoldingDrafts({});
      return;
    }

    const snapshotId = parseInt(selectedSnapshotId, 10);
    setSnapshotHoldingDrafts(buildSnapshotDrafts(snapshotId, true));
  }, [selectedSnapshotId, holdings, products, accounts, snapshotHoldings]);

  useEffect(() => {
    if (!selectedSnapshotId || typeof window === 'undefined') {
      return;
    }
    const snapshotId = parseInt(selectedSnapshotId, 10);
    window.localStorage.setItem(
      snapshotDraftStorageKey(snapshotId),
      JSON.stringify(snapshotHoldingDrafts)
    );
  }, [selectedSnapshotId, snapshotHoldingDrafts]);

  // User management functions
  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/users`);
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      const result = await response.json();
      const usersList = result.data?.items || [];
      setUsers(usersList);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newUser),
      });

      if (!response.ok) {
        throw new Error('Failed to create user');
      }

      setNewUser({ username: '', email: '', full_name: '' });
      setShowUserForm(false);
      fetchUsers();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create user');
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete user');
      }

      fetchUsers();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete user');
    }
  };

  const fetchInstitutions = async () => {
    try {
      setLoading(true);
      // 기본 기관 정보 조회
      const response = await fetch(`${API_BASE_URL}/portfolio/institutions`);
      if (!response.ok) throw new Error('Failed to fetch institutions');
      const result = await response.json();
      const items = Array.isArray(result) ? result : result.data?.items || [];
      
      // 금융기관별 자산총합 조회
      let assetsMap: Record<number, number> = {};
      try {
        const assetsResponse = await fetch(`${API_BASE_URL}/portfolio/institutions/assets`);
        if (assetsResponse.ok) {
          const assetsResult = await assetsResponse.json();
          const assetsItems = Array.isArray(assetsResult) ? assetsResult : assetsResult.data?.items || [];
          assetsMap = Object.fromEntries(
            assetsItems.map((item: any) => [item.institution_id, item.total_assets || 0])
          );
        }
      } catch (err) {
        console.warn('Failed to fetch institution assets:', err);
        // 자산 조회 실패 시에도 기본 정보는 표시
      }
      
      // 자산정보와 merge
      const itemsWithAssets = items.map((item: Institution) => ({
        ...item,
        total_assets: assetsMap[item.institution_id] || 0,
      }));
      
      const maxDisplayOrder = Array.isArray(result)
        ? Math.max(0, ...items.map((item: Institution) => item.display_order ?? 0))
        : result.data?.max_display_order ?? Math.max(0, ...items.map((item: Institution) => item.display_order ?? 0));
      setInstitutions(itemsWithAssets);
      setInstitutionMaxDisplayOrder(maxDisplayOrder);
      setNewInstitution((prev) => ({
        ...prev,
        display_order: prev.display_order !== '0' ? prev.display_order : String(maxDisplayOrder + 1),
      }));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching institutions');
    } finally {
      setLoading(false);
    }
  };

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/products`);
      if (!response.ok) throw new Error('Failed to fetch products');
      const result = await response.json();
      setProducts(Array.isArray(result) ? result : result.data?.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching products');
    } finally {
      setLoading(false);
    }
  };

  const fetchAccounts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/accounts`);
      if (!response.ok) throw new Error('Failed to fetch accounts');
      const result = await response.json();
      setAccounts(Array.isArray(result) ? result : result.data?.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching accounts');
    } finally {
      setLoading(false);
    }
  };

  const fetchAccountGroups = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/account-groups`);
      if (!response.ok) throw new Error('Failed to fetch account groups');
      const result = await response.json();
      setAccountGroups(Array.isArray(result) ? result : result.data?.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching account groups');
    } finally {
      setLoading(false);
    }
  };

  const fetchSnapshots = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/snapshots?user_id=1`);
      if (!response.ok) throw new Error('Failed to fetch snapshots');
      const result = await response.json();
      setSnapshots(Array.isArray(result) ? result : result.data?.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching snapshots');
    } finally {
      setLoading(false);
    }
  };

  const fetchWeeklySnapshots = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/weekly-snapshots?user_id=1`);
      if (!response.ok) throw new Error('Failed to fetch weekly snapshots');
      const result = await response.json();
      setWeeklySnapshots(Array.isArray(result) ? result : result.data?.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching weekly snapshots');
    } finally {
      setLoading(false);
    }
  };

  const fetchAnnualSnapshots = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/annual-snapshots?user_id=1`);
      if (!response.ok) throw new Error('Failed to fetch annual snapshots');
      const result = await response.json();
      setAnnualSnapshots(Array.isArray(result) ? result : result.data?.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching annual snapshots');
    } finally {
      setLoading(false);
    }
  };

  const fetchAnnualSnapshotHoldings = async (annualSnapshotId?: number) => {
    const targetId = annualSnapshotId ?? (selectedAnnualSnapshotId ? parseInt(selectedAnnualSnapshotId, 10) : null);
    if (!targetId || Number.isNaN(targetId)) {
      setAnnualSnapshotHoldings([]);
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(
        `${API_BASE_URL}/portfolio/annual-snapshot-holdings?annual_snapshot_id=${targetId}`
      );
      if (!response.ok) throw new Error('Failed to fetch annual snapshot holdings');
      const result = await response.json();
      setAnnualSnapshotHoldings(Array.isArray(result) ? result : result.data?.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching annual snapshot holdings');
      setAnnualSnapshotHoldings([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchAllAnnualSnapshotHoldings = async (snaps: AnnualSnapshot[]) => {
    if (snaps.length === 0) {
      setAnnualSnapshotHoldings([]);
      return;
    }

    try {
      setLoading(true);
      let allHoldings: AnnualSnapshotHolding[] = [];
      
      for (const snap of snaps) {
        const response = await fetch(
          `${API_BASE_URL}/portfolio/annual-snapshot-holdings?annual_snapshot_id=${snap.annual_snapshot_id}`
        );
        if (response.ok) {
          const result = await response.json();
          const holdings = Array.isArray(result) ? result : result.data?.items || [];
          allHoldings = [...allHoldings, ...holdings];
        }
      }
      
      setAnnualSnapshotHoldings(allHoldings);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching annual snapshot holdings');
      setAnnualSnapshotHoldings([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchHoldings = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/holdings`);
      if (!response.ok) throw new Error('Failed to fetch holdings');
      const result = await response.json();
      setHoldings(Array.isArray(result) ? result : result.data?.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching holdings');
    } finally {
      setLoading(false);
    }
  };

  const fetchSnapshotHoldings = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/snapshot-holdings`);
      if (!response.ok) throw new Error('Failed to fetch snapshot holdings');
      const result = await response.json();
      setSnapshotHoldings(Array.isArray(result) ? result : result.data?.items || []);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching snapshot holdings');
    } finally {
      setLoading(false);
    }
  };

  const fetchWeeklyReport = async () => {
    try {
      setLoading(true);
      const response = await fetch(
        `${API_BASE_URL}/portfolio/reports/weekly/pivot?user_id=1&year=${weeklyReportYear}`
      );
      if (!response.ok) throw new Error('Failed to fetch weekly report');
      const result = await response.json();
      if (result.code === 0 && result.data) {
        setWeeklyReportData(result.data);
      } else {
        setWeeklyReportData(null);
      }
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching weekly report');
      setWeeklyReportData(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchAnnualReport = async () => {
    try {
      setLoading(true);
      const response = await fetch(
        `${API_BASE_URL}/portfolio/reports/annual/pivot?user_id=1`
      );
      if (!response.ok) throw new Error('Failed to fetch annual report');
      const result = await response.json();
      if (result.code === 0 && result.data) {
        const annualData: WeeklyPivotReportData = result.data;
        const thisYear = new Date().getFullYear();
        // 연간 스냅샷의 reference_date는 다음 해 1월(e.g. 2025년 데이터 → 2026-01-xx)
        // 이번 연도 연간보고서가 있으면 reference_date 연도가 thisYear+1이어야 함
        const hasCurrentYear = annualData.weeks.some(
          (w) => new Date(w.reference_date).getFullYear() === thisYear + 1
        );

        if (!hasCurrentYear) {
          // 이번 연도 주간보고서에서 마지막 항목을 가져와 연간보고서에 추가
          try {
            const weeklyResponse = await fetch(
              `${API_BASE_URL}/portfolio/reports/weekly/pivot?user_id=1&year=${thisYear}`
            );
            if (weeklyResponse.ok) {
              const weeklyResult = await weeklyResponse.json();
              if (weeklyResult.code === 0 && weeklyResult.data) {
                const weeklyData: WeeklyPivotReportData = weeklyResult.data;
                if (weeklyData.weeks.length > 0) {
                  const lastWeekIdx = weeklyData.weeks.length - 1;
                  // week_number: 999 → 현재 연도 합성 항목임을 표시 (헤더 렌더링에서 구분)
                  const lastWeek = { ...weeklyData.weeks[lastWeekIdx], week_number: 999 };

                  // weeks 배열에 마지막 주간 항목 추가
                  const mergedWeeks = [...annualData.weeks, lastWeek];

                  // account_groups 병합: 연간 그룹에 마지막 주간 valuation 추가
                  const weeklyGroupMap = new Map(
                    weeklyData.account_groups.map((g) => [g.account_group_id, g])
                  );
                  const mergedGroups = annualData.account_groups.map((g) => {
                    const weeklyGroup = weeklyGroupMap.get(g.account_group_id);
                    const lastValuation = weeklyGroup
                      ? weeklyGroup.valuations[lastWeekIdx] ?? { weekly_snapshot_id: lastWeek.weekly_snapshot_id, amount: 0 }
                      : { weekly_snapshot_id: lastWeek.weekly_snapshot_id, amount: 0 };
                    return { ...g, valuations: [...g.valuations, lastValuation] };
                  });
                  // 연간보고서에 없는 계좌그룹이 주간에 있으면 추가
                  weeklyData.account_groups.forEach((wg) => {
                    if (!mergedGroups.find((g) => g.account_group_id === wg.account_group_id)) {
                      const zeroValuations = annualData.weeks.map((w) => ({
                        weekly_snapshot_id: w.weekly_snapshot_id,
                        amount: 0,
                      }));
                      const lastValuation = wg.valuations[lastWeekIdx] ?? {
                        weekly_snapshot_id: lastWeek.weekly_snapshot_id,
                        amount: 0,
                      };
                      mergedGroups.push({ ...wg, valuations: [...zeroValuations, lastValuation] });
                    }
                  });

                  // accounts 병합: 연간 계좌에 마지막 주간 valuation 추가
                  const weeklyAccountMap = new Map(
                    weeklyData.accounts.map((a) => [a.account_id, a])
                  );
                  const mergedAccounts = annualData.accounts.map((a) => {
                    const weeklyAccount = weeklyAccountMap.get(a.account_id);
                    const lastValuation = weeklyAccount
                      ? weeklyAccount.valuations[lastWeekIdx] ?? { weekly_snapshot_id: lastWeek.weekly_snapshot_id, amount: 0 }
                      : { weekly_snapshot_id: lastWeek.weekly_snapshot_id, amount: 0 };
                    return { ...a, valuations: [...a.valuations, lastValuation] };
                  });
                  weeklyData.accounts.forEach((wa) => {
                    if (!mergedAccounts.find((a) => a.account_id === wa.account_id)) {
                      const zeroValuations = annualData.weeks.map((w) => ({
                        weekly_snapshot_id: w.weekly_snapshot_id,
                        amount: 0,
                      }));
                      const lastValuation = wa.valuations[lastWeekIdx] ?? {
                        weekly_snapshot_id: lastWeek.weekly_snapshot_id,
                        amount: 0,
                      };
                      mergedAccounts.push({ ...wa, valuations: [...zeroValuations, lastValuation] });
                    }
                  });

                  // asset_classes 병합: 연간 자산유형에 마지막 주간 valuation 추가
                  const weeklyAssetClassMap = new Map(
                    (weeklyData.asset_classes || []).map((row) => [row.asset_class, row])
                  );
                  const mergedAssetClasses = (annualData.asset_classes || ASSET_CLASS_ORDER.map((assetClass) => ({
                    asset_class: assetClass,
                    valuations: annualData.weeks.map((w) => ({
                      weekly_snapshot_id: w.weekly_snapshot_id,
                      amount: 0,
                    })),
                  }))).map((row) => {
                    const weeklyRow = weeklyAssetClassMap.get(row.asset_class);
                    const lastValuation = weeklyRow
                      ? weeklyRow.valuations[lastWeekIdx] ?? { weekly_snapshot_id: lastWeek.weekly_snapshot_id, amount: 0 }
                      : { weekly_snapshot_id: lastWeek.weekly_snapshot_id, amount: 0 };
                    return {
                      ...row,
                      valuations: [...row.valuations, lastValuation],
                    };
                  });

                  setAnnualReportData({
                    ...annualData,
                    weeks: mergedWeeks,
                    account_groups: mergedGroups,
                    accounts: mergedAccounts,
                    asset_classes: mergedAssetClasses,
                  });
                } else {
                  setAnnualReportData(annualData);
                }
              } else {
                setAnnualReportData(annualData);
              }
            } else {
              setAnnualReportData(annualData);
            }
          } catch {
            // 주간보고서 fetch 실패 시 연간보고서 데이터만 사용
            setAnnualReportData(annualData);
          }
        } else {
          setAnnualReportData(annualData);
        }
      } else {
        setAnnualReportData(null);
      }
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching annual report');
      setAnnualReportData(null);
    } finally {
      setLoading(false);
    }
  };

  const normalizeTargetAmountInput = (value: string) =>
    value.replace(/[^0-9.-]/g, '').trim();

  const formatTargetAmountInput = (value: string) => {
    const normalized = normalizeTargetAmountInput(value);
    if (normalized === '') {
      return '';
    }
    const parsed = Number(normalized);
    if (!Number.isFinite(parsed)) {
      return value;
    }
    return parsed.toLocaleString('ko-KR', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    });
  };

  const fetchAccountTargetAllocations = async (year: number) => {
    try {
      setLoading(true);
      const response = await fetch(
        `${API_BASE_URL}/portfolio/target-allocations/account?year=${year}`
      );
      if (!response.ok) {
        throw new Error('Failed to fetch account target allocations');
      }
      const result = await response.json();
      const accountTargets: TargetAllocationAccount[] = result.account_targets ?? [];
      setAccountTargetAllocations(accountTargets);

      const draftMap: Record<number, string> = {};
      accountTargets.forEach((target) => {
        const amount = Number(target.target_amount);
        draftMap[target.account_id] = Number.isFinite(amount)
          ? amount.toLocaleString('ko-KR', {
              minimumFractionDigits: 0,
              maximumFractionDigits: 0,
            })
          : '';
      });
      setTargetAccountDrafts(draftMap);
      setError(null);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Error fetching account target allocations'
      );
      setAccountTargetAllocations([]);
      setTargetAccountDrafts({});
    } finally {
      setLoading(false);
    }
  };

  const fetchCurrentYearAccountTargetAllocations = async () => {
    try {
      const year = new Date().getFullYear();
      const response = await fetch(
        `${API_BASE_URL}/portfolio/target-allocations/account?year=${year}`
      );
      if (!response.ok) {
        throw new Error('Failed to fetch current year account target allocations');
      }
      const result = await response.json();
      const accountTargets: TargetAllocationAccount[] = result.account_targets ?? [];
      setTodayAccountTargetAllocations(accountTargets);
    } catch {
      setTodayAccountTargetAllocations([]);
    }
  };

  const handleSaveAllAccountTargetAllocations = async () => {
    // 모든 draft에서 유효한 값들만 필터링
    const toSave: Array<{ accountId: number; amount: number }> = [];
    const errors: string[] = [];

    Object.entries(targetAccountDrafts).forEach(([key, rawAmount]) => {
      const accountId = Number(key);
      if (!rawAmount || rawAmount.trim() === '') {
        return; // 빈 값은 무시
      }

      const normalizedAmount = normalizeTargetAmountInput(rawAmount);
      const amount = Number(normalizedAmount);

      if (!Number.isFinite(amount) || amount < 0) {
        const account = sortedAccounts.find((a) => a.account_id === accountId);
        errors.push(`${account?.name || `계좌 ${accountId}`}: 유효한 숫자를 입력해주세요.`);
        return;
      }

      toSave.push({ accountId, amount });
    });

    if (errors.length > 0) {
      alert(`입력 오류:\n${errors.join('\n')}`);
      return;
    }

    if (toSave.length === 0) {
      alert('저장할 목표금액이 없습니다.');
      return;
    }

    try {
      setSavingAllTargetAccounts(true);

      // 모든 저장을 병렬로 실행
      const savePromises = toSave.map((item) =>
        fetch(`${API_BASE_URL}/portfolio/target-allocations/account`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            year: targetYear,
            account_id: item.accountId,
            target_amount: item.amount,
          }),
        })
      );

      const responses = await Promise.all(savePromises);

      // 모든 응답 확인
      for (const response of responses) {
        if (!response.ok) {
          const result = await response.json();
          throw new Error(result.message || 'Failed to save account target allocation');
        }
      }

      // 성공 후 데이터 다시 로드 및 UI 업데이트
      await fetchAccountTargetAllocations(targetYear);
      await fetchAnnualReport();
      alert(`${toSave.length}개 계좌의 목표금액을 저장했습니다.`);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to save target allocations');
    } finally {
      setSavingAllTargetAccounts(false);
    }
  };

  // 연도 변경 시 주간 보고서 다시 로드
  useEffect(() => {
    if (activeTab === 'weeklyReport') {
      fetchWeeklyReport();
    }
  }, [weeklyReportYear]);

  // 주간/연간 보고서 테이블 렌더링 후 scrollWidth 측정
  useEffect(() => {
    if (weeklyReportBottomScrollRef.current && weeklyReportData) {
      const scrollWidth = weeklyReportBottomScrollRef.current.scrollWidth;
      setWeeklyReportScrollWidth(scrollWidth);
    }
  }, [weeklyReportData, showMonthEndOnly]);

  useEffect(() => {
    if (annualReportBottomScrollRef.current && annualReportData) {
      const scrollWidth = annualReportBottomScrollRef.current.scrollWidth;
      setAnnualReportScrollWidth(scrollWidth);
    }
  }, [annualReportData]);

  // Load asset class targets from API
  useEffect(() => {
    if (activeTab === 'targetAllocations') {
      fetchAssetClassTargets(targetYear);
    } else if (activeTab === 'snapshotAnalysis') {
      // 스냅샷 분석 탭일 때, 가장 최근 스냅샷의 연도 기준 목표 데이터 가져오기
      const latestSnapshot = snapshots
        .sort((a, b) => new Date(b.reference_date).getTime() - new Date(a.reference_date).getTime())[0];
      if (latestSnapshot) {
        const year = new Date(latestSnapshot.reference_date).getFullYear();
        fetchAssetClassTargets(year);
      }
    }
  }, [targetYear, activeTab, snapshots]);

  const fetchAssetClassTargets = async (year: number) => {
    try {
      const response = await fetch(`/api/portfolio/target-allocations/asset-classes/year/${year}`);
      const result = await response.json();
      if (result.code === 0 && result.data?.targets) {
        const targetsMap: Record<string, string> = {};
        result.data.targets.forEach((t: any) => {
          targetsMap[t.asset_class] = String(t.target_percentage);
        });
        setAssetClassTargets(targetsMap);
      } else {
        setAssetClassTargets({});
      }
    } catch (err) {
      console.error('Failed to fetch asset class targets:', err);
      setAssetClassTargets({});
    }
  };

  const handleSaveAssetClassTargets = async () => {
    try {
      setSavingAssetClassTargets(true);
      const payload = Object.entries(assetClassTargets)
        .filter(([_, value]) => value && parseFloat(value) > 0)
        .map(([asset_class, target_percentage]) => ({
          year: targetYear,
          asset_class,
          target_percentage: parseFloat(target_percentage),
        }));

      const response = await fetch('/api/portfolio/target-allocations/asset-classes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const result = await response.json();
      if (result.code === 0) {
        await fetchAssetClassTargets(targetYear);
        alert(`${targetYear}년도 자산별 목표 %를 저장했습니다.`);
      } else {
        alert(result.message || '저장에 실패했습니다');
      }
    } catch (err) {
      alert(err instanceof Error ? err.message : '저장에 실패했습니다');
    } finally {
      setSavingAssetClassTargets(false);
    }
  };

  const openInstitutionEdit = (institution: Institution) => {
    setEditingInstitution({
      institution_id: institution.institution_id,
      name: institution.name,
      type: institution.type,
      display_order: String(institution.display_order ?? 0),
    });
    setShowInstitutionEditForm(true);
    setShowInstitutionForm(false);
  };

  const cancelInstitutionEdit = () => {
    setEditingInstitution(null);
    setShowInstitutionEditForm(false);
  };

  const handleUpdateInstitution = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingInstitution) {
      return;
    }
    try {
      const payload = {
        name: editingInstitution.name,
        type: editingInstitution.type,
        display_order: parseInt(editingInstitution.display_order, 10) || 0,
      };
      const response = await fetch(
        `${API_BASE_URL}/portfolio/institutions/${editingInstitution.institution_id}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        }
      );
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to update institution');
      setEditingInstitution(null);
      setShowInstitutionEditForm(false);
      fetchInstitutions();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update institution');
    }
  };

  const handleCreateInstitution = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        ...newInstitution,
        display_order: parseInt(newInstitution.display_order, 10) || 0,
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/institutions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to create institution');
      setNewInstitution({
        name: '',
        type: '증권사',
        display_order: String(institutionMaxDisplayOrder + 1),
      });
      setShowInstitutionForm(false);
      fetchInstitutions();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create institution');
    }
  };

  const handleSaveInstitutionOrder = async () => {
    const ordered = getSortedInstitutions().map((item, index) => ({
      ...item,
      display_order: index + 1,
    }));

    try {
      setSavingInstitutionOrder(true);
      const payload = {
        items: ordered.map((item) => ({
          institution_id: item.institution_id,
          display_order: item.display_order,
        })),
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/institutions:reorder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to update display order');
      setInstitutions(ordered);
      alert('기관 표시순서가 저장되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update display order');
    } finally {
      setSavingInstitutionOrder(false);
    }
  };

  const handleDeleteInstitution = async (institutionId: number) => {
    if (!window.confirm('금융기관을 삭제하시겠습니까?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/portfolio/institutions/${institutionId}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to delete institution');
      }

      if (editingInstitution?.institution_id === institutionId) {
        cancelInstitutionEdit();
      }
      await fetchInstitutions();
      await fetchAccounts();
      alert('금융기관이 삭제되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete institution');
    }
  };

  const handleSaveProductOrder = async () => {
    const ordered = getSortedProducts().map((item, index) => ({
      ...item,
      display_order: index + 1,
    }));
    const displayOrderMap = new Map<number, number>();
    ordered.forEach((item) => {
      displayOrderMap.set(item.product_id, item.display_order);
    });

    try {
      setSavingProductOrder(true);
      const payload = {
        items: ordered.map((item) => ({
          product_id: item.product_id,
          display_order: item.display_order,
        })),
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/products:reorder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to update display order');
      setProducts((prev) =>
        prev.map((item) => {
          const newOrder = displayOrderMap.get(item.product_id);
          return newOrder == null ? item : { ...item, display_order: newOrder };
        })
      );
      alert('상품 표시순서가 저장되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update display order');
    } finally {
      setSavingProductOrder(false);
    }
  };

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const nextOrder = Math.max(0, ...products.map((item) => item.display_order ?? 0)) + 1;
      const payload = {
        ...newProduct,
        ticker: newProduct.ticker ? newProduct.ticker.trim().toUpperCase() : null,
        characteristics: newProduct.characteristics
          ? newProduct.characteristics.split(',').map((s) => s.trim())
          : undefined,
        display_order: nextOrder,
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to create product');
      setNewProduct({
        product_name: '',
        asset_class: '주식',
        region: '대한민국',
        currency: 'KRW',
        investment_type: '직접',
        risk_level: '위험',
        allow_snapshot_input: true,
        ticker: '',
        characteristics: '',
      });
      setShowProductForm(false);
      setShowProductEditForm(false);
      setEditingProduct(null);
      fetchProducts();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create product');
    }
  };

  const handleDeleteProduct = async (productId: number) => {
    if (!window.confirm('상품을 삭제하시겠습니까?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/portfolio/products/${productId}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to delete product');
      }

      if (editingProduct?.product_id === productId) {
        cancelProductEdit();
      }
      await fetchProducts();
      await fetchHoldings();
      alert('상품이 삭제되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete product');
    }
  };

  const openProductEdit = (product: Product) => {
    setEditingProduct({
      product_id: product.product_id,
      product_name: product.product_name,
      asset_class: product.asset_class,
      region: product.region,
      currency: product.currency,
      investment_type: product.investment_type,
      risk_level: product.risk_level,
      allow_snapshot_input: product.allow_snapshot_input,
      ticker: product.ticker ?? '',
      characteristics: product.characteristics?.join(', ') || '',
    });
    setShowProductEditForm(true);
    setShowProductForm(false);
  };

  const cancelProductEdit = () => {
    setEditingProduct(null);
    setShowProductEditForm(false);
  };

  const handleUpdateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingProduct) return;
    try {
      const payload = {
        product_name: editingProduct.product_name,
        asset_class: editingProduct.asset_class,
        region: editingProduct.region,
        currency: editingProduct.currency,
        investment_type: editingProduct.investment_type,
        risk_level: editingProduct.risk_level,
        allow_snapshot_input: editingProduct.allow_snapshot_input,
        ticker: editingProduct.ticker ? editingProduct.ticker.trim().toUpperCase() : null,
        characteristics: editingProduct.characteristics
          ? editingProduct.characteristics.split(',').map((s) => s.trim())
          : undefined,
      };
      const response = await fetch(
        `${API_BASE_URL}/portfolio/products/${editingProduct.product_id}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        }
      );
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to update product');
      cancelProductEdit();
      setShowProductForm(false);
      fetchProducts();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update product');
    }
  };

  const handleCollectProductBeta = async (productId: number) => {
    try {
      setCollectingProductBetaIds((prev) => [...prev, productId]);
      const response = await fetch(`${API_BASE_URL}/portfolio/products/${productId}/beta:collect`, {
        method: 'POST',
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to collect product beta');
      }
      await fetchProducts();
      const item = data?.data?.items?.[0];
      if (item?.updated) {
        alert('상품 베타를 실측 수집했습니다.');
      } else {
        alert(`실측 수집 실패: ${item?.message ?? 'unknown_error'}`);
      }
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to collect product beta');
    } finally {
      setCollectingProductBetaIds((prev) => prev.filter((id) => id !== productId));
    }
  };

  const handleCollectAllProductBetas = async () => {
    try {
      setCollectingAllProductBeta(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/products/beta:collect`, {
        method: 'POST',
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to collect all product betas');
      }
      await fetchProducts();
      const updatedCount = data?.data?.updated_count ?? 0;
      const items = data?.data?.items ?? [];
      const failedCount = items.filter((item: { updated?: boolean }) => !item.updated).length;
      alert(`전체 베타 수집 완료: 실측 성공 ${updatedCount}건, 실패 ${failedCount}건`);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to collect all product betas');
    } finally {
      setCollectingAllProductBeta(false);
    }
  };

  const handleResolveProductTicker = async (productId: number) => {
    try {
      setResolvingProductTickerIds((prev) => [...prev, productId]);
      const response = await fetch(`${API_BASE_URL}/portfolio/products/${productId}/ticker:resolve`, {
        method: 'POST',
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to resolve product ticker');
      }
      await fetchProducts();
      const result = data?.data;
      if (result?.updated) {
        alert(`티커가 변경되었습니다: ${result.old_ticker ?? '-'} -> ${result.new_ticker ?? '-'}`);
      } else {
        alert(`티커 변경 없음: ${result?.message ?? 'unknown_error'}`);
      }
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to resolve product ticker');
    } finally {
      setResolvingProductTickerIds((prev) => prev.filter((id) => id !== productId));
    }
  };

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const institutionId = parseInt(newAccount.institution_id, 10);
      const siblingOrders = accounts
        .filter((item) => item.institution_id === institutionId)
        .map((item) => item.display_order ?? 0);
      const nextOrder = Math.max(0, ...siblingOrders) + 1;
      const payload = {
        institution_id: institutionId,
        name: newAccount.name,
        type: newAccount.type,
        allow_snapshot_input: newAccount.allow_snapshot_input,
        display_order: nextOrder,
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/accounts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to create account');
      setNewAccount({
        institution_id: '',
        name: '',
        type: '위탁계좌',
        allow_snapshot_input: true,
        display_order: '0',
      });
      setShowAccountForm(false);
      fetchAccounts();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create account');
    }
  };

  const handleSaveAccountOrder = async () => {
    const sortedAccounts = getSortedAccounts();
    const updatedAccounts: Account[] = [];
    const displayOrderMap = new Map<number, number>();

    sortedAccounts.forEach((account) => {
      const siblingCount = updatedAccounts.filter(
        (item) => item.institution_id === account.institution_id
      ).length;
      const displayOrder = siblingCount + 1;
      updatedAccounts.push({ ...account, display_order: displayOrder });
      displayOrderMap.set(account.account_id, displayOrder);
    });

    try {
      setSavingAccountOrder(true);
      const payload = {
        items: updatedAccounts.map((item) => ({
          account_id: item.account_id,
          display_order: item.display_order,
        })),
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/accounts:reorder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to update display order');
      setAccounts((prev) =>
        prev.map((item) => {
          const newOrder = displayOrderMap.get(item.account_id);
          return newOrder == null ? item : { ...item, display_order: newOrder };
        })
      );
      alert('계좌 표시순서가 저장되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update display order');
    } finally {
      setSavingAccountOrder(false);
    }
  };

  const openAccountEdit = (account: Account) => {
    setEditingAccount({
      account_id: account.account_id,
      institution_id: account.institution_id,
      name: account.name,
      type: account.type,
      allow_snapshot_input: account.allow_snapshot_input,
      display_order: String(account.display_order ?? 0),
    });
    setShowAccountEditForm(true);
    setShowAccountForm(false);
  };

  const cancelAccountEdit = () => {
    setEditingAccount(null);
    setShowAccountEditForm(false);
  };

  const handleUpdateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingAccount) return;
    try {
      const payload = {
        name: editingAccount.name,
        type: editingAccount.type,
        allow_snapshot_input: editingAccount.allow_snapshot_input,
        display_order: parseInt(editingAccount.display_order, 10) || 0,
      };
      const response = await fetch(
        `${API_BASE_URL}/portfolio/accounts/${editingAccount.account_id}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        }
      );
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to update account');
      cancelAccountEdit();
      fetchAccounts();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update account');
    }
  };

  const handleDeleteAccount = async (accountId: number) => {
    if (!window.confirm('계좌를 삭제하시겠습니까?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/portfolio/accounts/${accountId}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to delete account');
      }

      if (editingAccount?.account_id === accountId) {
        cancelAccountEdit();
      }
      await fetchAccounts();
      await fetchAccountGroups();
      await fetchHoldings();
      alert('계좌가 삭제되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete account');
    }
  };

  const handleToggleAccountInGroup = (accountId: number) => {
    setNewAccountGroup((prev) => {
      const exists = prev.account_ids.includes(accountId);
      return {
        ...prev,
        account_ids: exists
          ? prev.account_ids.filter((id) => id !== accountId)
          : [...prev.account_ids, accountId],
      };
    });
  };

  const handleToggleAccountInEditingGroup = (accountId: number) => {
    setEditingAccountGroup((prev) => {
      if (!prev) return prev;
      const exists = prev.account_ids.includes(accountId);
      return {
        ...prev,
        account_ids: exists
          ? prev.account_ids.filter((id) => id !== accountId)
          : [...prev.account_ids, accountId],
      };
    });
  };

  const handleCreateAccountGroup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAccountGroup.name.trim()) {
      alert('그룹명을 입력해주세요.');
      return;
    }
    if (newAccountGroup.account_ids.length === 0) {
      alert('포함할 계좌를 1개 이상 선택해주세요.');
      return;
    }

    try {
      const payload = {
        name: newAccountGroup.name.trim(),
        account_ids: newAccountGroup.account_ids,
        include_in_report: newAccountGroup.include_in_report,
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/account-groups`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to create account group');

      setNewAccountGroup({ name: '', account_ids: [], include_in_report: false });
      setShowAccountGroupForm(false);
      await fetchAccountGroups();
      alert('계좌그룹이 생성되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create account group');
    }
  };

  const openAccountGroupEdit = (group: AccountGroup) => {
    setEditingAccountGroup({
      account_group_id: group.account_group_id,
      name: group.name,
      account_ids: [...group.account_ids],
      include_in_report: group.include_in_report,
    });
    setShowAccountGroupEditForm(true);
    setShowAccountGroupForm(false);
  };

  const cancelAccountGroupEdit = () => {
    setEditingAccountGroup(null);
    setShowAccountGroupEditForm(false);
  };

  const handleUpdateAccountGroup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingAccountGroup) return;
    if (!editingAccountGroup.name.trim()) {
      alert('그룹명을 입력해주세요.');
      return;
    }
    if (editingAccountGroup.account_ids.length === 0) {
      alert('포함할 계좌를 1개 이상 선택해주세요.');
      return;
    }

    try {
      const payload = {
        name: editingAccountGroup.name.trim(),
        account_ids: editingAccountGroup.account_ids,
        include_in_report: editingAccountGroup.include_in_report,
      };
      const response = await fetch(
        `${API_BASE_URL}/portfolio/account-groups/${editingAccountGroup.account_group_id}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        }
      );
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to update account group');

      cancelAccountGroupEdit();
      await fetchAccountGroups();
      alert('계좌그룹이 수정되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update account group');
    }
  };

  const handleSaveAccountGroupOrder = async () => {
    const sortedGroups = [...accountGroups].sort((a, b) => {
      const diff = (a.display_order ?? 0) - (b.display_order ?? 0);
      if (diff !== 0) {
        return diff;
      }
      return a.account_group_id - b.account_group_id;
    });

    const updatedGroups = sortedGroups.map((group, index) => ({
      ...group,
      display_order: index + 1,
    }));

    try {
      setSavingAccountGroupOrder(true);
      const payload = {
        items: updatedGroups.map((item) => ({
          account_group_id: item.account_group_id,
          display_order: item.display_order,
        })),
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/account-groups:reorder`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to update display order');
      setAccountGroups(updatedGroups);
      alert('계좌그룹 표시순서가 저장되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update display order');
    } finally {
      setSavingAccountGroupOrder(false);
    }
  };

  const handleDeleteAccountGroup = async (accountGroupId: number) => {
    if (!window.confirm('계좌그룹을 삭제하시겠습니까?')) return;

    try {
      const response = await fetch(`${API_BASE_URL}/portfolio/account-groups/${accountGroupId}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to delete account group');

      if (editingAccountGroup?.account_group_id === accountGroupId) {
        cancelAccountGroupEdit();
      }
      await fetchAccountGroups();
      alert('계좌그룹이 삭제되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete account group');
    }
  };

  const handleCreateSnapshot = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/portfolio/snapshots`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newSnapshot),
      });
      if (!response.ok) throw new Error('Failed to create snapshot');
      setNewSnapshot({ user_id: 1, reference_date: new Date().toISOString().split('T')[0] });
      setShowSnapshotForm(false);
      fetchSnapshots();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create snapshot');
    }
  };

  const handleCreateHolding = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        account_id: parseInt(newHolding.account_id, 10),
        product_id: parseInt(newHolding.product_id, 10),
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/holdings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to create holding');
      }
      setNewHolding({ account_id: '', product_id: '' });
      setShowHoldingForm(false);
      fetchHoldings();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create holding');
    }
  };

  const handleDeleteHolding = async (holdingId: number) => {
    if (!window.confirm('보유자산을 삭제하시겠습니까?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/portfolio/holdings/${holdingId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'hard_delete' }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Failed to delete holding');
      }

      await fetchHoldings();
      await fetchSnapshotHoldings();
      alert('보유자산이 삭제되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete holding');
    }
  };

  const handleSaveSnapshotHoldings = async () => {
    if (!selectedSnapshotId) {
      alert('스냅샷을 선택해주세요.');
      return;
    }

    const snapshotId = parseInt(selectedSnapshotId, 10);
    const existingByHoldingId = new Map<number, SnapshotHolding>();
    snapshotHoldings
      .filter((item) => item.snapshot_id === snapshotId)
      .forEach((item) => {
        existingByHoldingId.set(item.holding_id, item);
      });

    const targets = filterSnapshotInputEligibleHoldings(holdings, products, accounts)
      .map((holding) => ({
        holding,
        amount: snapshotHoldingDrafts[holding.holding_id] ?? '',
        existing: existingByHoldingId.get(holding.holding_id) || null,
      }))
      .filter((item) => String(item.amount).trim() !== '');

    if (targets.length === 0) {
      alert('저장할 평가금액이 없습니다.');
      return;
    }

    const invalid = targets.find((item) => {
      const normalized = normalizeSnapshotAmountInput(String(item.amount));
      return normalized === '' || Number.isNaN(parseFloat(normalized));
    });
    if (invalid) {
      alert('평가금액은 숫자만 입력해주세요.');
      return;
    }

    try {
      setSavingSnapshotHoldings(true);
      await Promise.all(
        targets.map((item) => {
          const payload = {
            valuation_amount: parseFloat(
              normalizeSnapshotAmountInput(String(item.amount))
            ),
            data_source: item.existing?.data_source || snapshotHoldingDataSource,
          };
          return fetch(
            `${API_BASE_URL}/portfolio/snapshots/${snapshotId}/holdings/${item.holding.holding_id}`,
            {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload),
            }
          ).then((response) => {
            if (!response.ok) {
              throw new Error('Failed to save snapshot holding');
            }
          });
        })
      );
      await fetchSnapshotHoldings();
      if (typeof window !== 'undefined') {
        window.localStorage.removeItem(snapshotDraftStorageKey(snapshotId));
      }
      alert('스냅샷 보유자산이 저장되었습니다.');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to save snapshot holdings');
    } finally {
      setSavingSnapshotHoldings(false);
    }
  };

  const handleResetSnapshotDrafts = () => {
    if (!selectedSnapshotId) {
      return;
    }
    const snapshotId = parseInt(selectedSnapshotId, 10);
    setSnapshotHoldingDrafts(buildSnapshotDrafts(snapshotId, false));
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(snapshotDraftStorageKey(snapshotId));
    }
  };

  const handleCloneSnapshot = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (!cloneForm.source_snapshot_id) {
        alert('원본 스냅샷을 선택해주세요.');
        return;
      }
      if (!cloneForm.reference_date) {
        alert('기준일을 입력해주세요.');
        return;
      }
      const sourceSnapshotId = Number(cloneForm.source_snapshot_id);
      if (!Number.isFinite(sourceSnapshotId) || sourceSnapshotId <= 0) {
        alert('유효한 스냅샷을 선택해주세요.');
        return;
      }
      const endpoint = cloneForm.period_type === 'weekly' ? 'weekly-snapshots' : 'annual-snapshots';
      const payload = {
        user_id: 1,
        reference_date: cloneForm.reference_date,
        source_snapshot_id: sourceSnapshotId,
      };
      const response = await fetch(
        `${API_BASE_URL}/portfolio/${endpoint}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        }
      );
      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || 'Failed to clone snapshot');
      }
      if (cloneForm.period_type === 'weekly') {
        await fetchWeeklySnapshots();
      } else {
        await fetchAnnualSnapshots();
      }
      alert(`${cloneForm.period_type === 'weekly' ? '주간' : '연간'} 스냅샷이 생성되었습니다.`);
      setCloneForm({
        source_snapshot_id: '',
        period_type: 'weekly',
        reference_date: new Date().toISOString().split('T')[0],
      });
      setShowCloneForm(false);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to clone snapshot');
    }
  };

  const handleLoadReport = async () => {
    try {
      setLoading(true);
      let url = '';
      const { report_type, reference_date, account_id, account_group_id } = reportFilter;
      
      if (report_type === 'weekly_account' && account_id) {
        url = `${API_BASE_URL}/portfolio/reports/weekly/accounts?user_id=1&start_date=${reference_date}&end_date=${reference_date}`;
      } else if (report_type === 'annual_account' && account_id) {
        url = `${API_BASE_URL}/portfolio/reports/annual/accounts?user_id=1`;
      } else if (report_type === 'weekly_account_group' && account_group_id) {
        url = `${API_BASE_URL}/portfolio/reports/weekly/account-groups?user_id=1&start_date=${reference_date}&end_date=${reference_date}`;
      } else if (report_type === 'annual_account_group' && account_group_id) {
        url = `${API_BASE_URL}/portfolio/reports/annual/account-groups?user_id=1`;
      } else if (report_type === 'asset_class') {
        url = `${API_BASE_URL}/portfolio/reports/asset-class?user_id=1&snapshot_date=${reference_date}`;
      } else {
        alert('필수 파라미터를 입력해주세요.');
        return;
      }

      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to load report');
      const result = await response.json();
      setReports(Array.isArray(result) ? result : [result]);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error loading report');
    } finally {
      setLoading(false);
    }
  };

  const handleLockSnapshot = async (snapshotId: number) => {
    if (!window.confirm('스냅샷을 잠금 처리하시겠습니까?')) return;
    try {
      const response = await fetch(`${API_BASE_URL}/portfolio/snapshots/${snapshotId}/lock`, {
        method: 'POST',
      });
      
      const result = await response.json();
      
      if (!response.ok) {
        // 서버에서 반환한 실제 에러 메시지 표시
        const errorMsg = result?.message || 'Failed to lock snapshot';
        
        // 이미 잠긴 경우 상태 동기화
        if (result?.code === 'SNAPSHOT_LOCKED') {
          await fetchSnapshots();
          alert(`이미 잠금 처리된 스냅샷입니다.\n${errorMsg}`);
        } else {
          alert(`잠금 처리 실패:\n${errorMsg}`);
        }
        return;
      }
      
      const lockedAt = new Date().toISOString();
      setSnapshots((prev) => prev.map((snap) => (
        snap.snapshot_id === snapshotId
          ? { ...snap, status: 'locked', locked_at: lockedAt }
          : snap
      )));
      alert('스냅샷이 잠금 처리되었습니다.');
      await fetchSnapshots();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to lock snapshot');
    }
  };

  const handleUnlockSnapshot = async (snapshotId: number) => {
    if (!window.confirm('스냅샷 잠금을 해제하시겠습니까?')) return;
    try {
      const response = await fetch(`${API_BASE_URL}/portfolio/snapshots/${snapshotId}/unlock`, {
        method: 'POST',
      });
      
      const result = await response.json();
      
      if (!response.ok) {
        const errorMsg = result?.message || 'Failed to unlock snapshot';
        alert(`잠금 해제 실패:\n${errorMsg}`);
        return;
      }
      
      setSnapshots((prev) => prev.map((snap) => (
        snap.snapshot_id === snapshotId
          ? { ...snap, status: 'in_progress', locked_at: null }
          : snap
      )));
      alert('스냅샷 잠금이 해제되었습니다.');
      await fetchSnapshots();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to unlock snapshot');
    }
  };

  const canUnlockSnapshot = (snapshot: Snapshot): boolean => {
    // 잠금 상태가 아니면 해제 불가
    if (snapshot.status !== 'locked') return false;
    
    // 기준일로부터 7일이 지났는지 확인
    const referenceDate = new Date(snapshot.reference_date);
    const today = new Date();
    const daysDiff = Math.floor((today.getTime() - referenceDate.getTime()) / (1000 * 60 * 60 * 24));
    if (daysDiff >= 7) return false;
    
    // 기준일이 더 늦은 잠금된 스냅샷이 있는지 확인
    const hasLaterLockedSnapshot = snapshots.some(
      (s) => s.status === 'locked' && s.reference_date > snapshot.reference_date
    );
    if (hasLaterLockedSnapshot) return false;
    
    return true;
  };

  const openHoldingsForAccount = (accountId: number) => {
    setHoldingsAccountFilter(accountId);
    setHoldingsProductFilter(null);
    setActiveTab('holdings');
  };

  const openHoldingsForProduct = (productId: number) => {
    setHoldingsProductFilter(productId);
    setHoldingsAccountFilter(null);
    setActiveTab('holdings');
  };

  const openSnapshotHoldings = (snapshotId: number) => {
    setSelectedSnapshotId(String(snapshotId));
    setActiveTab('snapshotHoldings');
  };

  const openAnnualSnapshotHoldings = (annualSnapshotId: number) => {
    setSelectedAnnualSnapshotId(String(annualSnapshotId));
    setActiveTab('annualSnapshotHoldings');
    fetchAnnualSnapshotHoldings(annualSnapshotId);
  };

  const openClonePanel = (snapshot: Snapshot) => {
    setCloneForm({
      source_snapshot_id: String(snapshot.snapshot_id),
      period_type: 'weekly',
      reference_date: snapshot.reference_date,
    });
    setShowSnapshotForm(false);
    setShowCloneForm(true);
  };

  const clearHoldingsFilter = () => {
    setHoldingsAccountFilter(null);
    setHoldingsProductFilter(null);
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>포트폴리오 관리</h1>
      </header>

      <div className={styles.ribbon}>
        {/* Group 0: Users */}
        <div className={styles.ribbonGroup}>
          <div className={styles.groupLabel}>사용자</div>
          <div className={styles.groupButtons}>
            <button
              className={activeTab === 'users' ? styles.activeTab : ''}
              onClick={() => setActiveTab('users')}
            >
              사용자 관리
            </button>
          </div>
        </div>

        {/* Group 1: Basic Data */}
        <div className={styles.ribbonGroup}>
          <div className={styles.groupLabel}>데이터 관리</div>
          <div className={styles.groupButtons}>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                className={activeTab === 'institutions' ? styles.activeTab : ''}
                onClick={() => setActiveTab('institutions')}
                style={{ flex: 1 }}
              >
                금융기관
              </button>
              <button
                className={activeTab === 'accounts' ? styles.activeTab : ''}
                onClick={() => setActiveTab('accounts')}
                style={{ flex: 1 }}
              >
                계좌
              </button>
            </div>
            <button
              className={activeTab === 'accountGroups' ? styles.activeTab : ''}
              onClick={() => setActiveTab('accountGroups')}
            >
              계좌그룹
            </button>
            <button
              className={activeTab === 'holdings' ? styles.activeTab : ''}
              onClick={() => setActiveTab('holdings')}
            >
              보유자산
            </button>
            <button
              className={activeTab === 'products' ? styles.activeTab : ''}
              onClick={() => setActiveTab('products')}
            >
              상품
            </button>
          </div>
        </div>

        {/* Group 2: Snapshots */}
        <div className={styles.ribbonGroup}>
          <div className={styles.groupLabel}>스냅샷</div>
          <div className={styles.groupButtons}>
            <button
              className={activeTab === 'snapshots' ? styles.activeTab : ''}
              onClick={() => setActiveTab('snapshots')}
            >
              일일 스냅샷
            </button>
            <button
              className={activeTab === 'weeklySnapshots' ? styles.activeTab : ''}
              onClick={() => setActiveTab('weeklySnapshots')}
            >
              주간 스냅샷
            </button>
            <button
              className={activeTab === 'annualSnapshots' ? styles.activeTab : ''}
              onClick={() => setActiveTab('annualSnapshots')}
            >
              연간 스냅샷
            </button>
          </div>
        </div>

        {/* Group 3: Reports & Analysis */}
        <div className={styles.ribbonGroup}>
          <div className={styles.groupLabel}>분석</div>
          <div className={styles.groupButtons}>
            <button
              className={activeTab === 'weeklyReport' ? styles.activeTab : ''}
              onClick={() => setActiveTab('weeklyReport')}
            >
              주간 보고서
            </button>
            <button
              className={activeTab === 'annualReport' ? styles.activeTab : ''}
              onClick={() => setActiveTab('annualReport')}
            >
              연간 보고서
            </button>
            <button
              className={activeTab === 'snapshotAnalysis' ? styles.activeTab : ''}
              onClick={() => setActiveTab('snapshotAnalysis')}
            >
              스냅샷 분석
            </button>
            <button
              className={activeTab === 'targetAllocations' ? styles.activeTab : ''}
              onClick={() => setActiveTab('targetAllocations')}
            >
              목표 자산배분
            </button>
          </div>
        </div>
      </div>

      {error && <div className={styles.error}>{error}</div>}

      {/* Users Tab */}
      {activeTab === 'users' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>사용자 목록 ({users.length})</h2>
            <div className={styles.actionButtons}>
              <button onClick={() => setShowUserForm(!showUserForm)}>
                {showUserForm ? '취소' : '+ 사용자 추가'}
              </button>
              <button onClick={fetchUsers}>새로고침</button>
            </div>
          </div>

          {showUserForm && (
            <form onSubmit={handleCreateUser} className={styles.form}>
              <input
                type="text"
                placeholder="사용자명 *"
                value={newUser.username}
                onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                required
              />
              <input
                type="email"
                placeholder="이메일 *"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                required
              />
              <input
                type="text"
                placeholder="전체 이름"
                value={newUser.full_name}
                onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
              />
              <button type="submit">생성</button>
            </form>
          )}

          {users.length === 0 ? (
            <div className={styles.infoBox}>
              <p>등록된 사용자가 없습니다.</p>
            </div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>사용자명</th>
                  <th>이메일</th>
                  <th>전체 이름</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td>{user.full_name || '-'}</td>
                    <td>
                      <button
                        onClick={() => handleDeleteUser(user.id)}
                        className={styles.deleteButton}
                      >
                        삭제
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Institutions Tab */}
      {activeTab === 'institutions' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>금융기관 목록</h2>
            <div className={styles.actionButtons}>
              <button
                onClick={handleSaveInstitutionOrder}
                disabled={savingInstitutionOrder}
              >
                {savingInstitutionOrder ? '저장 중...' : '표시순서 저장'}
              </button>
              <button onClick={() => setShowInstitutionForm(!showInstitutionForm)}>
                {showInstitutionForm ? '취소' : '+ 추가'}
              </button>
            </div>
          </div>

          {showInstitutionForm && (
            <form onSubmit={handleCreateInstitution} className={styles.form}>
              <input
                type="text"
                placeholder="기관명 (예: KB증권)"
                value={newInstitution.name}
                onChange={(e) => setNewInstitution({ ...newInstitution, name: e.target.value })}
                required
              />
              <select
                value={newInstitution.type}
                onChange={(e) => setNewInstitution({ ...newInstitution, type: e.target.value })}
              >
                <option value="증권사">증권사</option>
                <option value="은행">은행</option>
                <option value="기타기관">기타기관</option>
              </select>
              <button type="submit">생성</button>
            </form>
          )}

          {showInstitutionEditForm && editingInstitution && (
            <form onSubmit={handleUpdateInstitution} className={styles.form}>
              <input
                type="text"
                placeholder="기관명 (예: KB증권)"
                value={editingInstitution.name}
                onChange={(e) =>
                  setEditingInstitution({
                    ...editingInstitution,
                    name: e.target.value,
                  })
                }
                required
              />
              <select
                value={editingInstitution.type}
                onChange={(e) =>
                  setEditingInstitution({
                    ...editingInstitution,
                    type: e.target.value,
                  })
                }
              >
                <option value="증권사">증권사</option>
                <option value="은행">은행</option>
                <option value="기타기관">기타기관</option>
              </select>
              <button type="submit">저장</button>
              <button type="button" onClick={cancelInstitutionEdit}>
                취소
              </button>
            </form>
          )}

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            <table className={`${styles.table} ${styles.institutionsTable}`}>
              <colgroup>
                <col style={{ width: '64px' }} />
                <col style={{ width: '72px' }} />
                <col style={{ width: '110px' }} />
                <col />
                <col style={{ width: '180px' }} />
                <col style={{ width: '130px' }} />
                <col style={{ width: '140px' }} />
              </colgroup>
              <thead>
                <tr>
                  <th>정렬</th>
                  <th>번호</th>
                  <th>유형</th>
                  <th>기관명</th>
                  <th className={styles.amount} style={{ textAlign: 'right' }}>자산총합</th>
                  <th>생성일</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                {getSortedInstitutions().map((inst, index) => (
                  <tr
                    key={inst.institution_id}
                    onDragOver={(event) => event.preventDefault()}
                    onDrop={() => handleInstitutionDrop(inst.institution_id)}
                  >
                    <td
                      className={styles.dragHandle}
                      draggable
                      onDragStart={() => handleInstitutionDragStart(inst.institution_id)}
                      onDragEnd={() => setDraggingInstitutionId(null)}
                      title="드래그하여 순서 변경"
                    >
                      ::
                    </td>
                    <td>{index + 1}</td>
                    <td>{inst.type}</td>
                    <td>{inst.name}</td>
                    <td className={styles.amount} style={{ textAlign: 'right' }}>
                      {inst.total_assets !== undefined && inst.total_assets > 0 
                        ? inst.total_assets.toLocaleString('ko-KR', { maximumFractionDigits: 0 })
                        : '-'
                      }
                    </td>
                    <td>{new Date(inst.created_at).toLocaleDateString()}</td>
                    <td>
                      <div className={styles.actionButtons}>
                        <button onClick={() => openInstitutionEdit(inst)}>수정</button>
                        {(accountReferenceCountByInstitutionId.get(inst.institution_id) ?? 0) === 0 && (
                          <button
                            onClick={() => handleDeleteInstitution(inst.institution_id)}
                            className={styles.deleteButton}
                          >
                            삭제
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Products Tab */}
      {activeTab === 'products' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>상품 목록</h2>
            <div className={styles.actionButtons}>
              <button
                onClick={handleSaveProductOrder}
                disabled={savingProductOrder}
              >
                {savingProductOrder ? '저장 중...' : '표시순서 저장'}
              </button>
              <button
                onClick={() => setShowProductBetaView((prev) => !prev)}
              >
                {showProductBetaView ? '일반 보기' : '베타 보기'}
              </button>
              {showProductBetaView && (
                <button
                  onClick={handleCollectAllProductBetas}
                  disabled={collectingAllProductBeta}
                >
                  {collectingAllProductBeta ? '수집 중...' : '전체 베타 수집'}
                </button>
              )}
              <button
                onClick={() => {
                  setShowProductForm(!showProductForm);
                  setShowProductEditForm(false);
                  setEditingProduct(null);
                }}
              >
                {showProductForm ? '취소' : '+ 추가'}
              </button>
            </div>
          </div>

          {showProductForm && (
            <form onSubmit={handleCreateProduct} className={styles.form}>
              <input
                type="text"
                placeholder="상품명 (예: 삼성전자)"
                value={newProduct.product_name}
                onChange={(e) => setNewProduct({ ...newProduct, product_name: e.target.value })}
                required
              />
              <select
                value={newProduct.asset_class}
                onChange={(e) => setNewProduct({ ...newProduct, asset_class: e.target.value })}
              >
                <option value="주식">주식</option>
                <option value="채권">채권</option>
                <option value="통화">통화</option>
                <option value="금">금</option>
                <option value="부동산">부동산</option>
                <option value="가상자산">가상자산</option>
                <option value="기타자산">기타자산</option>
              </select>
              <select
                value={newProduct.region}
                onChange={(e) => setNewProduct({ ...newProduct, region: e.target.value })}
              >
                <option value="대한민국">대한민국</option>
                <option value="미국">미국</option>
              </select>
              <select
                value={newProduct.currency}
                onChange={(e) => setNewProduct({ ...newProduct, currency: e.target.value })}
              >
                <option value="KRW">KRW</option>
                <option value="USD">USD</option>
              </select>
              <select
                value={newProduct.investment_type}
                onChange={(e) => setNewProduct({ ...newProduct, investment_type: e.target.value })}
              >
                <option value="직접">직접</option>
                <option value="ETF">ETF</option>
              </select>
              <select
                value={newProduct.risk_level}
                onChange={(e) => setNewProduct({ ...newProduct, risk_level: e.target.value })}
              >
                <option value="안전">안전</option>
                <option value="위험">위험</option>
              </select>
              <label>
                <input
                  type="checkbox"
                  checked={newProduct.allow_snapshot_input}
                  onChange={(e) =>
                    setNewProduct({ ...newProduct, allow_snapshot_input: e.target.checked })
                  }
                />
                스냅샷 평가금액 입력 허용
              </label>
              <input
                type="text"
                placeholder="티커 (예: FNGU, QLD, 005930.KS)"
                value={newProduct.ticker}
                onChange={(e) => setNewProduct({ ...newProduct, ticker: e.target.value })}
              />
              <input
                type="text"
                placeholder="특성 (쉼표로 구분, 선택사항)"
                value={newProduct.characteristics}
                onChange={(e) => setNewProduct({ ...newProduct, characteristics: e.target.value })}
              />
              <button type="submit">생성</button>
            </form>
          )}

          {showProductEditForm && editingProduct && (
            <form onSubmit={handleUpdateProduct} className={styles.form}>
              <input
                type="text"
                placeholder="상품명 (예: 삼성전자)"
                value={editingProduct.product_name}
                onChange={(e) =>
                  setEditingProduct({
                    ...editingProduct,
                    product_name: e.target.value,
                  })
                }
                required
              />
              <select
                value={editingProduct.asset_class}
                onChange={(e) =>
                  setEditingProduct({
                    ...editingProduct,
                    asset_class: e.target.value,
                  })
                }
              >
                <option value="주식">주식</option>
                <option value="채권">채권</option>
                <option value="통화">통화</option>
                <option value="금">금</option>
                <option value="부동산">부동산</option>
                <option value="가상자산">가상자산</option>
                <option value="기타자산">기타자산</option>
              </select>
              <select
                value={editingProduct.region}
                onChange={(e) =>
                  setEditingProduct({
                    ...editingProduct,
                    region: e.target.value,
                  })
                }
              >
                <option value="대한민국">대한민국</option>
                <option value="미국">미국</option>
              </select>
              <select
                value={editingProduct.currency}
                onChange={(e) =>
                  setEditingProduct({
                    ...editingProduct,
                    currency: e.target.value,
                  })
                }
              >
                <option value="KRW">KRW</option>
                <option value="USD">USD</option>
              </select>
              <select
                value={editingProduct.investment_type}
                onChange={(e) =>
                  setEditingProduct({
                    ...editingProduct,
                    investment_type: e.target.value,
                  })
                }
              >
                <option value="직접">직접</option>
                <option value="ETF">ETF</option>
              </select>
              <select
                value={editingProduct.risk_level}
                onChange={(e) =>
                  setEditingProduct({
                    ...editingProduct,
                    risk_level: e.target.value,
                  })
                }
              >
                <option value="안전">안전</option>
                <option value="위험">위험</option>
              </select>
              <label>
                <input
                  type="checkbox"
                  checked={editingProduct.allow_snapshot_input}
                  onChange={(e) =>
                    setEditingProduct({
                      ...editingProduct,
                      allow_snapshot_input: e.target.checked,
                    })
                  }
                />
                스냅샷 평가금액 입력 허용
              </label>
              <input
                type="text"
                placeholder="티커 (예: FNGU, QLD, 005930.KS)"
                value={editingProduct.ticker}
                onChange={(e) =>
                  setEditingProduct({
                    ...editingProduct,
                    ticker: e.target.value,
                  })
                }
              />
              <input
                type="text"
                placeholder="특성 (쉼표로 구분, 선택사항)"
                value={editingProduct.characteristics}
                onChange={(e) =>
                  setEditingProduct({
                    ...editingProduct,
                    characteristics: e.target.value,
                  })
                }
              />
              <button type="submit">저장</button>
              <button type="button" onClick={cancelProductEdit}>
                취소
              </button>
            </form>
          )}

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>정렬</th>
                  <th>번호</th>
                  <th>상품명</th>
                  <th>자산군</th>
                  {!showProductBetaView && <th>지역</th>}
                  {!showProductBetaView && <th>통화</th>}
                  {!showProductBetaView && <th>투자유형</th>}
                  {!showProductBetaView && <th>위험도</th>}
                  {!showProductBetaView && <th>스냅샷 입력</th>}
                  {showProductBetaView && <th>티커</th>}
                  {showProductBetaView && <th>국내베타</th>}
                  {showProductBetaView && <th>국제베타</th>}
                  {showProductBetaView && <th>수집일</th>}
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                {getSortedProducts().map((prod, index) => (
                  <tr
                    key={prod.product_id}
                    onDragOver={(event) => event.preventDefault()}
                    onDrop={() => handleProductDrop(prod.product_id)}
                  >
                    <td
                      className={styles.dragHandle}
                      draggable
                      onDragStart={() => handleProductDragStart(prod.product_id)}
                      onDragEnd={() => setDraggingProductId(null)}
                      title="드래그하여 순서 변경"
                    >
                      ::
                    </td>
                    <td>{index + 1}</td>
                    <td>{prod.product_name}</td>
                    <td>{prod.asset_class}</td>
                    {!showProductBetaView && <td>{prod.region}</td>}
                    {!showProductBetaView && <td>{prod.currency}</td>}
                    {!showProductBetaView && <td>{prod.investment_type}</td>}
                    {!showProductBetaView && <td>{prod.risk_level}</td>}
                    {!showProductBetaView && <td>{prod.allow_snapshot_input ? '허용' : '제외'}</td>}
                    {showProductBetaView && <td>{prod.ticker ?? '-'}</td>}
                    {showProductBetaView && <td>{formatBeta(prod.domestic_beta)}</td>}
                    {showProductBetaView && <td>{formatBeta(prod.global_beta)}</td>}
                    {showProductBetaView && <td>{formatCollectedDate(prod.beta_collected_at)}</td>}
                    <td>
                      <div className={styles.actionButtons}>
                        {showProductBetaView ? (
                          <>
                            <button
                              onClick={() => handleResolveProductTicker(prod.product_id)}
                              disabled={resolvingProductTickerIds.includes(prod.product_id)}
                            >
                              {resolvingProductTickerIds.includes(prod.product_id)
                                ? '변경 중...'
                                : '티커변경'}
                            </button>
                            <button
                              onClick={() => handleCollectProductBeta(prod.product_id)}
                              disabled={collectingProductBetaIds.includes(prod.product_id)}
                            >
                              {collectingProductBetaIds.includes(prod.product_id)
                                ? '수집 중...'
                                : '베타 수집'}
                            </button>
                          </>
                        ) : (
                          <>
                            <button onClick={() => openProductEdit(prod)}>수정</button>
                            {(holdingReferenceCountByProductId.get(prod.product_id) ?? 0) === 0 && (
                              <button
                                onClick={() => handleDeleteProduct(prod.product_id)}
                                className={styles.deleteButton}
                              >
                                삭제
                              </button>
                            )}
                            <button onClick={() => openHoldingsForProduct(prod.product_id)}>
                              보유자산 보기
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Accounts Tab */}
      {activeTab === 'accounts' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>계좌 목록</h2>
            <div className={styles.actionButtons}>
              <button
                onClick={handleSaveAccountOrder}
                disabled={savingAccountOrder}
              >
                {savingAccountOrder ? '저장 중...' : '표시순서 저장'}
              </button>
              <button
                onClick={() => {
                  setShowAccountForm(!showAccountForm);
                  setShowAccountEditForm(false);
                  setEditingAccount(null);
                }}
              >
                {showAccountForm ? '취소' : '+ 추가'}
              </button>
            </div>
          </div>

          {showAccountForm && (
            <form onSubmit={handleCreateAccount} className={styles.form}>
              <select
                value={newAccount.institution_id}
                onChange={(e) => setNewAccount({ ...newAccount, institution_id: e.target.value })}
                required
              >
                <option value="">금융기관 선택</option>
                {institutions.map((inst) => (
                  <option key={inst.institution_id} value={inst.institution_id}>
                    {inst.name}
                  </option>
                ))}
              </select>
              <input
                type="text"
                placeholder="계좌명 (예: 주식계좌)"
                value={newAccount.name}
                onChange={(e) => setNewAccount({ ...newAccount, name: e.target.value })}
                required
              />
              <select
                value={newAccount.type}
                onChange={(e) => setNewAccount({ ...newAccount, type: e.target.value })}
              >
                {ACCOUNT_TYPES.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
              <label style={{ display: 'block', margin: '10px 0' }}>
                <input
                  type="checkbox"
                  checked={newAccount.allow_snapshot_input}
                  onChange={(e) =>
                    setNewAccount({
                      ...newAccount,
                      allow_snapshot_input: e.target.checked,
                    })
                  }
                  style={{ marginRight: '8px' }}
                />
                스냅샷 평가금액 입력 허용
              </label>
              <button type="submit">생성</button>
            </form>
          )}

          {showAccountEditForm && editingAccount && (
            <form onSubmit={handleUpdateAccount} className={styles.form}>
              <select value={editingAccount.institution_id} disabled>
                {institutions.map((inst) => (
                  <option key={inst.institution_id} value={inst.institution_id}>
                    {inst.name}
                  </option>
                ))}
              </select>
              <input
                type="text"
                placeholder="계좌명 (예: 주식계좌)"
                value={editingAccount.name}
                onChange={(e) =>
                  setEditingAccount({
                    ...editingAccount,
                    name: e.target.value,
                  })
                }
                required
              />
              <select
                value={editingAccount.type}
                onChange={(e) =>
                  setEditingAccount({
                    ...editingAccount,
                    type: e.target.value,
                  })
                }
              >
                {ACCOUNT_TYPES.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
              <label style={{ display: 'block', margin: '10px 0' }}>
                <input
                  type="checkbox"
                  checked={editingAccount.allow_snapshot_input}
                  onChange={(e) =>
                    setEditingAccount({
                      ...editingAccount,
                      allow_snapshot_input: e.target.checked,
                    })
                  }
                  style={{ marginRight: '8px' }}
                />
                스냅샷 평가금액 입력 허용
              </label>
              <button type="submit">저장</button>
              <button type="button" onClick={cancelAccountEdit}>
                취소
              </button>
            </form>
          )}

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>정렬</th>
                  <th>번호</th>
                  <th>금융기관</th>
                  <th>계좌명</th>
                  <th>유형</th>
                  <th>스냅샷 입력</th>
                  <th>생성일</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                {getSortedAccounts().map((acc, index) => {
                  const inst = institutions.find((i) => i.institution_id === acc.institution_id);
                  return (
                    <tr
                      key={acc.account_id}
                      onDragOver={(event) => event.preventDefault()}
                      onDrop={() => handleAccountDrop(acc.account_id)}
                    >
                      <td
                        className={styles.dragHandle}
                        draggable
                        onDragStart={() => handleAccountDragStart(acc.account_id)}
                        onDragEnd={() => setDraggingAccountId(null)}
                        title="드래그하여 순서 변경"
                      >
                        ::
                      </td>
                      <td>{index + 1}</td>
                      <td>{inst?.name || acc.institution_id}</td>
                      <td>{acc.name}</td>
                      <td>{acc.type}</td>
                      <td>{acc.allow_snapshot_input ? '허용' : '제외'}</td>
                      <td>{new Date(acc.created_at).toLocaleDateString()}</td>
                      <td>
                        <div className={styles.actionButtons}>
                          <button onClick={() => openAccountEdit(acc)}>수정</button>
                          {(holdingReferenceCountByAccountId.get(acc.account_id) ?? 0) === 0 && (
                            <button
                              onClick={() => handleDeleteAccount(acc.account_id)}
                              className={styles.deleteButton}
                            >
                              삭제
                            </button>
                          )}
                          <button onClick={() => openHoldingsForAccount(acc.account_id)}>
                            보유자산 보기
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Account Groups Tab */}
      {activeTab === 'accountGroups' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>계좌그룹 목록</h2>
            <div>
              {accountGroups.length > 0 && (
                <button
                  onClick={handleSaveAccountGroupOrder}
                  disabled={savingAccountGroupOrder}
                  style={{ marginRight: '10px' }}
                >
                  {savingAccountGroupOrder ? '저장 중...' : '표시순서 저장'}
                </button>
              )}
              <button
                onClick={() => {
                  setShowAccountGroupForm((prev) => !prev);
                  setShowAccountGroupEditForm(false);
                  setEditingAccountGroup(null);
                  if (showAccountGroupForm) {
                    setNewAccountGroup({ name: '', account_ids: [], include_in_report: false });
                  }
                }}
              >
                {showAccountGroupForm ? '취소' : '+ 추가'}
              </button>
            </div>
          </div>

          {showAccountGroupForm && (
            <form onSubmit={handleCreateAccountGroup} className={styles.form}>
              <input
                type="text"
                placeholder="그룹명 (예: 미국 투자 계좌)"
                value={newAccountGroup.name}
                onChange={(e) =>
                  setNewAccountGroup((prev) => ({
                    ...prev,
                    name: e.target.value,
                  }))
                }
                required
              />
              <div style={{ border: '1px solid #ddd', borderRadius: '6px', padding: '10px', maxHeight: '220px', overflowY: 'auto' }}>
                {getSortedAccounts().map((account) => {
                  const institution = institutions.find((item) => item.institution_id === account.institution_id);
                  return (
                    <label key={account.account_id} style={{ display: 'block', marginBottom: '6px' }}>
                      <input
                        type="checkbox"
                        checked={newAccountGroup.account_ids.includes(account.account_id)}
                        onChange={() => handleToggleAccountInGroup(account.account_id)}
                        style={{ marginRight: '8px' }}
                      />
                      {institution?.name ?? '-'} / {account.name} ({account.type})
                    </label>
                  );
                })}
              </div>
              <label style={{ display: 'block', margin: '10px 0' }}>
                <input
                  type="checkbox"
                  checked={newAccountGroup.include_in_report}
                  onChange={(e) =>
                    setNewAccountGroup((prev) => ({
                      ...prev,
                      include_in_report: e.target.checked,
                    }))
                  }
                  style={{ marginRight: '8px' }}
                />
                보고서에 포함
              </label>
              <button type="submit">생성</button>
            </form>
          )}

          {showAccountGroupEditForm && editingAccountGroup && (
            <form onSubmit={handleUpdateAccountGroup} className={styles.form}>
              <input
                type="text"
                placeholder="그룹명"
                value={editingAccountGroup.name}
                onChange={(e) =>
                  setEditingAccountGroup((prev) =>
                    prev
                      ? {
                          ...prev,
                          name: e.target.value,
                        }
                      : prev
                  )
                }
                required
              />
              <div style={{ border: '1px solid #ddd', borderRadius: '6px', padding: '10px', maxHeight: '220px', overflowY: 'auto' }}>
                {getSortedAccounts().map((account) => {
                  const institution = institutions.find((item) => item.institution_id === account.institution_id);
                  return (
                    <label key={`edit-${account.account_id}`} style={{ display: 'block', marginBottom: '6px' }}>
                      <input
                        type="checkbox"
                        checked={editingAccountGroup.account_ids.includes(account.account_id)}
                        onChange={() => handleToggleAccountInEditingGroup(account.account_id)}
                        style={{ marginRight: '8px' }}
                      />
                      {institution?.name ?? '-'} / {account.name} ({account.type})
                    </label>
                  );
                })}
              </div>
              <label style={{ display: 'block', margin: '10px 0' }}>
                <input
                  type="checkbox"
                  checked={editingAccountGroup.include_in_report}
                  onChange={(e) =>
                    setEditingAccountGroup((prev) =>
                      prev
                        ? {
                            ...prev,
                            include_in_report: e.target.checked,
                          }
                        : prev
                    )
                  }
                  style={{ marginRight: '8px' }}
                />
                보고서에 포함
              </label>
              <div className={styles.actionButtons}>
                <button type="submit">저장</button>
                <button type="button" onClick={cancelAccountGroupEdit}>취소</button>
              </div>
            </form>
          )}

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th style={{ width: '40px' }}></th>
                  <th>번호</th>
                  <th>그룹명</th>
                  <th>포함 계좌</th>
                  <th>보고서 포함</th>
                  <th>생성일</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                {accountGroups.length === 0 ? (
                  <tr>
                    <td colSpan={7}>생성된 계좌그룹이 없습니다.</td>
                  </tr>
                ) : (
                  accountGroups
                    .sort((a, b) => {
                      const diff = (a.display_order ?? 0) - (b.display_order ?? 0);
                      if (diff !== 0) {
                        return diff;
                      }
                      return a.account_group_id - b.account_group_id;
                    })
                    .map((group, index) => (
                    <tr
                      key={group.account_group_id}
                      onDragOver={(event) => event.preventDefault()}
                      onDrop={() => handleAccountGroupDrop(group.account_group_id)}
                    >
                      <td
                        className={styles.dragHandle}
                        draggable
                        onDragStart={() => handleAccountGroupDragStart(group.account_group_id)}
                        onDragEnd={() => setDraggingAccountGroupId(null)}
                        title="드래그하여 순서 변경"
                      >
                        ::
                      </td>
                      <td>{index + 1}</td>
                      <td>{group.name}</td>
                      <td>
                        {group.account_ids.length === 0
                          ? '-'
                          : group.account_ids.map((accountId) => {
                              const account = accounts.find((item) => item.account_id === accountId);
                              const institution = institutions.find(
                                (item) => item.institution_id === account?.institution_id
                              );
                              return (
                                <div key={`${group.account_group_id}-${accountId}`}>
                                  {institution?.name ?? '-'} / {account?.name ?? `계좌ID ${accountId}`}
                                </div>
                              );
                            })}
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <input
                          type="checkbox"
                          checked={group.include_in_report}
                          readOnly
                          style={{ cursor: 'default' }}
                        />
                      </td>
                      <td>{new Date(group.created_at).toLocaleDateString()}</td>
                      <td>
                        <div className={styles.actionButtons}>
                          <button type="button" onClick={() => openAccountGroupEdit(group)}>
                            수정
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDeleteAccountGroup(group.account_group_id)}
                          >
                            삭제
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Snapshots Tab */}
      {activeTab === 'snapshots' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>스냅샷 목록</h2>
            <button onClick={() => setShowSnapshotForm(!showSnapshotForm)}>
              {showSnapshotForm ? '취소' : '+ 추가'}
            </button>
          </div>

          {showSnapshotForm && (
            <form onSubmit={handleCreateSnapshot} className={styles.form}>
              <input
                type="date"
                value={newSnapshot.reference_date}
                onChange={(e) => setNewSnapshot({ ...newSnapshot, reference_date: e.target.value })}
                required
              />
              <button type="submit">생성</button>
            </form>
          )}

          {showCloneForm && (
            <form onSubmit={handleCloneSnapshot} className={styles.form}>
              <input
                type="text"
                value={cloneSourceSnapshot
                  ? `${cloneSourceSnapshot.reference_date} (ID: ${cloneSourceSnapshot.snapshot_id})`
                  : '원본 스냅샷 미선택'
                }
                readOnly
              />
              <input
                type="date"
                value={cloneForm.reference_date}
                onChange={(e) => setCloneForm({ ...cloneForm, reference_date: e.target.value })}
                required
              />
              <select
                value={cloneForm.period_type}
                onChange={(e) => setCloneForm({ ...cloneForm, period_type: e.target.value })}
              >
                <option value="weekly">주간 스냅샷</option>
                <option value="annual">연간 스냅샷</option>
              </select>
              <div className={styles.actionButtons}>
                <button type="submit">복제</button>
                <button type="button" onClick={() => setShowCloneForm(false)}>취소</button>
              </div>
            </form>
          )}

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>번호</th>
                  <th>기준일</th>
                  <th>상태</th>
                  <th>잠금일시</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                {sortedSnapshots.map((snap, index) => (
                  <tr key={snap.snapshot_id}>
                    <td>{index + 1}</td>
                    <td>{snap.reference_date}</td>
                    <td>{snap.status === 'locked' ? '🔒 잠금' : '✏️ 편집 가능'}</td>
                    <td>{snap.locked_at ? new Date(snap.locked_at).toLocaleString() : '-'}</td>
                    <td>
                      <div className={styles.actionButtons}>
                        <button onClick={() => openSnapshotHoldings(snap.snapshot_id)}>
                          보유자산 보기
                        </button>
                        {snap.status === 'locked' && (
                          <>
                            <button onClick={() => openClonePanel(snap)}>복제</button>
                            {canUnlockSnapshot(snap) && (
                              <button onClick={() => handleUnlockSnapshot(snap.snapshot_id)}>
                                잠금 해제
                              </button>
                            )}
                          </>
                        )}
                        {snap.status !== 'locked' && (
                          <button onClick={() => handleLockSnapshot(snap.snapshot_id)}>
                            잠금
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Weekly Snapshots Tab */}
      {activeTab === 'weeklySnapshots' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>주간 스냅샷 목록</h2>
          </div>

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>번호</th>
                  <th>기준일</th>
                  <th>상태</th>
                  <th>생성일</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                {sortedWeeklySnapshots.map((snap, index) => (
                  <tr key={snap.weekly_snapshot_id}>
                    <td>{index + 1}</td>
                    <td>{snap.reference_date}</td>
                    <td>{snap.status === 'locked' ? '🔒 잠금' : '✏️ 편집 가능'}</td>
                    <td>{new Date(snap.created_at).toLocaleString()}</td>
                    <td>
                      <div className={styles.actionButtons}>
                        <button onClick={() => openSnapshotHoldings(snap.source_snapshot_id)}>
                          보유자산 보기
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Annual Snapshots Tab */}
      {activeTab === 'annualSnapshots' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>연간 스냅샷 목록</h2>
          </div>

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>번호</th>
                  <th>기준일</th>
                  <th>상태</th>
                  <th>생성일</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                {sortedAnnualSnapshots.map((snap, index) => (
                  <tr key={snap.annual_snapshot_id}>
                    <td>{index + 1}</td>
                    <td>{snap.reference_date}</td>
                    <td>{snap.status === 'locked' ? '🔒 잠금' : '✏️ 편집 가능'}</td>
                    <td>{new Date(snap.created_at).toLocaleString()}</td>
                    <td>
                      <div className={styles.actionButtons}>
                        <button onClick={() => openAnnualSnapshotHoldings(snap.annual_snapshot_id)}>
                          보유자산 보기
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Annual Snapshot Holdings Tab */}
      {activeTab === 'annualSnapshotHoldings' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>연간 스냅샷 보유자산 목록</h2>
          </div>

          <div className={styles.form}>
            <select
              value={selectedAnnualSnapshotId}
              onChange={(e) => {
                const snapshotId = e.target.value;
                setSelectedAnnualSnapshotId(snapshotId);
                if (!snapshotId) {
                  setAnnualSnapshotHoldings([]);
                  return;
                }
                fetchAnnualSnapshotHoldings(parseInt(snapshotId, 10));
              }}
              required
            >
              <option value="">연간 스냅샷 선택</option>
              {sortedAnnualSnapshots.map((snap) => (
                <option key={snap.annual_snapshot_id} value={snap.annual_snapshot_id}>
                  {snap.reference_date}
                </option>
              ))}
            </select>
          </div>

          {!selectedAnnualSnapshotId ? (
            <div className={styles.loading}>연간 스냅샷을 선택해주세요.</div>
          ) : loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            (() => {
              const totalSum = annualSnapshotHoldings.reduce(
                (sum, item) => sum + Number(item.valuation_amount || 0),
                0
              );

              const rows: React.ReactNode[] = [];
              let currentAccountId: number | null = null;
              let currentAccountLabel = '';
              let accountSum = 0;

              annualSnapshotHoldings.forEach((item, index) => {
                // Account changed - push previous account summary
                if (
                  item.account_id !== currentAccountId &&
                  currentAccountId !== null
                ) {
                  rows.push(
                    <tr key={`summary-${currentAccountId}`}>
                      <td colSpan={4}>계좌 합계 ({currentAccountLabel})</td>
                      <td style={{ textAlign: 'right', fontWeight: 'bold' }}>
                        {accountSum.toLocaleString('ko-KR', {
                          minimumFractionDigits: 0,
                          maximumFractionDigits: 0,
                        })}
                      </td>
                      <td colSpan={2}></td>
                    </tr>
                  );
                }

                // Update current account context
                if (item.account_id !== currentAccountId) {
                  currentAccountId = item.account_id;
                  currentAccountLabel = item.account_name;
                  accountSum = 0;
                }

                accountSum += Number(item.valuation_amount || 0);

                rows.push(
                  <tr key={item.annual_snapshot_holding_id}>
                    <td>{index + 1}</td>
                    <td>{item.institution_name}</td>
                    <td>{item.account_name}</td>
                    <td>{item.product_name}</td>
                    <td style={{ textAlign: 'right' }}>
                      {Number(item.valuation_amount || 0).toLocaleString('ko-KR', {
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 0,
                      })}
                    </td>
                    <td>{getDataSourceLabel(item.data_source)}</td>
                    <td>{item.created_at ? new Date(item.created_at).toLocaleString() : '-'}</td>
                  </tr>
                );
              });

              // Push final account summary
              if (currentAccountId !== null) {
                rows.push(
                  <tr key={`summary-${currentAccountId}-final`}>
                    <td colSpan={4}>계좌 합계 ({currentAccountLabel})</td>
                    <td style={{ textAlign: 'right', fontWeight: 'bold' }}>
                      {accountSum.toLocaleString('ko-KR', {
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 0,
                      })}
                    </td>
                    <td colSpan={2}></td>
                  </tr>
                );
              }

              return (
                <table className={styles.table}>
                  <thead>
                    <tr>
                      <th>번호</th>
                      <th>금융기관</th>
                      <th>계좌</th>
                      <th>상품</th>
                      <th>평가금액</th>
                      <th>데이터출처</th>
                      <th>생성일</th>
                    </tr>
                  </thead>
                  <tbody>
                    {annualSnapshotHoldings.length === 0 ? (
                      <tr>
                        <td colSpan={7}>보유자산 데이터가 없습니다.</td>
                      </tr>
                    ) : (
                      <>
                        <tr>
                          <td colSpan={4}>전체 합계</td>
                          <td style={{ textAlign: 'right', fontWeight: 'bold' }}>
                            {totalSum.toLocaleString('ko-KR', {
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                            })}
                          </td>
                          <td colSpan={2}></td>
                        </tr>
                        {rows}
                        <tr>
                          <td colSpan={4}>전체 합계</td>
                          <td style={{ textAlign: 'right', fontWeight: 'bold' }}>
                            {totalSum.toLocaleString('ko-KR', {
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                            })}
                          </td>
                          <td colSpan={2}></td>
                        </tr>
                      </>
                    )}
                  </tbody>
                </table>
              );
            })()
          )}
        </div>
      )}

      {/* Holdings Tab */}
      {activeTab === 'holdings' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>보유자산 목록</h2>
            <button onClick={() => setShowHoldingForm(!showHoldingForm)}>
              {showHoldingForm ? '취소' : '+ 추가'}
            </button>
          </div>

          <div className={styles.filterRow}>
            <label htmlFor="holdings-account-filter">계좌 필터</label>
            <select
              id="holdings-account-filter"
              value={holdingsAccountFilter ?? ''}
              onChange={(e) =>
                setHoldingsAccountFilter(
                  e.target.value ? Number(e.target.value) : null
                )
              }
            >
              <option value="">전체</option>
              {accounts.map((acc) => {
                const inst = institutions.find((i) => i.institution_id === acc.institution_id);
                return (
                  <option key={acc.account_id} value={acc.account_id}>
                    {inst?.name || acc.institution_id} - {acc.name}
                  </option>
                );
              })}
            </select>
            <label htmlFor="holdings-product-filter">상품 필터</label>
            <select
              id="holdings-product-filter"
              value={holdingsProductFilter ?? ''}
              onChange={(e) =>
                setHoldingsProductFilter(
                  e.target.value ? Number(e.target.value) : null
                )
              }
            >
              <option value="">전체</option>
              {products.map((prod) => (
                <option key={prod.product_id} value={prod.product_id}>
                  {prod.product_name}
                </option>
              ))}
            </select>
            {(holdingsAccountFilter !== null || holdingsProductFilter !== null) && (
              <button type="button" onClick={clearHoldingsFilter}>
                필터 해제
              </button>
            )}
          </div>

          {showHoldingForm && (
            <form onSubmit={handleCreateHolding} className={styles.form}>
              <select
                value={holdingInstitutionFilter}
                onChange={(e) => {
                  const nextInstitution = e.target.value;
                  setHoldingInstitutionFilter(nextInstitution);
                  if (nextInstitution) {
                    const stillValid = accounts.some(
                      (acc) =>
                        acc.account_id.toString() === newHolding.account_id &&
                        acc.institution_id.toString() === nextInstitution
                    );
                    if (!stillValid) {
                      setNewHolding({ ...newHolding, account_id: '' });
                    }
                  }
                }}
              >
                <option value="">금융기관 전체</option>
                {institutions.map((inst) => (
                  <option key={inst.institution_id} value={inst.institution_id}>
                    {inst.name}
                  </option>
                ))}
              </select>
              <select
                value={newHolding.account_id}
                onChange={(e) => setNewHolding({ ...newHolding, account_id: e.target.value })}
                required
              >
                <option value="">계좌 선택</option>
                {accounts
                  .filter((acc) =>
                    holdingInstitutionFilter
                      ? acc.institution_id.toString() === holdingInstitutionFilter
                      : true
                  )
                  .map((acc) => {
                  const inst = institutions.find((i) => i.institution_id === acc.institution_id);
                  return (
                    <option key={acc.account_id} value={acc.account_id}>
                      {inst?.name || acc.institution_id} - {acc.name}
                    </option>
                  );
                })}
              </select>
              <select
                value={newHolding.product_id}
                onChange={(e) => setNewHolding({ ...newHolding, product_id: e.target.value })}
                required
              >
                <option value="">상품 선택</option>
                {products.map((prod) => (
                  <option key={prod.product_id} value={prod.product_id}>
                    {prod.product_name}
                  </option>
                ))}
              </select>
              <button type="submit">생성</button>
            </form>
          )}

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>번호</th>
                  <th>금융기관</th>
                  <th>계좌이름</th>
                  <th>상품이름</th>
                  <th>생성일</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                {holdings
                  .filter(h => !h.deleted_at)
                  .filter((holding) =>
                    holdingsAccountFilter === null
                      ? true
                      : holding.account_id === holdingsAccountFilter
                  )
                  .filter((holding) =>
                    holdingsProductFilter === null
                      ? true
                      : holding.product_id === holdingsProductFilter
                  )
                  .map((holding): HoldingView => {
                    const account = accounts.find((acc) => acc.account_id === holding.account_id) || null;
                    const institution = institutions.find((i) => i.institution_id === account?.institution_id) || null;
                    const product = products.find((p) => p.product_id === holding.product_id) || null;
                    return {
                      holding,
                      account,
                      institution,
                      product,
                    };
                  })
                  .sort((a, b) => {
                    const instOrderA = a.institution?.display_order ?? 0;
                    const instOrderB = b.institution?.display_order ?? 0;
                    if (instOrderA !== instOrderB) {
                      return instOrderA - instOrderB;
                    }
                    const accOrderA = a.account?.display_order ?? 0;
                    const accOrderB = b.account?.display_order ?? 0;
                    if (accOrderA !== accOrderB) {
                      return accOrderA - accOrderB;
                    }
                    const prodOrderA = a.product?.display_order ?? 0;
                    const prodOrderB = b.product?.display_order ?? 0;
                    if (prodOrderA !== prodOrderB) {
                      return prodOrderA - prodOrderB;
                    }
                    return a.holding.holding_id - b.holding.holding_id;
                  })
                  .map(({ holding, account, institution, product }, index) => {
                    return (
                      <tr key={holding.holding_id}>
                        <td>{index + 1}</td>
                        <td>{institution?.name || account?.institution_id || '-'}</td>
                        <td>{account?.name || holding.account_id}</td>
                        <td>{product?.product_name || holding.product_id}</td>
                        <td>{new Date(holding.created_at).toLocaleDateString()}</td>
                        <td>
                          {(snapshotHoldingReferenceCountByHoldingId.get(holding.holding_id) ?? 0) === 0 && (
                            <button
                              onClick={() => handleDeleteHolding(holding.holding_id)}
                              className={styles.deleteButton}
                            >
                              삭제
                            </button>
                          )}
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Snapshot Holdings Tab */}
      {activeTab === 'snapshotHoldings' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>스냅샷 보유자산 입력</h2>
            <div className={styles.actionButtons}>
              <button
                onClick={handleResetSnapshotDrafts}
                disabled={!selectedSnapshotId}
              >
                로컬 값 초기화
              </button>
              <button
                onClick={handleSaveSnapshotHoldings}
                disabled={!selectedSnapshotId || savingSnapshotHoldings || isSelectedSnapshotLocked}
              >
                {savingSnapshotHoldings ? '저장 중...' : '일괄 저장'}
              </button>
            </div>
          </div>

          <div className={styles.form}>
            <select
              value={selectedSnapshotId}
              onChange={(e) => setSelectedSnapshotId(e.target.value)}
              required
            >
              <option value="">스냅샷 선택</option>
              {sortedSnapshots.map((snap) => (
                <option key={snap.snapshot_id} value={snap.snapshot_id}>
                  {snap.reference_date}
                </option>
              ))}
            </select>
          </div>

          <div className={styles.assetClassLegend} aria-label="자산군 색상 범례">
            {ASSET_CLASS_ORDER.map((assetClass) => (
              <span key={assetClass} className={styles.assetClassLegendItem}>
                <span
                  className={styles.assetClassIcon}
                  style={{ backgroundColor: getAssetClassColor(assetClass) }}
                  aria-hidden="true"
                />
                <span>{assetClass}</span>
              </span>
            ))}
          </div>

          {!selectedSnapshotId ? (
            <div className={styles.loading}>스냅샷을 선택해주세요.</div>
          ) : loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            (() => {
              const snapshotId = parseInt(selectedSnapshotId, 10);
              const snapshot = snapshots.find((s) => s.snapshot_id === snapshotId) || null;
              const isSnapshotLocked = snapshot?.status === 'locked';
              const selectedReferenceDateMs = snapshot
                ? new Date(snapshot.reference_date).getTime()
                : Number.NaN;
              const holdingMap = new Map<number, SnapshotHolding>();
              snapshotHoldings
                .filter((item) => item.snapshot_id === snapshotId)
                .forEach((item) => {
                  holdingMap.set(item.holding_id, item);
                });

              const nearestPreviousSnapshot = snapshots
                .filter((item) => {
                  const itemReferenceDateMs = new Date(item.reference_date).getTime();
                  return (
                    Number.isFinite(selectedReferenceDateMs)
                    && Number.isFinite(itemReferenceDateMs)
                    && itemReferenceDateMs < selectedReferenceDateMs
                  );
                })
                .sort((a, b) => {
                  const dateDiff =
                    new Date(b.reference_date).getTime() - new Date(a.reference_date).getTime();
                  if (dateDiff !== 0) {
                    return dateDiff;
                  }
                  return b.snapshot_id - a.snapshot_id;
                })[0] || null;

              const previousAmountsByHolding = new Map<number, number>();
              if (nearestPreviousSnapshot) {
                snapshotHoldings
                  .filter((item) => item.snapshot_id === nearestPreviousSnapshot.snapshot_id)
                  .forEach((item) => {
                    const amount = parseFloat(
                      normalizeSnapshotAmountInput(String(item.valuation_amount))
                    );
                    if (!Number.isNaN(amount)) {
                      previousAmountsByHolding.set(item.holding_id, amount);
                    }
                  });
              }

              const views = filterSnapshotInputVisibleHoldings(holdings, products, accounts, {
                currentValueHoldingIds: holdingMap.keys(),
                previousValueHoldingIds: previousAmountsByHolding.keys(),
              })
                .map((holding) => {
                  const account = accounts.find((a) => a.account_id === holding.account_id) || null;
                  const institution = institutions.find((i) => i.institution_id === account?.institution_id) || null;
                  const product = products.find((p) => p.product_id === holding.product_id) || null;
                  const isInputAllowed = (
                    isProductAllowedForSnapshotInput(product)
                    && isAccountAllowedForSnapshotInput(account)
                  );
                  return {
                    holding,
                    account,
                    institution,
                    product,
                    existing: holdingMap.get(holding.holding_id) || null,
                    isInputAllowed,
                    isReadOnly: isSnapshotLocked || !isInputAllowed,
                  };
                })
                .sort((a, b) => {
                  const instOrderA = a.institution?.display_order ?? 0;
                  const instOrderB = b.institution?.display_order ?? 0;
                  if (instOrderA !== instOrderB) {
                    return instOrderA - instOrderB;
                  }
                  const accOrderA = a.account?.display_order ?? 0;
                  const accOrderB = b.account?.display_order ?? 0;
                  if (accOrderA !== accOrderB) {
                    return accOrderA - accOrderB;
                  }
                  const prodOrderA = a.product?.display_order ?? 0;
                  const prodOrderB = b.product?.display_order ?? 0;
                  if (prodOrderA !== prodOrderB) {
                    return prodOrderA - prodOrderB;
                  }
                  return a.holding.holding_id - b.holding.holding_id;
                });

              const parseAmount = (value: string | number | null | undefined) => {
                if (value == null) {
                  return 0;
                }
                const parsed = parseFloat(normalizeSnapshotAmountInput(String(value)));
                return Number.isNaN(parsed) ? 0 : parsed;
              };

              const isDraftDifferent = (
                draftValue: string | number | null | undefined,
                existingValue: string | number | null | undefined
              ) => {
                const draftNormalized = normalizeSnapshotAmountInput(String(draftValue ?? ''));
                const existingNormalized = normalizeSnapshotAmountInput(String(existingValue ?? ''));
                if (draftNormalized === '' && existingNormalized === '') {
                  return false;
                }
                const draftNumber = parseAmount(draftNormalized);
                const existingNumber = parseAmount(existingNormalized);
                return draftNumber !== existingNumber;
              };

              const formatAmount = (value: number) => value.toLocaleString();
              const formatRatio = (value: number) => `${value.toFixed(2)}%`;
              const truncateText = (text: string, maxLength: number = 47) => {
                if (text.length <= maxLength) return text;
                return text.substring(0, maxLength) + '...';
              };

              const totalSum = views.reduce((sum, view) => {
                const draftValue = snapshotHoldingDrafts[view.holding.holding_id];
                const effectiveValue = view.isReadOnly
                  ? (view.existing?.valuation_amount ?? '')
                  : (draftValue !== undefined ? draftValue : (view.existing?.valuation_amount ?? ''));
                return sum + parseAmount(effectiveValue);
              }, 0);
              const totalPreviousSum = views.reduce((sum, view) => {
                const previousAmount = previousAmountsByHolding.get(view.holding.holding_id);
                return sum + (previousAmount ?? 0);
              }, 0);
              // Group views by account
              const viewsByAccount = new Map<number, typeof views>();
              views.forEach((view) => {
                const accountId = view.account?.account_id ?? view.holding.account_id;
                if (!viewsByAccount.has(accountId)) {
                  viewsByAccount.set(accountId, []);
                }
                viewsByAccount.get(accountId)!.push(view);
              });

              const rows: React.ReactNode[] = [];
              let globalIndex = 0;

              viewsByAccount.forEach((accountViews) => {
                let accountSum = 0;
                let accountPreviousSum = 0;
                const firstView = accountViews[0];
                const accountLabel = `${firstView.institution?.name || '-'} - ${firstView.account?.name || '-'}`;
                const accountId = firstView.account?.account_id ?? firstView.holding.account_id;

                accountViews.forEach((view) => {
                  const draftValue = snapshotHoldingDrafts[view.holding.holding_id];
                  const effectiveValue = view.isReadOnly
                    ? (view.existing?.valuation_amount ?? '')
                    : (draftValue !== undefined ? draftValue : (view.existing?.valuation_amount ?? ''));
                  const amount = parseAmount(effectiveValue);
                  const previousAmount = previousAmountsByHolding.get(view.holding.holding_id) ?? 0;

                  accountSum += amount;
                  accountPreviousSum += previousAmount;

                  globalIndex += 1;
                  rows.push(
                    <tr key={`${snapshotId}-${view.holding.holding_id}`}>
                      <td>{globalIndex}</td>
                      <td>{truncateText(view.institution?.name || '-')}</td>
                      <td>{truncateText(view.account?.name || '-')}</td>
                      <td>
                        <div className={styles.productNameCell}>
                          <span
                            className={styles.assetClassIcon}
                            style={{ backgroundColor: getAssetClassColor(view.product?.asset_class) }}
                            title={view.product?.asset_class || '기타자산'}
                            aria-label={`자산종류: ${view.product?.asset_class || '기타자산'}`}
                          />
                          <span title={view.product?.product_name || '-'}>
                            {truncateText(view.product?.product_name || '-')}
                          </span>
                        </div>
                      </td>
                      <td className={styles.amountCell}>
                        {previousAmount != null && previousAmount > 0 ? formatAmount(previousAmount) : '-'}
                      </td>
                      <td>
                        {(() => {
                          const draftValue = snapshotHoldingDrafts[view.holding.holding_id];
                          const displayValue = view.isReadOnly
                            ? (view.existing?.valuation_amount ?? '')
                            : (draftValue !== undefined ? draftValue : (view.existing?.valuation_amount ?? ''));
                          const isDirty = !view.isReadOnly
                            && isDraftDifferent(displayValue, view.existing?.valuation_amount);
                          return (
                            <input
                              type="text"
                              inputMode="decimal"
                              className={`${styles.amountInput}${isDirty ? ` ${styles.amountInputDirty}` : ''}`}
                              data-index={globalIndex - 1}
                              data-holding-id={view.holding.holding_id}
                              value={displayValue}
                              readOnly={view.isReadOnly}
                              disabled={isSnapshotLocked}
                              placeholder={view.isInputAllowed ? undefined : '조회 전용'}
                              title={view.isInputAllowed
                                ? undefined
                                : '입력 제외 상태입니다. 수정이 필요하면 입력 허용으로 변경한 뒤 다시 제외해 주세요.'}
                              onChange={(e) =>
                                setSnapshotHoldingDrafts((prev) => ({
                                  ...prev,
                                  [view.holding.holding_id]: e.target.value,
                                }))
                              }
                              onBlur={(e) => {
                                const formatted = formatSnapshotAmountInput(e.target.value);
                                if (formatted !== e.target.value) {
                                  setSnapshotHoldingDrafts((prev) => ({
                                    ...prev,
                                    [view.holding.holding_id]: formatted,
                                  }));
                                }
                              }}
                              onKeyDown={handleSnapshotAmountKeyDown}
                            />
                          );
                        })()}
                      </td>
                      <td className={styles.amountCell}>
                        {formatRatio(totalSum > 0 ? (amount / totalSum) * 100 : 0)}
                      </td>
                      <td>
                        {view.isInputAllowed
                          ? getDataSourceLabel(view.existing?.data_source || snapshotHoldingDataSource)
                          : `조회 전용${view.existing?.data_source ? ` · ${getDataSourceLabel(view.existing.data_source)}` : ''}`}
                      </td>
                    </tr>
                  );
                });

                rows.push(
                  <tr key={`summary-${accountId}`}>
                    <td colSpan={4}>계좌 합계 ({accountLabel})</td>
                    <td className={styles.amountCell}>{formatAmount(accountPreviousSum)}</td>
                    <td className={styles.amountCell}>{formatAmount(accountSum)}</td>
                    <td className={styles.amountCell}>
                      {formatRatio(totalSum > 0 ? (accountSum / totalSum) * 100 : 0)}
                    </td>
                    <td></td>
                  </tr>
                );
              });

              return (
                <table className={styles.table} ref={snapshotHoldingsTableRef}>
                  <thead>
                    <tr>
                      <th>번호</th>
                      <th>금융기관</th>
                      <th>계좌이름</th>
                      <th>상품이름</th>
                      <th>
                        이전 평가금액
                        {nearestPreviousSnapshot
                          ? ` (${nearestPreviousSnapshot.reference_date})`
                          : ' (-)'}
                      </th>
                      <th>평가금액</th>
                      <th>비중</th>
                      <th>데이터소스</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colSpan={4}>전체 합계</td>
                      <td className={styles.amountCell}>{formatAmount(totalPreviousSum)}</td>
                      <td className={styles.amountCell}>{formatAmount(totalSum)}</td>
                      <td className={styles.amountCell}>{formatRatio(totalSum > 0 ? 100 : 0)}</td>
                      <td></td>
                    </tr>
                    {rows}
                    <tr>
                      <td colSpan={4}>전체 합계</td>
                      <td className={styles.amountCell}>{formatAmount(totalPreviousSum)}</td>
                      <td className={styles.amountCell}>{formatAmount(totalSum)}</td>
                      <td className={styles.amountCell}>{formatRatio(totalSum > 0 ? 100 : 0)}</td>
                      <td></td>
                    </tr>
                  </tbody>
                </table>
              );
            })()
          )}
        </div>
      )}

      {/* Weekly Pivot Report Tab */}
      {activeTab === 'weeklyReport' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>주간 보고서 (Pivot)</h2>
            <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
              <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', userSelect: 'none' }}>
                <input
                  type="checkbox"
                  checked={showMonthEndOnly}
                  onChange={(e) => setShowMonthEndOnly(e.target.checked)}
                  style={{ marginRight: '8px', cursor: 'pointer', width: '16px', height: '16px' }}
                />
                <span style={{ fontSize: '13px', fontWeight: 'normal' }}>월말만 보기</span>
              </label>
              <div>
                <label style={{ marginRight: '10px' }}>연도:</label>
                <select
                  value={weeklyReportYear}
                  onChange={(e) => setWeeklyReportYear(Number(e.target.value))}
                  style={{ padding: '5px 10px', fontSize: '13px' }}
                >
                  {[2024, 2025, 2026, 2027, 2028].map((year) => (
                    <option key={year} value={year}>
                      {year}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : weeklyReportData && weeklyReportData.weeks.length > 0 ? (
            (() => {
              // 필터링 로직: 월말 또는 현재 주 스냅샷만 표시
              const filteredWeeks = showMonthEndOnly
                ? weeklyReportData.weeks.filter((week, weekIdx, allWeeks) => {
                    const currentDate = new Date(week.reference_date);
                    const now = new Date();
                    
                    // 현재 주인지 확인 (ISO week 기준으로 현재 주 포함)
                    const isCurrentWeek = (() => {
                      const weekStart = new Date(currentDate);
                      weekStart.setDate(currentDate.getDate() - currentDate.getDay()); // 주의 시작 (일요일)
                      const weekEnd = new Date(weekStart);
                      weekEnd.setDate(weekStart.getDate() + 6); // 주의 끝 (토요일)
                      return now >= weekStart && now <= weekEnd;
                    })();
                    
                    // 월말인지 확인
                    const currentYearMonth = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}`;
                    const isMonthEnd = weekIdx === allWeeks.length - 1 || 
                      (() => {
                        const nextDate = new Date(allWeeks[weekIdx + 1].reference_date);
                        const nextYearMonth = `${nextDate.getFullYear()}-${String(nextDate.getMonth() + 1).padStart(2, '0')}`;
                        return currentYearMonth !== nextYearMonth;
                      })();
                    
                    return isMonthEnd || isCurrentWeek;
                  })
                : weeklyReportData.weeks;
              
              // 필터링된 데이터로 account_groups와 accounts의 valuations도 필터링
              const filteredData = {
                ...weeklyReportData,
                weeks: filteredWeeks,
                account_groups: weeklyReportData.account_groups.map(group => ({
                  ...group,
                  valuations: group.valuations.filter((_, idx) => {
                    if (!showMonthEndOnly) return true;
                    return filteredWeeks.some(w => w.weekly_snapshot_id === weeklyReportData.weeks[idx].weekly_snapshot_id);
                  })
                })),
                accounts: weeklyReportData.accounts.map(account => ({
                  ...account,
                  valuations: account.valuations.filter((_, idx) => {
                    if (!showMonthEndOnly) return true;
                    return filteredWeeks.some(w => w.weekly_snapshot_id === weeklyReportData.weeks[idx].weekly_snapshot_id);
                  })
                }))
              };
              
              return (
                <>
                  {/* 상단 스크롤바 */}
                  <div
                    ref={weeklyReportTopScrollRef}
                    style={{
                      overflowX: 'auto',
                      overflowY: 'hidden',
                      marginBottom: '10px',
                    }}
                    onScroll={(e) => {
                      if (weeklyReportBottomScrollRef.current) {
                        weeklyReportBottomScrollRef.current.scrollLeft = e.currentTarget.scrollLeft;
                      }
                    }}
                  >
                    <div style={{ width: `${weeklyReportScrollWidth}px`, height: '1px' }} />
                  </div>

              {/* 메인 테이블 */}
              <div
                 ref={weeklyReportBottomScrollRef}
                 className={styles.tableWrapperAuto}
                onScroll={(e) => {
                  if (weeklyReportTopScrollRef.current) {
                    weeklyReportTopScrollRef.current.scrollLeft = e.currentTarget.scrollLeft;
                  }
                }}
              >
                <table className={styles.table} style={{ minWidth: '800px' }}>
                <thead style={{ position: 'sticky', top: 0, zIndex: 10, backgroundColor: '#fff' }}>
                  <tr>
                    <th style={{ position: 'sticky', left: 0, backgroundColor: '#fff', zIndex: 11, width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                      금융기관
                    </th>
                    <th style={{ position: 'sticky', left: '160px', backgroundColor: '#fff', zIndex: 11, width: '260px', minWidth: '260px' }}>
                      계좌
                    </th>
                    {filteredData.weeks.map((week) => (
                      <th key={week.weekly_snapshot_id} style={{ backgroundColor: '#fff', minWidth: '100px', fontSize: '11px', padding: '6px 4px', textAlign: 'center' }}>
                        {week.reference_date} (W{week.week_number})
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {/* 계좌그룹 섹션 (상단) */}
                  {filteredData.account_groups && filteredData.account_groups.length > 0 && (
                    <>
                      <tr style={{ borderBottom: '2px solid #ccc' }}>
                        <td colSpan={filteredData.weeks.length + 2} style={{ padding: '10px 8px', backgroundColor: '#f5f5f5', fontWeight: 'bold', textAlign: 'center' }}>
                          계좌 그룹
                        </td>
                      </tr>
                      {[...filteredData.account_groups].sort((a, b) => a.display_order - b.display_order).map((group) => (
                        <tr key={group.account_group_id} style={{ backgroundColor: '#fffacd' }}>
                          <td style={{ position: 'sticky', left: 0, backgroundColor: '#fffacd', zIndex: 1, fontWeight: 'bold', width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                            {group.account_group_name}
                          </td>
                          <td style={{ position: 'sticky', left: '160px', backgroundColor: '#fffacd', zIndex: 1, fontSize: '11px', color: '#666', width: '260px', minWidth: '260px' }}>
                            (합계)
                          </td>
                          {group.valuations.map((val, idx) => (
                            <td key={idx} style={{ textAlign: 'right', fontWeight: 'bold' }}>
                              {val.amount > 0
                                ? val.amount.toLocaleString('ko-KR', {
                                    minimumFractionDigits: 0,
                                    maximumFractionDigits: 0,
                                  })
                                : '-'}
                            </td>
                          ))}
                        </tr>
                      ))}
                      {/* 계좌 그룹 총합 행 */}
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#ffeb99' }}>
                        <td style={{ position: 'sticky', left: 0, backgroundColor: '#ffeb99', zIndex: 1, width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                          총합
                        </td>
                        <td style={{ position: 'sticky', left: '160px', backgroundColor: '#ffeb99', zIndex: 1, width: '260px', minWidth: '260px' }}>
                        </td>
                        {(() => {
                          // 모든 주차의 총액 계산
                          const totals = filteredData.weeks.map((week, weekIdx) => {
                            return filteredData.accounts.reduce((sum, account) => {
                              const val = account.valuations[weekIdx];
                              return sum + (val ? val.amount : 0);
                            }, 0);
                          });
                          
                          // 최대값과 최소값 찾기 (0보다 큰 값들 중에서)
                          const validTotals = totals.filter(t => t > 0);
                          const maxTotal = validTotals.length > 0 ? Math.max(...validTotals) : 0;
                          const minTotal = validTotals.length > 0 ? Math.min(...validTotals) : 0;
                          
                          return filteredData.weeks.map((week, weekIdx) => {
                            const total = totals[weekIdx];
                            let color = 'black';
                            
                            // 최대값과 최소값이 다르고, 현재 값이 0보다 클 때만 색상 적용
                            if (total > 0 && maxTotal !== minTotal) {
                              if (total === maxTotal) {
                                color = '#d32f2f'; // Red for max
                              } else if (total === minTotal) {
                                color = '#1976d2'; // Blue for min
                              }
                            }
                            
                            return (
                              <td key={week.weekly_snapshot_id} style={{ textAlign: 'right', color: color, fontWeight: (total === maxTotal || total === minTotal) && total > 0 && maxTotal !== minTotal ? 'bold' : 'bold' }}>
                                {total > 0
                                  ? total.toLocaleString('ko-KR', {
                                      minimumFractionDigits: 0,
                                      maximumFractionDigits: 0,
                                    })
                                  : '-'}
                              </td>
                            );
                          });
                        })()}
                      </tr>
                      <tr style={{ borderTop: '2px solid #ccc', borderBottom: '2px solid #ccc' }}>
                        <td colSpan={filteredData.weeks.length + 2} style={{ padding: '10px 8px', backgroundColor: '#f5f5f5', fontWeight: 'bold', textAlign: 'center' }}>
                          전체 계좌
                        </td>
                      </tr>
                    </>
                  )}

                  {filteredData.accounts.map((account) => (
                    <tr key={account.account_id}>
                      <td style={{ position: 'sticky', left: 0, backgroundColor: '#fff', zIndex: 1, width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                        {account.institution_name}
                      </td>
                      <td style={{ position: 'sticky', left: '160px', backgroundColor: '#fff', zIndex: 1, width: '260px', minWidth: '260px' }}>
                        {account.account_name}
                      </td>
                      {account.valuations.map((val, idx) => (
                        <td key={idx} style={{ textAlign: 'right' }}>
                          {val.amount > 0
                            ? val.amount.toLocaleString('ko-KR', {
                                minimumFractionDigits: 0,
                                maximumFractionDigits: 0,
                              })
                            : '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                  {/* 합계 행 */}
                  {filteredData.accounts.length > 0 && (
                    <>
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#f0f0f0' }}>
                        <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#f0f0f0', zIndex: 1, width: '420px', minWidth: '420px' }}>
                          총합
                        </td>
                        {(() => {
                          // 모든 주차의 총액 계산
                          const totals = filteredData.weeks.map((week, weekIdx) => {
                            return filteredData.accounts.reduce((sum, account) => {
                              const val = account.valuations[weekIdx];
                              return sum + (val ? val.amount : 0);
                            }, 0);
                          });
                          
                          // 최대값과 최소값 찾기 (0보다 큰 값들 중에서)
                          const validTotals = totals.filter(t => t > 0);
                          const maxTotal = validTotals.length > 0 ? Math.max(...validTotals) : 0;
                          const minTotal = validTotals.length > 0 ? Math.min(...validTotals) : 0;
                          
                          return filteredData.weeks.map((week, weekIdx) => {
                            const total = totals[weekIdx];
                            let color = 'black';
                            
                            // 최대값과 최소값이 다르고, 현재 값이 0보다 클 때만 색상 적용
                            if (total > 0 && maxTotal !== minTotal) {
                              if (total === maxTotal) {
                                color = '#d32f2f'; // Red for max
                              } else if (total === minTotal) {
                                color = '#1976d2'; // Blue for min
                              }
                            }
                            
                            return (
                              <td key={week.weekly_snapshot_id} style={{ textAlign: 'right', color: color }}>
                                {total > 0
                                  ? total.toLocaleString('ko-KR', {
                                      minimumFractionDigits: 0,
                                      maximumFractionDigits: 0,
                                    })
                                  : '-'}
                              </td>
                            );
                          });
                        })()}
                      </tr>
                      {/* 전주 대비 변화 행들 - 월말만 보기 시 숨김 */}
                      {!showMonthEndOnly && (
                        <>
                          {/* 전주 대비 변화 (금액) 행 */}
                          <tr style={{ fontWeight: 'bold', backgroundColor: '#fff5f5' }}>
                            <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#fff5f5', zIndex: 1, width: '420px', minWidth: '420px' }}>
                              전주 대비 변화 (금액)
                            </td>
                            {filteredData.weeks.map((week, weekIdx) => {
                              const currentTotal = filteredData.accounts.reduce((sum, account) => {
                                const val = account.valuations[weekIdx];
                                return sum + (val ? val.amount : 0);
                              }, 0);

                              let changeAmount = 0;
                              let changeColor = 'black';

                              if (weekIdx > 0) {
                                const prevTotal = filteredData.accounts.reduce((sum, account) => {
                                  const val = account.valuations[weekIdx - 1];
                                  return sum + (val ? val.amount : 0);
                                }, 0);

                                changeAmount = currentTotal - prevTotal;

                                if (changeAmount >= 0) {
                                  changeColor = '#d32f2f'; // Red for positive
                                } else {
                                  changeColor = '#1976d2'; // Blue for negative
                                }
                              }

                              return (
                                <td
                                  key={week.weekly_snapshot_id}
                                  style={{
                                    textAlign: 'right',
                                    color: changeColor,
                                  }}
                                >
                                  {weekIdx > 0
                                    ? `${changeAmount >= 0 ? '+' : ''}${changeAmount.toLocaleString('ko-KR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`
                                    : '-'}
                                </td>
                              );
                            })}
                          </tr>
                          {/* 전주 대비 변화 (%) 행 */}
                          <tr style={{ fontWeight: 'bold', backgroundColor: '#ffebee' }}>
                            <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#ffebee', zIndex: 1, width: '420px', minWidth: '420px' }}>
                              전주 대비 변화 (%)
                            </td>
                            {filteredData.weeks.map((week, weekIdx) => {
                              const currentTotal = filteredData.accounts.reduce((sum, account) => {
                                const val = account.valuations[weekIdx];
                                return sum + (val ? val.amount : 0);
                              }, 0);

                              let changePercent = 0;
                              let changeColor = 'black';

                              if (weekIdx > 0) {
                                const prevTotal = filteredData.accounts.reduce((sum, account) => {
                                  const val = account.valuations[weekIdx - 1];
                                  return sum + (val ? val.amount : 0);
                                }, 0);

                                if (prevTotal > 0) {
                                  changePercent = ((currentTotal - prevTotal) / prevTotal) * 100;

                                  if (changePercent >= 1) {
                                    changeColor = '#d32f2f'; // Red
                                  } else if (changePercent <= -1) {
                                    changeColor = '#1976d2'; // Blue
                                  }
                                }
                              }

                              return (
                                <td
                                  key={week.weekly_snapshot_id}
                                  style={{
                                    textAlign: 'right',
                                    color: changeColor,
                                  }}
                                >
                                  {weekIdx > 0
                                    ? `${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(2)}%`
                                    : '-'}
                                </td>
                              );
                            })}
                          </tr>
                        </>
                      )}
                      {/* 전월 대비 변화 (금액) 행 */}
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#e3f2fd' }}>
                        <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#e3f2fd', zIndex: 1, width: '420px', minWidth: '420px' }}>
                          전월 대비 변화 (금액)
                        </td>
                        {filteredData.weeks.map((week, weekIdx) => {
                          const currentDate = new Date(week.reference_date);
                          const currentYearMonth = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}`;
                          
                          // 다음 주가 있는지 확인하고, 다른 월인지 판단
                          const isMonthEnd = weekIdx === filteredData.weeks.length - 1 || 
                            (() => {
                              const nextDate = new Date(filteredData.weeks[weekIdx + 1].reference_date);
                              const nextYearMonth = `${nextDate.getFullYear()}-${String(nextDate.getMonth() + 1).padStart(2, '0')}`;
                              return currentYearMonth !== nextYearMonth;
                            })();

                          if (!isMonthEnd) {
                            return (
                              <td key={week.weekly_snapshot_id} style={{ textAlign: 'right' }}>
                                -
                              </td>
                            );
                          }

                          // 현재 월의 총액
                          const currentTotal = filteredData.accounts.reduce((sum, account) => {
                            const val = account.valuations[weekIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);

                          // 전월 마지막 주 찾기
                          let prevMonthEndIdx = -1;
                          for (let i = weekIdx - 1; i >= 0; i--) {
                            const prevDate = new Date(filteredData.weeks[i].reference_date);
                            const prevYearMonth = `${prevDate.getFullYear()}-${String(prevDate.getMonth() + 1).padStart(2, '0')}`;
                            
                            if (prevYearMonth !== currentYearMonth) {
                              prevMonthEndIdx = i;
                              break;
                            }
                          }

                          if (prevMonthEndIdx === -1) {
                            return (
                              <td key={week.weekly_snapshot_id} style={{ textAlign: 'right' }}>
                                -
                              </td>
                            );
                          }

                          // 전월 마지막 주의 총액
                          const prevMonthTotal = filteredData.accounts.reduce((sum, account) => {
                            const val = account.valuations[prevMonthEndIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);

                          const changeAmount = currentTotal - prevMonthTotal;
                          const changeColor = changeAmount >= 0 ? '#d32f2f' : '#1976d2';

                          return (
                            <td
                              key={week.weekly_snapshot_id}
                              style={{
                                textAlign: 'right',
                                color: changeColor,
                              }}
                            >
                              {changeAmount >= 0 ? '+' : ''}{changeAmount.toLocaleString('ko-KR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                            </td>
                          );
                        })}
                      </tr>
                      {/* 전월 대비 변화 (%) 행 */}
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#bbdefb' }}>
                        <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#bbdefb', zIndex: 1, width: '420px', minWidth: '420px' }}>
                          전월 대비 변화 (%)
                        </td>
                        {filteredData.weeks.map((week, weekIdx) => {
                          const currentDate = new Date(week.reference_date);
                          const currentYearMonth = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}`;
                          
                          // 다음 주가 있는지 확인하고, 다른 월인지 판단
                          const isMonthEnd = weekIdx === filteredData.weeks.length - 1 || 
                            (() => {
                              const nextDate = new Date(filteredData.weeks[weekIdx + 1].reference_date);
                              const nextYearMonth = `${nextDate.getFullYear()}-${String(nextDate.getMonth() + 1).padStart(2, '0')}`;
                              return currentYearMonth !== nextYearMonth;
                            })();

                          if (!isMonthEnd) {
                            return (
                              <td key={week.weekly_snapshot_id} style={{ textAlign: 'right' }}>
                                -
                              </td>
                            );
                          }

                          // 현재 월의 총액
                          const currentTotal = filteredData.accounts.reduce((sum, account) => {
                            const val = account.valuations[weekIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);

                          // 전월 마지막 주 찾기
                          let prevMonthEndIdx = -1;
                          for (let i = weekIdx - 1; i >= 0; i--) {
                            const prevDate = new Date(filteredData.weeks[i].reference_date);
                            const prevYearMonth = `${prevDate.getFullYear()}-${String(prevDate.getMonth() + 1).padStart(2, '0')}`;
                            
                            if (prevYearMonth !== currentYearMonth) {
                              prevMonthEndIdx = i;
                              break;
                            }
                          }

                          if (prevMonthEndIdx === -1) {
                            return (
                              <td key={week.weekly_snapshot_id} style={{ textAlign: 'right' }}>
                                -
                              </td>
                            );
                          }

                          // 전월 마지막 주의 총액
                          const prevMonthTotal = filteredData.accounts.reduce((sum, account) => {
                            const val = account.valuations[prevMonthEndIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);

                          if (prevMonthTotal === 0) {
                            return (
                              <td key={week.weekly_snapshot_id} style={{ textAlign: 'right' }}>
                                -
                              </td>
                            );
                          }

                          const changePercent = ((currentTotal - prevMonthTotal) / prevMonthTotal) * 100;
                          let changeColor = 'black';
                          
                          if (changePercent >= 1) {
                            changeColor = '#d32f2f'; // Red
                          } else if (changePercent <= -1) {
                            changeColor = '#1976d2'; // Blue
                          }

                          return (
                            <td
                              key={week.weekly_snapshot_id}
                              style={{
                                textAlign: 'right',
                                color: changeColor,
                              }}
                            >
                              {changePercent >= 0 ? '+' : ''}{changePercent.toFixed(2)}%
                            </td>
                          );
                        })}
                      </tr>
                    </>
                  )}
                </tbody>
              </table>
            </div>
            </>
              );
            })()
          ) : (
            <div className={styles.infoBox}>
              <p>{weeklyReportYear}년의 주간 스냅샷이 없습니다.</p>
            </div>
          )}
        </div>
      )}

      {/* Annual Report Tab */}
      {activeTab === 'annualReport' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>연간 보고서 (Pivot)</h2>
          </div>

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : annualReportData && annualReportData.weeks.length > 0 ? (
            <>
              {/* 상단 스크롤바 */}
              <div
                ref={annualReportTopScrollRef}
                style={{
                  overflowX: 'auto',
                  overflowY: 'hidden',
                  marginBottom: '10px',
                }}
                onScroll={(e) => {
                  if (annualReportBottomScrollRef.current) {
                    annualReportBottomScrollRef.current.scrollLeft = e.currentTarget.scrollLeft;
                  }
                }}
              >
                <div style={{ width: `${annualReportScrollWidth}px`, height: '1px' }} />
              </div>

              {/* 메인 테이블 */}
              <div
                ref={annualReportBottomScrollRef}
                className={styles.tableWrapperAuto}
                onScroll={(e) => {
                  if (annualReportTopScrollRef.current) {
                    annualReportTopScrollRef.current.scrollLeft = e.currentTarget.scrollLeft;
                  }
                }}
              >
                <table className={styles.table} style={{ minWidth: '800px' }}>
                <thead style={{ position: 'sticky', top: 0, zIndex: 10, backgroundColor: '#fff' }}>
                  <tr>
                    <th style={{ position: 'sticky', left: 0, backgroundColor: '#fff', zIndex: 11, width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                      금융기관
                    </th>
                    <th style={{ position: 'sticky', left: '160px', backgroundColor: '#fff', zIndex: 11, width: '260px', minWidth: '260px' }}>
                      계좌
                    </th>
                    {annualReportData.weeks.map((yearPoint) => (
                      <th key={yearPoint.weekly_snapshot_id} style={{ backgroundColor: '#fff', minWidth: '100px', fontSize: '11px', padding: '6px 4px', textAlign: 'center' }}>
                        {yearPoint.week_number === 999
                          ? `${new Date(yearPoint.reference_date).getFullYear()}년`
                          : `${new Date(yearPoint.reference_date).getFullYear() - 1}년`}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {annualReportData.account_groups && annualReportData.account_groups.length > 0 && (
                    <>
                      <tr style={{ borderBottom: '2px solid #ccc' }}>
                        <td colSpan={annualReportData.weeks.length + 2} style={{ padding: '10px 8px', backgroundColor: '#f5f5f5', fontWeight: 'bold', textAlign: 'center' }}>
                          계좌 그룹
                        </td>
                      </tr>
                      {[...annualReportData.account_groups].sort((a, b) => a.display_order - b.display_order).map((group) => (
                        <tr key={group.account_group_id} style={{ backgroundColor: '#fffacd' }}>
                          <td style={{ position: 'sticky', left: 0, backgroundColor: '#fffacd', zIndex: 1, fontWeight: 'bold', width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                            {group.account_group_name}
                          </td>
                          <td style={{ position: 'sticky', left: '160px', backgroundColor: '#fffacd', zIndex: 1, fontSize: '11px', color: '#666', width: '260px', minWidth: '260px' }}>
                            (합계)
                          </td>
                          {group.valuations.map((val, idx) => (
                            <td key={idx} style={{ textAlign: 'right', fontWeight: 'bold' }}>
                              {val.amount > 0
                                ? val.amount.toLocaleString('ko-KR', {
                                    minimumFractionDigits: 0,
                                    maximumFractionDigits: 0,
                                  })
                                : '-'}
                            </td>
                          ))}
                        </tr>
                      ))}
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#ffeb99' }}>
                        <td style={{ position: 'sticky', left: 0, backgroundColor: '#ffeb99', zIndex: 1, width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                          총합
                        </td>
                        <td style={{ position: 'sticky', left: '160px', backgroundColor: '#ffeb99', zIndex: 1, width: '260px', minWidth: '260px' }}>
                        </td>
                        {annualReportData.weeks.map((yearPoint, yearIdx) => {
                          const total = annualReportData.accounts.reduce((sum, account) => {
                            const val = account.valuations[yearIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);
                          return (
                            <td key={yearPoint.weekly_snapshot_id} style={{ textAlign: 'right' }}>
                              {total > 0
                                ? total.toLocaleString('ko-KR', {
                                    minimumFractionDigits: 0,
                                    maximumFractionDigits: 0,
                                  })
                                : '-'}
                            </td>
                          );
                        })}
                      </tr>
                      <tr style={{ borderTop: '2px solid #ccc', borderBottom: '2px solid #ccc' }}>
                        <td colSpan={annualReportData.weeks.length + 2} style={{ padding: '10px 8px', backgroundColor: '#f5f5f5', fontWeight: 'bold', textAlign: 'center' }}>
                          전체 계좌
                        </td>
                      </tr>
                    </>
                  )}

                  {annualReportData.accounts.map((account) => (
                    <tr key={account.account_id}>
                      <td style={{ position: 'sticky', left: 0, backgroundColor: '#fff', zIndex: 1, width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                        {account.institution_name}
                      </td>
                      <td style={{ position: 'sticky', left: '160px', backgroundColor: '#fff', zIndex: 1, width: '260px', minWidth: '260px' }}>
                        {account.account_name}
                      </td>
                      {account.valuations.map((val, idx) => (
                        <td key={idx} style={{ textAlign: 'right' }}>
                          {val.amount > 0
                            ? val.amount.toLocaleString('ko-KR', {
                                minimumFractionDigits: 0,
                                maximumFractionDigits: 0,
                              })
                            : '-'}
                        </td>
                      ))}
                    </tr>
                  ))}

                  {annualReportData.accounts.length > 0 && (
                    <>
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#f0f0f0' }}>
                        <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#f0f0f0', zIndex: 1, width: '420px', minWidth: '420px' }}>
                          총합
                        </td>
                        {annualReportData.weeks.map((yearPoint, yearIdx) => {
                          const total = annualReportData.accounts.reduce((sum, account) => {
                            const val = account.valuations[yearIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);
                          return (
                            <td key={yearPoint.weekly_snapshot_id} style={{ textAlign: 'right' }}>
                              {total > 0
                                ? total.toLocaleString('ko-KR', {
                                    minimumFractionDigits: 0,
                                    maximumFractionDigits: 0,
                                  })
                                : '-'}
                            </td>
                          );
                        })}
                      </tr>
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#fff0f0' }}>
                        <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#fff0f0', zIndex: 1 }}>
                          전년 대비 금액
                        </td>
                        {annualReportData.weeks.map((yearPoint, yearIdx) => {
                          const currentTotal = annualReportData.accounts.reduce((sum, account) => {
                            const val = account.valuations[yearIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);

                          let changeAmount = 0;
                          let changeColor = 'black';

                          if (yearIdx > 0) {
                            const prevTotal = annualReportData.accounts.reduce((sum, account) => {
                              const val = account.valuations[yearIdx - 1];
                              return sum + (val ? val.amount : 0);
                            }, 0);
                            changeAmount = currentTotal - prevTotal;
                            if (changeAmount >= 1) {
                              changeColor = '#d32f2f';
                            } else if (changeAmount <= -1) {
                              changeColor = '#1976d2';
                            }
                          }

                          return (
                            <td
                              key={yearPoint.weekly_snapshot_id}
                              style={{
                                textAlign: 'right',
                                color: changeColor,
                              }}
                            >
                              {yearIdx > 0
                                ? (changeAmount >= 0 ? '+' : '') + changeAmount.toLocaleString('ko-KR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
                                : '-'}
                            </td>
                          );
                        })}
                      </tr>
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#fff5f5' }}>
                        <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#fff5f5', zIndex: 1 }}>
                          전년 대비 변화
                        </td>
                        {annualReportData.weeks.map((yearPoint, yearIdx) => {
                          const currentTotal = annualReportData.accounts.reduce((sum, account) => {
                            const val = account.valuations[yearIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);

                          let changePercent = 0;
                          let changeColor = 'black';

                          if (yearIdx > 0) {
                            const prevTotal = annualReportData.accounts.reduce((sum, account) => {
                              const val = account.valuations[yearIdx - 1];
                              return sum + (val ? val.amount : 0);
                            }, 0);

                            if (prevTotal > 0) {
                              changePercent = ((currentTotal - prevTotal) / prevTotal) * 100;

                              if (changePercent >= 1) {
                                changeColor = '#d32f2f';
                              } else if (changePercent <= -1) {
                                changeColor = '#1976d2';
                              }
                            }
                          }

                          return (
                            <td
                              key={yearPoint.weekly_snapshot_id}
                              style={{
                                textAlign: 'right',
                                color: changeColor,
                              }}
                            >
                              {yearIdx > 0 ? changePercent.toFixed(2) + '%' : '-'}
                            </td>
                          );
                        })}
                      </tr>
                      {/* 자산유형별 합계 섹션 */}
                      {annualReportData.asset_classes && annualReportData.asset_classes.length > 0 && (
                        <>
                          <tr style={{ borderBottom: '2px solid #ccc' }}>
                            <td colSpan={annualReportData.weeks.length + 2} style={{ padding: '10px 8px', backgroundColor: '#f5f5f5', fontWeight: 'bold', textAlign: 'center' }}>
                              자산유형별 합계
                            </td>
                          </tr>
                          {annualReportData.asset_classes.map((assetClass) => (
                            <tr key={assetClass.asset_class}>
                              <td style={{ position: 'sticky', left: 0, backgroundColor: '#f9f9f9', zIndex: 1, fontWeight: 'bold', width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                                {assetClass.asset_class}
                              </td>
                              <td style={{ position: 'sticky', left: '160px', backgroundColor: '#f9f9f9', zIndex: 1, fontSize: '11px', color: '#666', width: '260px', minWidth: '260px' }}>
                                (합계)
                              </td>
                              {assetClass.valuations.map((val, idx) => (
                                <td key={idx} style={{ textAlign: 'right', fontWeight: 'bold' }}>
                                  {val.amount > 0
                                    ? val.amount.toLocaleString('ko-KR', {
                                        minimumFractionDigits: 0,
                                        maximumFractionDigits: 0,
                                      })
                                    : '-'}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </>
                      )}
                      {/* 연간 MDD 행 */}
                      {annualReportData.mdd_by_year && annualReportData.mdd_by_year.length > 0 && (
                        <>
                          <tr style={{ borderBottom: '2px solid #ccc' }}>
                            <td colSpan={annualReportData.weeks.length + 2} style={{ padding: '10px 8px', backgroundColor: '#f5f5f5', fontWeight: 'bold', textAlign: 'center' }}>
                              연간 MDD
                            </td>
                          </tr>
                          <tr style={{ fontWeight: 'bold', backgroundColor: '#f0f4ff' }}>

                            <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#f0f4ff', zIndex: 1 }}>
                              MDD (%)
                            </td>
                            {annualReportData.weeks.map((yearPoint) => {
                              const mddItem = annualReportData.mdd_by_year!.find(
                                (m) => m.annual_snapshot_id === yearPoint.weekly_snapshot_id
                              );
                              const hasData = mddItem && mddItem.weekly_snapshot_count >= 2;
                              const mddPct = hasData ? mddItem!.mdd_percentage : null;
                              const mddColor = mddPct !== null && mddPct < -0.01 ? '#1976d2' : 'inherit';
                              return (
                                <td
                                  key={yearPoint.weekly_snapshot_id}
                                  style={{ textAlign: 'right', color: mddColor }}
                                  title={hasData ? `최고: ${mddItem!.peak_amount.toLocaleString('ko-KR', { maximumFractionDigits: 0 })}\n최저: ${mddItem!.trough_amount.toLocaleString('ko-KR', { maximumFractionDigits: 0 })}\n주간 스냅샷 수: ${mddItem!.weekly_snapshot_count}` : ''}
                                >
                                  {mddPct !== null ? mddPct.toFixed(2) + '%' : '-'}
                                </td>
                              );
                            })}
                          </tr>
                          <tr style={{ fontWeight: 'bold', backgroundColor: '#f0f4ff' }}>
                            <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#f0f4ff', zIndex: 1 }}>
                              MDD 최고금액
                            </td>
                            {annualReportData.weeks.map((yearPoint) => {
                              const mddItem = annualReportData.mdd_by_year!.find(
                                (m) => m.annual_snapshot_id === yearPoint.weekly_snapshot_id
                              );
                              const hasData = mddItem && mddItem.weekly_snapshot_count >= 2 && mddItem.peak_amount > 0;
                              return (
                                <td key={yearPoint.weekly_snapshot_id} style={{ textAlign: 'right' }}>
                                  {hasData ? mddItem!.peak_amount.toLocaleString('ko-KR', { maximumFractionDigits: 0 }) : '-'}
                                </td>
                              );
                            })}
                          </tr>
                          <tr style={{ fontWeight: 'bold', backgroundColor: '#f0f4ff' }}>
                            <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#f0f4ff', zIndex: 1 }}>
                              MDD 최저금액
                            </td>
                            {annualReportData.weeks.map((yearPoint) => {
                              const mddItem = annualReportData.mdd_by_year!.find(
                                (m) => m.annual_snapshot_id === yearPoint.weekly_snapshot_id
                              );
                              const hasData = mddItem && mddItem.weekly_snapshot_count >= 2 && mddItem.trough_amount > 0;
                              return (
                                <td key={yearPoint.weekly_snapshot_id} style={{ textAlign: 'right' }}>
                                  {hasData ? mddItem!.trough_amount.toLocaleString('ko-KR', { maximumFractionDigits: 0 }) : '-'}
                                </td>
                              );
                            })}
                          </tr>
                        </>
                      )}
                    </>
                  )}
                </tbody>
              </table>
            </div>
            </>
          ) : (
            <div className={styles.infoBox}>
              <p>연간 스냅샷 데이터가 없습니다.</p>
            </div>
          )}
        </div>
      )}

      {/* Snapshot Analysis Tab */}
      {activeTab === 'snapshotAnalysis' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>스냅샷 분석</h2>
          </div>

          {(() => {
            // 가장 최근 일일 스냅샷 찾기 (snapshots 배열은 모두 일일 스냅샷)
            const latestSnapshot = snapshots
              .sort((a, b) => new Date(b.reference_date).getTime() - new Date(a.reference_date).getTime())[0];

            if (!latestSnapshot) {
              return (
                <div className={styles.infoBox}>
                  <p>조회할 일일 스냅샷이 없습니다.</p>
                </div>
              );
            }

            // 해당 스냅샷의 모든 holdings
            const latestHoldings = snapshotHoldings.filter(
              (sh) => sh.snapshot_id === latestSnapshot.snapshot_id
            );

            if (latestHoldings.length === 0) {
              return (
                <div className={styles.infoBox}>
                  <p>해당 스냅샷에 보유자산이 없습니다.</p>
                </div>
              );
            }

            // 자산 유형별 합계 계산
            const assetClassMap = new Map<string, number>();
            latestHoldings.forEach((snapshotHolding) => {
              const holding = holdings.find((h) => h.holding_id === snapshotHolding.holding_id);
              const product = holding ? products.find((p) => p.product_id === holding.product_id) : undefined;
              const assetClass = product?.asset_class || '미분류';
              const amount = Number(snapshotHolding.valuation_amount || 0);
              assetClassMap.set(assetClass, (assetClassMap.get(assetClass) || 0) + amount);
            });

            const chartData = Array.from(assetClassMap.entries())
              .map(([name, value]) => ({
                name,
                value,
              }))
              .sort((a, b) => b.value - a.value);

            const filteredDetailHoldings = snapshotAnalysisAccountGroupFilter === null
              ? latestHoldings
              : latestHoldings.filter((snapshotHolding) => {
                  const holding = holdings.find((item) => item.holding_id === snapshotHolding.holding_id);
                  if (!holding) {
                    return false;
                  }

                  const selectedGroup = sortedAccountGroups.find(
                    (group) => group.account_group_id === snapshotAnalysisAccountGroupFilter
                  );

                  return selectedGroup?.account_ids.includes(holding.account_id) ?? false;
                });

            const detailAssetClassMap = new Map<string, number>();
            filteredDetailHoldings.forEach((snapshotHolding) => {
              const holding = holdings.find((item) => item.holding_id === snapshotHolding.holding_id);
              const product = holding ? products.find((item) => item.product_id === holding.product_id) : undefined;
              const assetClass = product?.asset_class || '미분류';
              const amount = Number(snapshotHolding.valuation_amount || 0);
              detailAssetClassMap.set(assetClass, (detailAssetClassMap.get(assetClass) || 0) + amount);
            });

            const detailAssetClassCandidates = [
              ...ASSET_CLASS_ORDER,
              ...Object.keys(assetClassTargets),
              ...chartData.map((item) => item.name),
              ...Array.from(detailAssetClassMap.keys()),
            ];

            const detailAssetClassNames = Array.from(new Set(detailAssetClassCandidates));
            const detailChartData = detailAssetClassNames
              .map((name) => ({
                name,
                value: detailAssetClassMap.get(name) || 0,
              }))
              .sort((a, b) => {
                const aOrder = ASSET_CLASS_ORDER.indexOf(a.name);
                const bOrder = ASSET_CLASS_ORDER.indexOf(b.name);

                if (aOrder !== -1 || bOrder !== -1) {
                  if (aOrder === -1) {
                    return 1;
                  }
                  if (bOrder === -1) {
                    return -1;
                  }
                  return aOrder - bOrder;
                }

                return a.name.localeCompare(b.name, 'ko');
              });

            const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF6B6B'];

            const totalValue = chartData.reduce((sum, item) => sum + item.value, 0);
            const detailTotalValue = detailChartData.reduce((sum, item) => sum + item.value, 0);

            // 커스텀 Legend 컴포넌트 (비중 순서 유지)
            const CustomPieLegend = (props: any) => {
              const { payload } = props;
              
              // chartData의 순서(비중 순)를 유지
              const orderedPayload = chartData.map((item) => {
                const entry = payload.find((p: any) => p.value === item.name);
                return entry;
              }).filter(Boolean);

              return (
                <div style={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap', marginTop: '10px' }}>
                  {orderedPayload.map((entry: any, index: number) => (
                    <div key={`legend-${index}`} style={{ display: 'flex', alignItems: 'center', marginRight: '20px', marginBottom: '5px' }}>
                      <div style={{ width: '14px', height: '14px', backgroundColor: entry.color, marginRight: '5px' }}></div>
                      <span style={{ fontSize: '14px' }}>{entry.value}</span>
                    </div>
                  ))}
                </div>
              );
            };

            return (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <div style={{ backgroundColor: '#f5f5f5', padding: '15px', borderRadius: '5px' }}>
                  <p style={{ margin: '0 0 10px 0' }}>
                    <strong>기준일:</strong> {latestSnapshot.reference_date}
                  </p>
                  <p style={{ margin: '0' }}>
                    <strong>총 평가금액:</strong> {totalValue.toLocaleString('ko-KR', { minimumFractionDigits: 0 })} 원
                  </p>
                </div>

                {/* 원그래프와 표를 가로로 배치 */}
                <div style={{ display: 'flex', gap: '40px', alignItems: 'flex-start' }}>
                  {/* 원그래프 */}
                  <div style={{ flex: '0 0 750px' }}>
                    <ResponsiveContainer width="100%" height={600}>
                      <PieChart>
                        <Pie
                          data={chartData}
                          cx="50%"
                          cy="50%"
                          outerRadius={180}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip
                          formatter={(value) => {
                            const amount = value ?? 0;
                            const percentage = totalValue > 0 ? ((amount as number) / totalValue * 100).toFixed(2) : '0.00';
                            return `${percentage}%`;
                          }}
                        />
                        <Legend content={CustomPieLegend} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>

                  {/* 자산 유형별 상세 표 */}
                  <div style={{ flex: '1', minWidth: '300px' }}>
                    <div className={styles.filterRow} style={{ justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                      <h3 style={{ margin: 0 }}>자산 유형별 상세</h3>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                        <label htmlFor="snapshot-analysis-account-group-filter">계좌그룹</label>
                        <select
                          id="snapshot-analysis-account-group-filter"
                          value={snapshotAnalysisAccountGroupFilter ?? ''}
                          onChange={(e) =>
                            setSnapshotAnalysisAccountGroupFilter(
                              e.target.value ? Number(e.target.value) : null
                            )
                          }
                        >
                          <option value="">전체</option>
                          {sortedAccountGroups.map((group) => (
                            <option key={group.account_group_id} value={group.account_group_id}>
                              {group.name}
                            </option>
                          ))}
                        </select>
                      </div>
                    </div>
                    {(() => {
                      const targetsByAssetClass = assetClassTargets; // targetAllocations에서 가져온 데이터

                      return (
                        <table className={styles.table}>
                          <thead>
                            <tr>
                              <th>자산 유형</th>
                              <th style={{ textAlign: 'right' }}>금액</th>
                              <th style={{ textAlign: 'right' }}>비중</th>
                              <th style={{ textAlign: 'right' }}>목표</th>
                            </tr>
                          </thead>
                          <tbody>
                            {detailChartData.map((item, idx) => {
                              const targetPercentage = targetsByAssetClass[item.name];
                              const currentPercentage = detailTotalValue > 0
                                ? ((item.value / detailTotalValue) * 100).toFixed(2)
                                : '0.00';
                              return (
                                <tr key={idx}>
                                  <td>{item.name}</td>
                                  <td style={{ textAlign: 'right' }}>
                                    {item.value.toLocaleString('ko-KR', { minimumFractionDigits: 0 })} 원
                                  </td>
                                  <td style={{ textAlign: 'right' }}>
                                    {currentPercentage}%
                                  </td>
                                  <td style={{ textAlign: 'right' }}>
                                    {targetPercentage ? `${targetPercentage}%` : '-'}
                                  </td>
                                </tr>
                              );
                            })}
                            <tr style={{ fontWeight: 'bold', backgroundColor: '#f5f5f5' }}>
                              <td>합계</td>
                              <td style={{ textAlign: 'right' }}>
                                {detailTotalValue.toLocaleString('ko-KR', { minimumFractionDigits: 0 })} 원
                              </td>
                              <td style={{ textAlign: 'right' }}>100.00%</td>
                              <td style={{ textAlign: 'right' }}>
                                {(() => {
                                  const totalTarget = Object.values(targetsByAssetClass)
                                    .filter(v => v)
                                    .reduce((sum, v) => sum + parseFloat(v), 0);
                                  return totalTarget > 0 ? `${totalTarget.toFixed(2)}%` : '-';
                                })()}
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      );
                    })()}
                  </div>
                </div>
              </div>
            );
          })()}

          {/* 오늘 기준 목표자산배분 비교 */}
          {(() => {
            const currentYearForToday = new Date().getFullYear();
            const latestCurrentYearSnapshot = sortedSnapshots.find(
              (snapshot) =>
                new Date(snapshot.reference_date).getFullYear() === currentYearForToday
            );

            if (!latestCurrentYearSnapshot) {
              return null;
            }

            const accountToGroupIds = new Map<number, number[]>();
            sortedAccountGroups.forEach((group) => {
              group.account_ids.forEach((accountId) => {
                const existing = accountToGroupIds.get(accountId) ?? [];
                existing.push(group.account_group_id);
                accountToGroupIds.set(accountId, existing);
              });
            });

            const targetMap = new Map<number, number>();
            todayAccountTargetAllocations.forEach((target) => {
              const amount = Number(target.target_amount);
              if (!Number.isFinite(amount)) {
                return;
              }
              const groupIds = accountToGroupIds.get(target.account_id) ?? [];
              groupIds.forEach((groupId) => {
                targetMap.set(groupId, (targetMap.get(groupId) ?? 0) + amount);
              });
            });

            const holdingToAccountId = new Map<number, number>();
            holdings
              .filter((holding) => !holding.deleted_at)
              .forEach((holding) => {
                holdingToAccountId.set(holding.holding_id, holding.account_id);
              });

            const actualMap = new Map<number, number>();
            snapshotHoldings
              .filter(
                (snapshotHolding) =>
                  snapshotHolding.snapshot_id === latestCurrentYearSnapshot.snapshot_id
              )
              .forEach((snapshotHolding) => {
                const accountId = holdingToAccountId.get(snapshotHolding.holding_id);
                if (accountId == null) {
                  return;
                }
                const groupIds = accountToGroupIds.get(accountId) ?? [];
                if (groupIds.length === 0) {
                  return;
                }
                const amount = Number(snapshotHolding.valuation_amount);
                if (!Number.isFinite(amount)) {
                  return;
                }
                groupIds.forEach((groupId) => {
                  actualMap.set(groupId, (actualMap.get(groupId) ?? 0) + amount);
                });
              });

            const mappedChartData = sortedAccountGroups
              .map((group) => {
                const targetAmount = targetMap.get(group.account_group_id) ?? 0;
                const actualAmount = actualMap.get(group.account_group_id) ?? 0;
                const achievementRate =
                  targetAmount > 0 ? (actualAmount / targetAmount) * 100 : 0;
                return {
                  그룹: group.name,
                  목표금액: targetAmount,
                  실제금액: actualAmount,
                  달성률: achievementRate,
                };
              })
              .filter((item) => item.목표금액 > 0 || item.실제금액 > 0);

            // 전체 합계 계산
            const totalTarget = Array.from(targetMap.values()).reduce((sum, val) => sum + val, 0);
            const totalActual = Array.from(actualMap.values()).reduce((sum, val) => sum + val, 0);
            const totalAchievementRate = totalTarget > 0 ? (totalActual / totalTarget) * 100 : 0;

            // 전체 합계 행 추가
            const chartData = [
              ...mappedChartData,
              {
                그룹: '전체 합계',
                목표금액: totalTarget,
                실제금액: totalActual,
                달성률: totalAchievementRate,
              },
            ];

            if (chartData.length === 0) {
              return null;
            }

            return (
              <div style={{ marginTop: '40px' }}>
                <h2>오늘 기준 목표자산배분 달성 현황</h2>
                <p style={{ marginTop: '8px', color: '#666' }}>
                  기준일: {latestCurrentYearSnapshot.reference_date}
                </p>
                <ResponsiveContainer width="100%" height={320}>
                  <ComposedChart data={chartData} margin={{ top: 8, right: 8, bottom: 8, left: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="그룹" />
                    <YAxis
                      yAxisId="left"
                      width={96}
                      tickFormatter={(value) =>
                        formatToEokLabel(Number(value))
                      }
                      tickMargin={8}
                      label={{
                        value: '평가금액 (억원)',
                        angle: -90,
                        position: 'insideLeft',
                        dx: 6,
                        style: { fill: '#4b5563', fontSize: 12, fontWeight: 600 },
                      }}
                    />
                    <YAxis
                      yAxisId="right"
                      orientation="right"
                      tickFormatter={(value) => `${Number(value).toFixed(0)}%`}
                      tickMargin={8}
                      label={{
                        value: '달성률 (%)',
                        angle: 90,
                        position: 'insideRight',
                        dx: -10,
                        style: { fill: '#4b5563', fontSize: 12, fontWeight: 600 },
                      }}
                    />
                    <Tooltip
                      formatter={(value: number | string | undefined, name: string | undefined) => {
                        const numericValue = Number(value ?? 0);
                        const label = name ?? '';
                        if (label === '달성률') {
                          return [`${numericValue.toFixed(2)}%`, label];
                        }
                        return [
                          numericValue.toLocaleString('ko-KR', {
                            minimumFractionDigits: 0,
                            maximumFractionDigits: 0,
                          }),
                          label,
                        ];
                      }}
                    />
                    <Legend />
                    <Bar yAxisId="left" dataKey="목표금액" />
                    <Bar yAxisId="left" dataKey="실제금액" />
                    <Line yAxisId="right" type="monotone" dataKey="달성률" />
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
            );
          })()}

          {/* 연간 평가금액 추이 */}
          {(() => {
            if (annualSnapshots.length === 0) {
              return null;
            }

            // 각 연도별 데이터 준비
            const yearDataMap = new Map<string, { year: string; total: number; [key: string]: number | string }>();
            
            // annualSnapshots를 연도 기준으로 처리
            annualSnapshots.forEach((snap) => {
              const year = String(Number(snap.reference_date.substring(0, 4)) - 1); // 연간 스냅샷 연도 -1
              
              if (!yearDataMap.has(year)) {
                yearDataMap.set(year, { year, total: 0 });
              }
              
              const yearData = yearDataMap.get(year)!;
              
              // 이 연도의 annualSnapshotHoldings에서 같은 의존성으로 데이터 찾기
              // (실제로는 API에서 각 스냅샷별 데이터가 필요함)
              // 현재 데이터 한계로 annualSnapshotHoldings를 사용
            });

            // 실제 annualSnapshotHoldings를 이용해 연도별 계좌그룹별 합계 계산
            const yearAccountGroupMap = new Map<string, Map<string, number>>();
            
            annualSnapshotHoldings.forEach((holding) => {
              // holding이 어느 연도의 스냅샷인지 알 수 없으므로, 
              // annualSnapshots의 reference_date를 기반으로 추론
              const relatedSnapshot = annualSnapshots.find(
                (s) => s.annual_snapshot_id === holding.annual_snapshot_id
              );
              
              if (!relatedSnapshot) return;
              
              const year = String(Number(relatedSnapshot.reference_date.substring(0, 4)) - 1); // 연간 스냅샷 연도 -1
              
              // account_id로 계좌그룹 찾기
              const accountGroup = accountGroups.find((ag) =>
                ag.account_ids.includes(holding.account_id)
              );
              const accountGroupName = accountGroup?.name || '미분류';
              
              const amount = Number(holding.valuation_amount || 0);
              
              if (!yearAccountGroupMap.has(year)) {
                yearAccountGroupMap.set(year, new Map());
              }
              
              const groupMap = yearAccountGroupMap.get(year)!;
              groupMap.set(accountGroupName, (groupMap.get(accountGroupName) || 0) + amount);
            });

            // 최신 일간 스냅샷 (당일) 데이터 추가
            const latestDailySnapshot = snapshots
              .sort((a, b) => new Date(b.reference_date).getTime() - new Date(a.reference_date).getTime())[0];
            
            if (latestDailySnapshot) {
              const currentYear = String(new Date(latestDailySnapshot.reference_date).getFullYear());
              const latestDailyHoldings = snapshotHoldings.filter(
                (sh) => sh.snapshot_id === latestDailySnapshot.snapshot_id
              );
              
              if (!yearAccountGroupMap.has(currentYear)) {
                yearAccountGroupMap.set(currentYear, new Map());
              }
              const latestYearGroupMap = yearAccountGroupMap.get(currentYear)!;
              
              latestDailyHoldings.forEach((snapshotHolding) => {
                const holding = holdings.find((h) => h.holding_id === snapshotHolding.holding_id);
                if (!holding) return;
                
                const accountGroup = accountGroups.find((ag) =>
                  ag.account_ids.includes(holding.account_id)
                );
                const accountGroupName = accountGroup?.name || '미분류';
                const amount = Number(snapshotHolding.valuation_amount || 0);
                
                latestYearGroupMap.set(accountGroupName, (latestYearGroupMap.get(accountGroupName) || 0) + amount);
              });
            }

            // 차트 데이터 생성 (전체합계를 먼저 추가하여 Legend 순서 제어)
            const chartDataByYear = Array.from(yearAccountGroupMap.entries())
              .map(([year, accountGroupMap]) => {
                const yearObj: any = { year };
                let total = 0;
                
                // 먼저 합계 계산
                accountGroupMap.forEach((amount) => {
                  total += amount;
                });
                
                // 전체합계를 먼저 추가
                yearObj.전체합계 = total;
                
                // 그 다음 계좌그룹별 금액 추가
                accountGroupMap.forEach((amount, accountGroup) => {
                  yearObj[accountGroup] = amount;
                });
                
                return yearObj;
              })
              .sort((a, b) => a.year.localeCompare(b.year));

            // 전년 대비 증가율 계산
            chartDataByYear.forEach((item, index) => {
              if (index > 0) {
                const prevTotal = chartDataByYear[index - 1].전체합계;
                const currentTotal = item.전체합계;
                if (prevTotal > 0) {
                  item.증가율 = ((currentTotal - prevTotal) / prevTotal) * 100;
                } else {
                  item.증가율 = 0;
                }
              } else {
                item.증가율 = null; // 첫 해는 증가율 없음
              }
            });

            if (chartDataByYear.length === 0) {
              return null;
            }

            // 계좌그룹 목록 추출 (중복 제거 및 정렬)
            const allAccountGroups = Array.from(
              new Set(
                chartDataByYear.flatMap((item) =>
                  Object.keys(item).filter((key) => key !== 'year' && key !== '전체합계' && key !== '증가율')
                )
              )
            ).sort();

            const lineColors = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#82CA9D', '#8884D8', '#FFC658', '#FF6B6B'];
            const logScaleSeriesThreshold = 100000000;
            const currentYear = String(new Date().getFullYear());
            const currentYearData = chartDataByYear.find((item) => item.year === currentYear);
            const visibleAccountGroups = snapshotAnalysisLogScale
              ? allAccountGroups.filter((group) =>
                  Number(currentYearData?.[group] ?? 0) > logScaleSeriesThreshold
                )
              : allAccountGroups;
            const amountKeys = ['전체합계', ...visibleAccountGroups];
            const amountChartData = snapshotAnalysisLogScale
              ? chartDataByYear.map((item) => {
                  const nextItem: Record<string, string | number | null> = { ...item };
                  amountKeys.forEach((key) => {
                    const rawValue = Number(nextItem[key]);
                    nextItem[key] = Number.isFinite(rawValue) && rawValue > 0 ? rawValue : null;
                  });
                  return nextItem;
                })
              : chartDataByYear;

            // 금액 차트용 커스텀 Tooltip 컴포넌트
            const CustomAmountTooltip = (props: any) => {
              const { active, payload, label } = props;
              
              if (!active || !payload || !payload.length) {
                return null;
              }

              // 전체합계를 먼저, 나머지는 알파벳순으로 정렬
              const orderedPayload = [
                ...payload.filter((entry: any) => entry.dataKey === '전체합계'),
                ...payload.filter((entry: any) => entry.dataKey !== '전체합계')
                  .sort((a: any, b: any) => a.dataKey.localeCompare(b.dataKey))
              ];

              return (
                <div style={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #ccc', 
                  padding: '10px',
                  borderRadius: '4px'
                }}>
                  <p style={{ margin: '0 0 5px 0', fontWeight: 'bold' }}>{`연도: ${label}`}</p>
                  {orderedPayload.map((entry: any, index: number) => (
                    <p key={`tooltip-${index}`} style={{ margin: '3px 0', color: entry.color }}>
                      {`${entry.dataKey}: ${(entry.value as number).toLocaleString('ko-KR', { minimumFractionDigits: 0 })} 원`}
                    </p>
                  ))}
                </div>
              );
            };

            // 증가율 차트용 커스텀 Tooltip 컴포넌트
            const CustomGrowthTooltip = (props: any) => {
              const { active, payload, label } = props;
              
              if (!active || !payload || !payload.length) {
                return null;
              }

              const growthRate = payload[0]?.value;

              return (
                <div style={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #ccc', 
                  padding: '10px',
                  borderRadius: '4px'
                }}>
                  <p style={{ margin: '0 0 5px 0', fontWeight: 'bold' }}>{`연도: ${label}`}</p>
                  {growthRate !== null && growthRate !== undefined && (
                    <p style={{ margin: '3px 0', color: '#82ca9d', fontWeight: 'bold' }}>
                      {`증가율: ${growthRate >= 0 ? '+' : ''}${growthRate.toFixed(2)}%`}
                    </p>
                  )}
                </div>
              );
            };

            // 금액 차트용 커스텀 Legend 컴포넌트
            const CustomAmountLegend = (props: any) => {
              const { payload } = props;
              
              // 전체합계를 먼저, 나머지는 알파벳순으로 정렬
              const orderedPayload = [
                ...payload.filter((entry: any) => entry.value === '전체합계'),
                ...payload.filter((entry: any) => entry.value !== '전체합계')
                  .sort((a: any, b: any) => a.value.localeCompare(b.value))
              ];

              return (
                <div style={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap', marginTop: '10px' }}>
                  {orderedPayload.map((entry: any, index: number) => (
                    <div key={`legend-${index}`} style={{ display: 'flex', alignItems: 'center', marginRight: '20px', marginBottom: '5px' }}>
                      <div style={{ width: '14px', height: '14px', backgroundColor: entry.color, marginRight: '5px' }}></div>
                      <span style={{ fontSize: '14px' }}>{entry.value}</span>
                    </div>
                  ))}
                </div>
              );
            };

            return (
              <div style={{ marginTop: '40px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
                  <h2 style={{ margin: 0 }}>연간 평가금액 추이</h2>
                  <button
                    type="button"
                    role="switch"
                    aria-checked={snapshotAnalysisLogScale}
                    aria-label="Y축 로그 스케일 전환"
                    onClick={() => setSnapshotAnalysisLogScale((prev) => !prev)}
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '8px',
                      border: `1px solid ${snapshotAnalysisLogScale ? '#60a5fa' : '#d1d5db'}`,
                      borderRadius: '999px',
                      padding: '6px 10px',
                      backgroundColor: snapshotAnalysisLogScale ? '#eff6ff' : '#ffffff',
                      color: '#1f2937',
                      fontSize: '14px',
                      cursor: 'pointer',
                    }}
                  >
                    <span
                      aria-hidden="true"
                      style={{
                        width: '40px',
                        height: '22px',
                        borderRadius: '999px',
                        backgroundColor: snapshotAnalysisLogScale ? '#2563eb' : '#d1d5db',
                        padding: '2px',
                        display: 'inline-flex',
                        alignItems: 'center',
                      }}
                    >
                      <span
                        style={{
                          width: '18px',
                          height: '18px',
                          borderRadius: '50%',
                          backgroundColor: '#ffffff',
                          boxShadow: '0 1px 2px rgba(0, 0, 0, 0.2)',
                          transform: snapshotAnalysisLogScale ? 'translateX(18px)' : 'translateX(0)',
                          transition: 'transform 0.2s ease',
                        }}
                      />
                    </span>
                    <span style={{ fontWeight: 500 }}>Y축 로그 스케일</span>
                    <span
                      aria-label="로그 스케일 표시 기준 안내"
                      title="로그 스케일에서는 올해 평가금액이 1억원을 넘지 않는 계좌그룹은 차트에서 제외됩니다."
                      style={{
                        width: '18px',
                        height: '18px',
                        borderRadius: '50%',
                        border: '1px solid #94a3b8',
                        color: '#475569',
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '12px',
                        fontWeight: 700,
                        lineHeight: 1,
                        cursor: 'help',
                        backgroundColor: '#f8fafc',
                      }}
                    >
                      i
                    </span>
                  </button>
                </div>
                
                {/* 평가금액 선그래프 */}
                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                  <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={amountChartData} margin={{ top: 8, right: 8, bottom: 8, left: 18 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="year" />
                      <YAxis 
                        scale={snapshotAnalysisLogScale ? 'log' : 'auto'}
                        domain={snapshotAnalysisLogScale ? ['auto', 'auto'] : [0, 'auto']}
                        allowDataOverflow={snapshotAnalysisLogScale}
                        width={100}
                        tickFormatter={(value) =>
                          formatToEokLabel(Number(value))
                        }
                        tickMargin={8}
                        label={{
                          value: snapshotAnalysisLogScale ? '평가금액 (억원, 로그)' : '평가금액 (억원)',
                          angle: -90,
                          position: 'insideLeft',
                          dx: -8,
                          style: { fill: '#4b5563', fontSize: 12, fontWeight: 600 },
                        }}
                      />
                      <Tooltip content={CustomAmountTooltip} />
                      <Legend content={CustomAmountLegend} />
                      {/* 전체 합계 라인 */}
                      <Line
                        type="monotone"
                        dataKey="전체합계"
                        stroke="#FF0000"
                        strokeWidth={3}
                        dot={{ fill: '#FF0000', r: 5 }}
                        activeDot={{ r: 7 }}
                        connectNulls={snapshotAnalysisLogScale}
                      />
                      {/* 계좌그룹별 라인 */}
                      {visibleAccountGroups.map((group) => {
                        const originalIndex = allAccountGroups.indexOf(group);
                        const lineColor = lineColors[originalIndex % lineColors.length];

                        return (
                          <Line
                            key={group}
                            type="monotone"
                            dataKey={group}
                            stroke={lineColor}
                            strokeWidth={2}
                            dot={{ fill: lineColor, r: 4 }}
                            activeDot={{ r: 6 }}
                            connectNulls={snapshotAnalysisLogScale}
                          />
                        );
                      })}
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                {/* 증가율 막대그래프 */}
                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '40px' }}>
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={chartDataByYear}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="year" />
                      <YAxis 
                        width={74}
                        tickFormatter={(value) => `${value.toFixed(0)}%`}
                        tickMargin={8}
                        label={{
                          value: '증가율 (%)',
                          angle: -90,
                          position: 'insideLeft',
                          dx: 10,
                          style: { fill: '#4b5563', fontSize: 12, fontWeight: 600 },
                        }}
                      />
                      <Tooltip content={CustomGrowthTooltip} />
                      <Bar
                        dataKey="증가율"
                        fill="#82ca9d"
                        barSize={50}
                        label={{
                          position: 'top',
                          formatter: (value: any) => {
                            if (value === null || value === undefined) return '';
                            const numValue = Number(value);
                            return `${numValue >= 0 ? '+' : ''}${numValue.toFixed(2)}%`;
                          },
                          style: { fontSize: '12px', fontWeight: 'bold' }
                        }}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* 주간 평가금액 추이 */}
                <div style={{ marginTop: '40px' }}>
                  <h2 style={{ margin: '0 0 14px 0' }}>주간 평가금액 추이</h2>

                  <div
                    style={{
                      display: 'flex',
                      flexWrap: 'wrap',
                      gap: '12px',
                      alignItems: 'flex-start',
                      marginBottom: '14px',
                    }}
                  >
                    <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '14px', color: '#374151', fontWeight: 600 }}>조회 구간</span>
                      <select
                        value={snapshotAnalysisWeeklyRange}
                        onChange={(e) => setSnapshotAnalysisWeeklyRange(e.target.value as SnapshotAnalysisWeeklyRange)}
                        style={{ padding: '6px 10px', border: '1px solid #d1d5db', borderRadius: '6px' }}
                      >
                        <option value="6m">6개월</option>
                        <option value="1y">1년</option>
                        <option value="2y">2년</option>
                        <option value="5y">5년</option>
                        <option value="all">전체</option>
                      </select>
                    </label>

                    <div
                      style={{
                        display: 'grid',
                        gridTemplateColumns: '130px minmax(230px, 1fr) minmax(230px, 1fr)',
                        columnGap: '12px',
                        rowGap: '10px',
                        alignItems: 'center',
                        flex: '1 1 760px',
                      }}
                    >
                      <label
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '6px',
                          fontSize: '14px',
                          color: '#111827',
                          fontWeight: 700,
                        }}
                      >
                        <input
                          type="checkbox"
                          checked
                          readOnly
                          disabled
                          style={{ opacity: 1 }}
                        />
                        기본 시리즈
                      </label>
                      <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ fontSize: '14px', color: '#374151', fontWeight: 600 }}>계좌</span>
                        <select
                          value={snapshotAnalysisWeeklyAccountFilter}
                          onChange={(e) => {
                            setSnapshotAnalysisWeeklyAccountFilter(e.target.value);
                            setSnapshotAnalysisWeeklyAssetFilter('all');
                          }}
                          style={{ padding: '6px 10px', border: '1px solid #d1d5db', borderRadius: '6px', minWidth: '200px', width: '100%' }}
                        >
                          <option value="all">전체 계좌</option>
                          {snapshotAnalysisWeeklyAccountOptions.map((account) => (
                            <option key={account.account_id} value={String(account.account_id)}>
                              {getSnapshotAnalysisAccountOptionLabel(account)}
                            </option>
                          ))}
                        </select>
                      </label>
                      <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ fontSize: '14px', color: '#374151', fontWeight: 600 }}>자산</span>
                        <select
                          value={snapshotAnalysisWeeklyAssetFilter}
                          onChange={(e) => setSnapshotAnalysisWeeklyAssetFilter(e.target.value)}
                          style={{ padding: '6px 10px', border: '1px solid #d1d5db', borderRadius: '6px', minWidth: '200px', width: '100%' }}
                        >
                          <option value="all">전체 자산</option>
                          {snapshotAnalysisWeeklyAssetOptions.map((product) => (
                            <option key={product.product_id} value={String(product.product_id)}>
                              {product.product_name}
                            </option>
                          ))}
                        </select>
                      </label>

                      <label style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '14px', color: '#374151', fontWeight: 600 }}>
                        <input
                          type="checkbox"
                          checked={snapshotAnalysisWeeklySecondSeriesEnabled}
                          onChange={(e) => setSnapshotAnalysisWeeklySecondSeriesEnabled(e.target.checked)}
                        />
                        2번째 시리즈
                      </label>
                      <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', opacity: snapshotAnalysisWeeklySecondSeriesEnabled ? 1 : 0.55 }}>
                        <span style={{ fontSize: '14px', color: '#374151', fontWeight: 600 }}>계좌</span>
                        <select
                          disabled={!snapshotAnalysisWeeklySecondSeriesEnabled}
                          value={snapshotAnalysisWeeklySecondAccountFilter}
                          onChange={(e) => {
                            setSnapshotAnalysisWeeklySecondAccountFilter(e.target.value);
                            setSnapshotAnalysisWeeklySecondAssetFilter('all');
                          }}
                          style={{ padding: '6px 10px', border: '1px solid #d1d5db', borderRadius: '6px', minWidth: '200px', width: '100%' }}
                        >
                          <option value="all">전체 계좌</option>
                          {snapshotAnalysisWeeklyAccountOptions.map((account) => (
                            <option key={account.account_id} value={String(account.account_id)}>
                              {getSnapshotAnalysisAccountOptionLabel(account)}
                            </option>
                          ))}
                        </select>
                      </label>
                      <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', opacity: snapshotAnalysisWeeklySecondSeriesEnabled ? 1 : 0.55 }}>
                        <span style={{ fontSize: '14px', color: '#374151', fontWeight: 600 }}>자산</span>
                        <select
                          disabled={!snapshotAnalysisWeeklySecondSeriesEnabled}
                          value={snapshotAnalysisWeeklySecondAssetFilter}
                          onChange={(e) => setSnapshotAnalysisWeeklySecondAssetFilter(e.target.value)}
                          style={{ padding: '6px 10px', border: '1px solid #d1d5db', borderRadius: '6px', minWidth: '200px', width: '100%' }}
                        >
                          <option value="all">전체 자산</option>
                          {snapshotAnalysisWeeklySecondAssetOptions.map((product) => (
                            <option key={product.product_id} value={String(product.product_id)}>
                              {product.product_name}
                            </option>
                          ))}
                        </select>
                      </label>
                    </div>
                  </div>

                  {snapshotAnalysisWeeklyChartData.length > 0 ? (
                    <>
                      <ResponsiveContainer width="100%" height={320}>
                        <LineChart
                          data={snapshotAnalysisWeeklyChartData}
                          margin={{ top: 8, right: 8, bottom: 8, left: 18 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="xLabel" minTickGap={24} />
                          <YAxis
                            width={100}
                            tickFormatter={(value) => formatToEokLabel(Number(value))}
                            tickMargin={8}
                            label={{
                              value: '평가금액 (억원)',
                              angle: -90,
                              position: 'insideLeft',
                              dx: -8,
                              style: { fill: '#4b5563', fontSize: 12, fontWeight: 600 },
                            }}
                          />
                          <Tooltip
                            formatter={(value: number | string | undefined, name: string | undefined) => {
                              const numericValue = Number(value ?? 0);
                              return [
                                numericValue.toLocaleString('ko-KR', {
                                  minimumFractionDigits: 0,
                                  maximumFractionDigits: 0,
                                }),
                                name ?? '평가금액',
                              ];
                            }}
                            labelFormatter={(_, payload) => {
                              const rawDate = payload?.[0]?.payload?.referenceDate;
                              return rawDate ? `기준일: ${rawDate}` : '';
                            }}
                          />
                          <Legend />
                          <Line
                            type="monotone"
                            dataKey="amountPrimary"
                            name={snapshotAnalysisPrimarySeriesLabel}
                            stroke="#2563eb"
                            strokeWidth={2}
                            dot={{ fill: '#2563eb', r: 2 }}
                            activeDot={{ r: 5 }}
                            isAnimationActive={false}
                          />
                          {snapshotAnalysisWeeklySecondSeriesEnabled && (
                            <Line
                              type="monotone"
                              dataKey="amountSecondary"
                              name={snapshotAnalysisSecondarySeriesLabel}
                              stroke="#f97316"
                              strokeWidth={2}
                              dot={{ fill: '#f97316', r: 2 }}
                              activeDot={{ r: 5 }}
                              isAnimationActive={false}
                            />
                          )}
                        </LineChart>
                      </ResponsiveContainer>
                    </>
                  ) : (
                    <p style={{ color: '#6b7280' }}>주간 시계열 데이터를 표시할 수 없습니다.</p>
                  )}
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* Target Allocations Tab */}
      {activeTab === 'targetAllocations' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>목표 자산배분</h2>
          </div>

          <div className={styles.form}>
            <label htmlFor="target-allocation-year">목표 연도</label>
            <select
              id="target-allocation-year"
              value={targetYear}
              onChange={(e) => setTargetYear(Number(e.target.value))}
            >
              {targetYearOptions.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>

          <div className={styles.infoBox}>
            <p>연도별·계좌별 목표 금액을 입력하면 계좌그룹 목표와 연간 총액 목표를 자동 추론합니다.</p>
            <p>저장 단위는 계좌이며, 집계표와 그래프는 계좌 목표의 합계로 계산됩니다.</p>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <button
              onClick={handleSaveAllAccountTargetAllocations}
              disabled={savingAllTargetAccounts}
              style={{
                padding: '8px 16px',
                backgroundColor: savingAllTargetAccounts ? '#ccc' : '#0066cc',
                color: '#fff',
                border: 'none',
                borderRadius: '4px',
                cursor: savingAllTargetAccounts ? 'not-allowed' : 'pointer',
                fontSize: '14px',
                fontWeight: 'bold',
              }}
            >
              {savingAllTargetAccounts ? '일괄저장 중...' : '모든 계좌 일괄저장'}
            </button>
          </div>

          <div className={styles.tableWrapper} style={{ overflowX: 'auto', marginTop: '16px' }}>
            <table className={styles.table} style={{ minWidth: '980px' }}>
              <thead>
                <tr>
                  <th>기관</th>
                  <th>계좌</th>
                  <th style={{ textAlign: 'right' }}>목표 입력</th>
                  <th style={{ textAlign: 'right' }}>저장된 목표</th>
                </tr>
              </thead>
              <tbody>
                {accountTargetInputRows.map((row) => (
                  <tr key={row.account.account_id}>
                    <td>{row.institutionName}</td>
                    <td>{row.account.name}</td>
                    <td style={{ textAlign: 'right' }}>
                      <input
                        type="text"
                        inputMode="decimal"
                        className={styles.amountInput}
                        value={row.draftAmount}
                        onChange={(e) =>
                          setTargetAccountDrafts((prev) => ({
                            ...prev,
                            [row.account.account_id]: e.target.value,
                          }))
                        }
                        onBlur={(e) => {
                          const formatted = formatTargetAmountInput(e.target.value);
                          if (formatted !== e.target.value) {
                            setTargetAccountDrafts((prev) => ({
                              ...prev,
                              [row.account.account_id]: formatted,
                            }));
                          }
                        }}
                        placeholder="목표 금액"
                      />
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      {row.existingTarget
                        ? Number(row.existingTarget.target_amount).toLocaleString('ko-KR', {
                            minimumFractionDigits: 0,
                            maximumFractionDigits: 0,
                          })
                        : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{ marginTop: '16px' }} className={styles.infoBox}>
            <p>연간 계좌 목표 합계: {totalTargetAmount.toLocaleString('ko-KR')}원</p>
            <p>연간 실제 자산 합계: {totalActualAmount.toLocaleString('ko-KR')}원</p>
            <p>
              전체 달성률: {totalAchievementRate == null ? '-' : `${totalAchievementRate.toFixed(2)}%`}
            </p>
          </div>

          {/* 계좌그룹 및 총액 목표 집계 섹션 */}
          <div style={{ marginBottom: '32px', marginTop: '16px' }}>
            <h3 style={{ marginTop: 0 }}>계좌그룹별 자동 집계</h3>

            {loading ? (
              <div className={styles.loading}>로딩 중...</div>
            ) : sortedAccountGroups.length === 0 ? (
              <div className={styles.infoBox}>
                <p>계좌그룹이 없습니다. 먼저 계좌그룹을 생성해주세요.</p>
              </div>
            ) : (
              <>
                <div className={styles.tableWrapper} style={{ overflowX: 'auto' }}>
                  <table className={styles.table} style={{ minWidth: '980px' }}>
                    <thead>
                      <tr>
                        <th>계좌그룹</th>
                        <th style={{ textAlign: 'right' }}>목표 (금액)</th>
                        <th style={{ textAlign: 'right' }}>목표 (%)</th>
                        <th style={{ textAlign: 'right' }}>실제금액</th>
                        <th style={{ textAlign: 'right' }}>차이(실제-목표)</th>
                        <th style={{ textAlign: 'right' }}>달성률</th>
                      </tr>
                    </thead>
                    <tbody>
                      {targetComparisonRows.map((row) => (
                        <tr key={row.accountGroupId}>
                          <td>{row.accountGroupName}</td>
                          <td style={{ textAlign: 'right' }}>
                            {row.targetAmount.toLocaleString('ko-KR', {
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                            })}
                          </td>
                          <td style={{ textAlign: 'right' }}>
                            {row.targetGrowthRate == null
                              ? '-'
                              : `${row.targetGrowthRate.toFixed(2)}%`}
                          </td>
                          <td style={{ textAlign: 'right' }}>
                            {row.actualAmount.toLocaleString('ko-KR', {
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                            })}
                          </td>
                          <td style={{ textAlign: 'right' }}>
                            {row.gapAmount.toLocaleString('ko-KR', {
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                            })}
                          </td>
                          <td style={{ textAlign: 'right' }}>
                            {row.achievementRate == null
                              ? '-'
                              : `${row.achievementRate.toFixed(2)}%`}
                          </td>
                        </tr>
                      ))}
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#e8f4f8' }}>
                        <td>전체 합계</td>
                        <td style={{ textAlign: 'right' }}>
                          {totalTargetAmount.toLocaleString('ko-KR', {
                            minimumFractionDigits: 0,
                            maximumFractionDigits: 0,
                          })}
                        </td>
                        <td style={{ textAlign: 'right' }}>
                          {totalTargetGrowthRate == null
                            ? '-'
                            : `${totalTargetGrowthRate.toFixed(2)}%`}
                        </td>
                        <td style={{ textAlign: 'right' }}>
                          {totalActualAmount.toLocaleString('ko-KR', {
                            minimumFractionDigits: 0,
                            maximumFractionDigits: 0,
                          })}
                        </td>
                        <td style={{ textAlign: 'right' }}>
                          {totalGapAmount.toLocaleString('ko-KR', {
                            minimumFractionDigits: 0,
                            maximumFractionDigits: 0,
                          })}
                        </td>
                        <td style={{ textAlign: 'right' }}>
                          {totalAchievementRate == null
                            ? '-'
                            : `${totalAchievementRate.toFixed(2)}%`}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                {useLatestDailySnapshotForActual && !latestDailySnapshotForTargetYear && (
                  <div className={styles.infoBox}>
                    <p>{targetYear}년 일일 스냅샷이 없어 실제금액/달성률은 0으로 표시됩니다.</p>
                  </div>
                )}

                {!useLatestDailySnapshotForActual && annualReportYearIndex < 0 && (
                  <div className={styles.infoBox}>
                    <p>{targetYear}년 실제금액 데이터(연간 보고서)가 없어 실제금액/달성률은 0으로 표시됩니다.</p>
                  </div>
                )}

                {targetComparisonChartData.length > 0 && (
                  <div style={{ marginTop: '24px' }}>
                    <h3>목표 대비 실제 비교</h3>
                    <ResponsiveContainer width="100%" height={320}>
                      <ComposedChart data={targetComparisonChartData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="그룹" />
                        <YAxis
                          yAxisId="left"
                          tickFormatter={(value) =>
                            Number(value).toLocaleString('ko-KR', {
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                            })
                          }
                        />
                        <YAxis
                          yAxisId="right"
                          orientation="right"
                          tickFormatter={(value) => `${Number(value).toFixed(0)}%`}
                        />
                        <Tooltip
                          formatter={(value: number | string | undefined, name: string | undefined) => {
                            const numericValue = Number(value ?? 0);
                            const label = name ?? '';
                            if (label === '달성률') {
                              return [`${numericValue.toFixed(2)}%`, label];
                            }
                            return [
                              numericValue.toLocaleString('ko-KR', {
                                minimumFractionDigits: 0,
                                maximumFractionDigits: 0,
                              }),
                              label,
                            ];
                          }}
                        />
                        <Legend />
                        <Bar yAxisId="left" dataKey="목표금액" />
                        <Bar yAxisId="left" dataKey="실제금액" />
                        <Line yAxisId="right" type="monotone" dataKey="달성률" />
                      </ComposedChart>
                    </ResponsiveContainer>
                  </div>
                )}

                {targetDistributionChartData.length > 0 && (
                  <div style={{ marginTop: '24px' }}>
                    <h3>계좌그룹별 목표 금액 분포</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={targetDistributionChartData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis
                          tickFormatter={(value) =>
                            Number(value).toLocaleString('ko-KR', {
                              minimumFractionDigits: 0,
                              maximumFractionDigits: 0,
                            })
                          }
                        />
                        <Tooltip
                          formatter={(value: number | string | undefined) => {
                            const numericValue = Number(value ?? 0);
                            return [
                              numericValue.toLocaleString('ko-KR', {
                                minimumFractionDigits: 0,
                                maximumFractionDigits: 0,
                              }),
                              '목표금액',
                            ];
                          }}
                        />
                        <Legend />
                        <Bar dataKey="value" name="목표금액" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </>
            )}
          </div>

          {/* 자산별 목표 % 입력 섹션 */}
          <div style={{ marginTop: '48px', paddingTop: '32px', borderTop: '2px solid #ddd' }}>
            <div className={styles.sectionHeader}>
              <h3 style={{ margin: 0 }}>자산별 목표 비율</h3>
              <button
                onClick={handleSaveAssetClassTargets}
                disabled={savingAssetClassTargets}
                style={{
                  padding: '8px 16px',
                  backgroundColor: savingAssetClassTargets ? '#ccc' : '#28a745',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: savingAssetClassTargets ? 'not-allowed' : 'pointer',
                  fontSize: '14px',
                  fontWeight: 'bold',
                }}
              >
                {savingAssetClassTargets ? '저장 중...' : '자산별 목표 % 일괄저장'}
              </button>
            </div>

            <div className={styles.infoBox} style={{ marginTop: '16px' }}>
              <p>{targetYear}년도 자산클래스별 목표 비율을 입력하세요.</p>
              <p>입력한 값은 브라우저에 저장되며, 합계가 100%가 되도록 관리하세요.</p>
            </div>

            <div className={styles.tableWrapper} style={{ overflowX: 'auto', marginTop: '16px' }}>
              <table className={styles.table} style={{ minWidth: '600px' }}>
                <thead>
                  <tr>
                    <th>자산클래스</th>
                    <th style={{ textAlign: 'right' }}>목표 비율 (%)</th>
                  </tr>
                </thead>
                <tbody>
                  {(() => {
                    const assetClassOrder = ['주식', '채권', '금', '통화', '부동산', '가상자산'];
                    const allAssetClasses = Array.from(new Set(products.map((p) => p.asset_class)));
                    const sortedAssetClasses = [
                      ...assetClassOrder.filter(ac => allAssetClasses.includes(ac)),
                      ...allAssetClasses.filter(ac => !assetClassOrder.includes(ac)).sort()
                    ];
                    return sortedAssetClasses.map((assetClass) => (
                      <tr key={assetClass}>
                        <td>{assetClass}</td>
                        <td style={{ textAlign: 'right' }}>
                          <input
                            type="number"
                            min="0"
                            max="100"
                            step="0.01"
                            className={styles.amountInput}
                            value={assetClassTargets[assetClass] || ''}
                            onChange={(e) =>
                              setAssetClassTargets((prev) => ({
                                ...prev,
                                [assetClass]: e.target.value,
                              }))
                            }
                            placeholder="0.00"
                            style={{ textAlign: 'right' }}
                          />
                        </td>
                      </tr>
                    ));
                  })()}
                  <tr style={{ fontWeight: 'bold', backgroundColor: '#e8f4f8' }}>
                    <td>합계</td>
                    <td style={{ textAlign: 'right' }}>
                      {Object.values(assetClassTargets)
                        .reduce((sum, val) => sum + (parseFloat(val) || 0), 0)
                        .toFixed(2)}
                      %
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
