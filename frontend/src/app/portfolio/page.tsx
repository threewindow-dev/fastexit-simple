'use client';

import React, { useEffect, useRef, useState } from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, ComposedChart, Bar, BarChart } from 'recharts';
import styles from './portfolio.module.css';
import { filterSnapshotInputEligibleHoldings } from './snapshotInputPolicy';

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
  display_order: number;
  created_at: string;
}

interface Account {
  account_id: number;
  institution_id: number;
  name: string;
  type: string;
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

interface WeeklyPivotReportData {
  year: number;
  weeks: WeeklyPivotWeekInfo[];
  account_groups: WeeklyPivotAccountGroupRow[];
  accounts: WeeklyPivotAccountRow[];
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

const getDataSourceLabel = (dataSource: string): string => {
  const labels: { [key: string]: string } = {
    manual: '수동입력',
    auto: 'API연동',
    missing: '엑셀업로드',
  };
  return labels[dataSource] || dataSource;
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
    characteristics: string;
  } | null>(null);
  const [showProductEditForm, setShowProductEditForm] = useState(false);

  // Account Form
  const [newAccount, setNewAccount] = useState({
    institution_id: '',
    name: '',
    type: '위탁계좌',
    display_order: '0',
  });
  const [showAccountForm, setShowAccountForm] = useState(false);
  const [editingAccount, setEditingAccount] = useState<{
    account_id: number;
    institution_id: number;
    name: string;
    type: string;
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
    filterSnapshotInputEligibleHoldings(holdings, products)
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
      return ordered.map((item, index) => ({
        ...item,
        display_order: index + 1,
      }));
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

  const annualReportYearIndex = annualReportData
    ? annualReportData.weeks.findIndex(
        (item) => new Date(item.reference_date).getFullYear() === targetYear
      )
    : -1;

  // 전년도 평가금액을 시작일 평가금액으로 사용
  const previousYearIndex = annualReportData
    ? annualReportData.weeks.findIndex(
        (item) => new Date(item.reference_date).getFullYear() === targetYear - 1
      )
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
  } else if (annualReportData && annualReportYearIndex >= 0) {
    annualReportData.account_groups.forEach((group) => {
      const value = group.valuations[annualReportYearIndex]?.amount ?? 0;
      actualAmountMap.set(group.account_group_id, value);
    });
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
      fetchSnapshotHoldings();
      fetchAnnualSnapshots();
      fetchAccountGroups();
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
    if (!selectedSnapshotId) {
      setSnapshotHoldingDrafts({});
      return;
    }

    const snapshotId = parseInt(selectedSnapshotId, 10);
    setSnapshotHoldingDrafts(buildSnapshotDrafts(snapshotId, true));
  }, [selectedSnapshotId, holdings, products, snapshotHoldings]);

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
      const response = await fetch(`${API_BASE_URL}/portfolio/institutions`);
      if (!response.ok) throw new Error('Failed to fetch institutions');
      const result = await response.json();
      const items = Array.isArray(result) ? result : result.data?.items || [];
      const maxDisplayOrder = Array.isArray(result)
        ? Math.max(0, ...items.map((item: Institution) => item.display_order ?? 0))
        : result.data?.max_display_order ?? Math.max(0, ...items.map((item: Institution) => item.display_order ?? 0));
      setInstitutions(items);
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
        setAnnualReportData(result.data);
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

  // Load asset class targets from API
  useEffect(() => {
    if (activeTab === 'targetAllocations') {
      fetchAssetClassTargets(targetYear);
    }
  }, [targetYear, activeTab]);

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
      setProducts(ordered);
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
        display_order: nextOrder,
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/accounts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to create account');
      setNewAccount({ institution_id: '', name: '', type: '위탁계좌', display_order: '0' });
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

    const targets = filterSnapshotInputEligibleHoldings(holdings, products)
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
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>정렬</th>
                  <th>번호</th>
                  <th>기관명</th>
                  <th>유형</th>
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
                    <td>{inst.name}</td>
                    <td>{inst.type}</td>
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
                  <th>지역</th>
                  <th>통화</th>
                  <th>투자유형</th>
                  <th>위험도</th>
                  <th>스냅샷 입력</th>
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
                    <td>{prod.region}</td>
                    <td>{prod.currency}</td>
                    <td>{prod.investment_type}</td>
                    <td>{prod.risk_level}</td>
                    <td>{prod.allow_snapshot_input ? '허용' : '제외'}</td>
                    <td>
                      <div className={styles.actionButtons}>
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

              const views = holdings
                .filter((holding) => {
                  // 삭제된 항목은 제외
                  if (holding.deleted_at) {
                    return false;
                  }
                  // 이미 값이 입력되어 있으면 표시
                  if (holdingMap.has(holding.holding_id)) {
                    return true;
                  }
                  // allow_snapshot_input이 true인 경우만 표시
                  const product = products.find((p) => p.product_id === holding.product_id);
                  return product?.allow_snapshot_input !== false;
                })
                .map((holding) => {
                  const account = accounts.find((a) => a.account_id === holding.account_id) || null;
                  const institution = institutions.find((i) => i.institution_id === account?.institution_id) || null;
                  const product = products.find((p) => p.product_id === holding.product_id) || null;
                  return {
                    holding,
                    account,
                    institution,
                    product,
                    existing: holdingMap.get(holding.holding_id) || null,
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
                const effectiveValue = isSnapshotLocked 
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
                  const effectiveValue = isSnapshotLocked 
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
                      <td>{truncateText(view.product?.product_name || '-')}</td>
                      <td className={styles.amountCell}>
                        {previousAmount != null && previousAmount > 0 ? formatAmount(previousAmount) : '-'}
                      </td>
                      <td>
                        {(() => {
                          const draftValue = snapshotHoldingDrafts[view.holding.holding_id];
                          const displayValue = isSnapshotLocked 
                            ? (view.existing?.valuation_amount ?? '')
                            : (draftValue !== undefined ? draftValue : (view.existing?.valuation_amount ?? ''));
                          const isDirty = isDraftDifferent(displayValue, view.existing?.valuation_amount);
                          return (
                            <input
                              type="text"
                              inputMode="decimal"
                              className={`${styles.amountInput}${isDirty ? ` ${styles.amountInputDirty}` : ''}`}
                              data-index={globalIndex - 1}
                              data-holding-id={view.holding.holding_id}
                              value={displayValue}
                              disabled={isSnapshotLocked}
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
                      <td>{getDataSourceLabel(view.existing?.data_source || snapshotHoldingDataSource)}</td>
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

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : weeklyReportData && weeklyReportData.weeks.length > 0 ? (
            <div className={styles.tableWrapper} style={{ overflowX: 'auto' }}>
              <table className={styles.table} style={{ minWidth: '800px' }}>
                <thead style={{ position: 'sticky', top: 0, zIndex: 10, backgroundColor: '#fff' }}>
                  <tr>
                    <th style={{ position: 'sticky', left: 0, backgroundColor: '#fff', zIndex: 11, width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                      금융기관
                    </th>
                    <th style={{ position: 'sticky', left: '160px', backgroundColor: '#fff', zIndex: 11, width: '200px', minWidth: '200px' }}>
                      계좌
                    </th>
                    {weeklyReportData.weeks.map((week) => (
                      <th key={week.weekly_snapshot_id} style={{ backgroundColor: '#fff', minWidth: '100px', fontSize: '11px', padding: '6px 4px', textAlign: 'center' }}>
                        {week.reference_date} (W{week.week_number})
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {/* 계좌그룹 섹션 (상단) */}
                  {weeklyReportData.account_groups && weeklyReportData.account_groups.length > 0 && (
                    <>
                      <tr style={{ borderBottom: '2px solid #ccc' }}>
                        <td colSpan={weeklyReportData.weeks.length + 2} style={{ padding: '10px 8px', backgroundColor: '#f5f5f5', fontWeight: 'bold', textAlign: 'center' }}>
                          계좌 그룹
                        </td>
                      </tr>
                      {[...weeklyReportData.account_groups].sort((a, b) => a.display_order - b.display_order).map((group) => (
                        <tr key={group.account_group_id} style={{ backgroundColor: '#fffacd' }}>
                          <td style={{ position: 'sticky', left: 0, backgroundColor: '#fffacd', zIndex: 1, fontWeight: 'bold', width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                            {group.account_group_name}
                          </td>
                          <td style={{ position: 'sticky', left: '160px', backgroundColor: '#fffacd', zIndex: 1, fontSize: '11px', color: '#666', width: '200px', minWidth: '200px' }}>
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
                        <td style={{ position: 'sticky', left: '160px', backgroundColor: '#ffeb99', zIndex: 1, width: '200px', minWidth: '200px' }}>
                        </td>
                        {weeklyReportData.weeks.map((week, weekIdx) => {
                          const total = weeklyReportData.accounts.reduce((sum, account) => {
                            const val = account.valuations[weekIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);
                          return (
                            <td key={week.weekly_snapshot_id} style={{ textAlign: 'right' }}>
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
                        <td colSpan={weeklyReportData.weeks.length + 2} style={{ padding: '10px 8px', backgroundColor: '#f5f5f5', fontWeight: 'bold', textAlign: 'center' }}>
                          전체 계좌
                        </td>
                      </tr>
                    </>
                  )}

                  {weeklyReportData.accounts.map((account) => (
                    <tr key={account.account_id}>
                      <td style={{ position: 'sticky', left: 0, backgroundColor: '#fff', zIndex: 1, width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                        {account.institution_name}
                      </td>
                      <td style={{ position: 'sticky', left: '160px', backgroundColor: '#fff', zIndex: 1, width: '200px', minWidth: '200px' }}>
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
                  {weeklyReportData.accounts.length > 0 && (
                    <>
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#f0f0f0' }}>
                        <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#f0f0f0', zIndex: 1, width: '360px', minWidth: '360px' }}>
                          총합
                        </td>
                        {weeklyReportData.weeks.map((week, weekIdx) => {
                          const total = weeklyReportData.accounts.reduce((sum, account) => {
                            const val = account.valuations[weekIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);
                          return (
                            <td key={week.weekly_snapshot_id} style={{ textAlign: 'right' }}>
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
                      {/* 전주 대비 변화 행 */}
                      <tr style={{ fontWeight: 'bold', backgroundColor: '#fff5f5' }}>
                        <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#fff5f5', zIndex: 1, width: '360px', minWidth: '360px' }}>
                          전주 대비 변화
                        </td>
                        {weeklyReportData.weeks.map((week, weekIdx) => {
                          const currentTotal = weeklyReportData.accounts.reduce((sum, account) => {
                            const val = account.valuations[weekIdx];
                            return sum + (val ? val.amount : 0);
                          }, 0);

                          let changePercent = 0;
                          let changeColor = 'black';

                          if (weekIdx > 0) {
                            const prevTotal = weeklyReportData.accounts.reduce((sum, account) => {
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
                                ? changePercent.toFixed(2) + '%'
                                : '-'}
                            </td>
                          );
                        })}
                      </tr>
                    </>
                  )}
                </tbody>
              </table>
            </div>
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
            <div className={styles.tableWrapper} style={{ overflowX: 'auto' }}>
              <table className={styles.table} style={{ minWidth: '800px' }}>
                <thead style={{ position: 'sticky', top: 0, zIndex: 10, backgroundColor: '#fff' }}>
                  <tr>
                    <th style={{ position: 'sticky', left: 0, backgroundColor: '#fff', zIndex: 11, width: '160px', minWidth: '160px', whiteSpace: 'nowrap' }}>
                      금융기관
                    </th>
                    <th style={{ position: 'sticky', left: '160px', backgroundColor: '#fff', zIndex: 11, width: '200px', minWidth: '200px' }}>
                      계좌
                    </th>
                    {annualReportData.weeks.map((yearPoint) => (
                      <th key={yearPoint.weekly_snapshot_id} style={{ backgroundColor: '#fff', minWidth: '100px', fontSize: '11px', padding: '6px 4px', textAlign: 'center' }}>
                        {new Date(yearPoint.reference_date).getFullYear() - 1}년
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
                          <td style={{ position: 'sticky', left: '160px', backgroundColor: '#fffacd', zIndex: 1, fontSize: '11px', color: '#666', width: '200px', minWidth: '200px' }}>
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
                        <td style={{ position: 'sticky', left: '160px', backgroundColor: '#ffeb99', zIndex: 1, width: '200px', minWidth: '200px' }}>
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
                      <td style={{ position: 'sticky', left: '160px', backgroundColor: '#fff', zIndex: 1, width: '200px', minWidth: '200px' }}>
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
                        <td colSpan={2} style={{ position: 'sticky', left: 0, backgroundColor: '#f0f0f0', zIndex: 1, width: '360px', minWidth: '360px' }}>
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
                    </>
                  )}
                </tbody>
              </table>
            </div>
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

            const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF6B6B'];

            const totalValue = chartData.reduce((sum, item) => sum + item.value, 0);

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
                    <h3>자산 유형별 상세</h3>
                    <table className={styles.table}>
                      <thead>
                        <tr>
                          <th>자산 유형</th>
                          <th style={{ textAlign: 'right' }}>금액</th>
                          <th style={{ textAlign: 'right' }}>비중</th>
                        </tr>
                      </thead>
                      <tbody>
                        {chartData.map((item, idx) => (
                          <tr key={idx}>
                            <td>{item.name}</td>
                            <td style={{ textAlign: 'right' }}>
                              {item.value.toLocaleString('ko-KR', { minimumFractionDigits: 0 })} 원
                            </td>
                            <td style={{ textAlign: 'right' }}>
                              {((item.value / totalValue) * 100).toFixed(2)}%
                            </td>
                          </tr>
                        ))}
                        <tr style={{ fontWeight: 'bold', backgroundColor: '#f5f5f5' }}>
                          <td>합계</td>
                          <td style={{ textAlign: 'right' }}>
                            {totalValue.toLocaleString('ko-KR', { minimumFractionDigits: 0 })} 원
                          </td>
                          <td style={{ textAlign: 'right' }}>100.00%</td>
                        </tr>
                      </tbody>
                    </table>
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
                  <ComposedChart data={chartData}>
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
                <h2>연간 평가금액 추이</h2>
                
                {/* 평가금액 선그래프 */}
                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
                  <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={chartDataByYear}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="year" />
                      <YAxis 
                        tickFormatter={(value) =>
                          (value / 1000000).toFixed(0) + 'M'
                        }
                        label={{ value: '평가금액 (원)', angle: -90, position: 'insideLeft' }}
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
                      />
                      {/* 계좌그룹별 라인 */}
                      {allAccountGroups.map((group, idx) => (
                        <Line
                          key={group}
                          type="monotone"
                          dataKey={group}
                          stroke={lineColors[idx % lineColors.length]}
                          strokeWidth={2}
                          dot={{ fill: lineColors[idx % lineColors.length], r: 4 }}
                          activeDot={{ r: 6 }}
                        />
                      ))}
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
                        tickFormatter={(value) => `${value.toFixed(0)}%`}
                        label={{ value: '증가율 (%)', angle: -90, position: 'insideLeft' }}
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
