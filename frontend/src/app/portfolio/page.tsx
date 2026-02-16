'use client';

import React, { useEffect, useRef, useState } from 'react';
import styles from './portfolio.module.css';

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

interface Snapshot {
  snapshot_id: number;
  user_id: number;
  reference_date: string;
  status: string;
  locked_at: string | null;
  editable_until: string | null;
  created_at: string;
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
  const [activeTab, setActiveTab] = useState<'institutions' | 'products' | 'accounts' | 'snapshots' | 'holdings' | 'snapshotHoldings' | 'clone' | 'reports'>('institutions');
  const [institutions, setInstitutions] = useState<Institution[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [holdings, setHoldings] = useState<Holding[]>([]);
  const [snapshotHoldings, setSnapshotHoldings] = useState<SnapshotHolding[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
  const [snapshotHoldingDrafts, setSnapshotHoldingDrafts] = useState<Record<number, string>>({});
  const [snapshotHoldingDataSource, setSnapshotHoldingDataSource] = useState('manual');
  const [savingSnapshotHoldings, setSavingSnapshotHoldings] = useState(false);
  const snapshotHoldingsTableRef = useRef<HTMLTableElement | null>(null);
  const [draggingInstitutionId, setDraggingInstitutionId] = useState<number | null>(null);
  const [draggingAccountId, setDraggingAccountId] = useState<number | null>(null);
  const [draggingProductId, setDraggingProductId] = useState<number | null>(null);
  const [savingInstitutionOrder, setSavingInstitutionOrder] = useState(false);
  const [savingAccountOrder, setSavingAccountOrder] = useState(false);
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
    holdings
      .filter((holding) => !holding.deleted_at)
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

  const selectedSnapshot = selectedSnapshotId
    ? snapshots.find((snap) => snap.snapshot_id === Number(selectedSnapshotId)) || null
    : null;
  const isSelectedSnapshotLocked = selectedSnapshot?.status === 'locked';

  useEffect(() => {
    if (activeTab === 'institutions') {
      fetchInstitutions();
    } else if (activeTab === 'products') {
      fetchProducts();
      fetchInstitutions();
    } else if (activeTab === 'accounts') {
      fetchAccounts();
      fetchInstitutions(); // For dropdown
    } else if (activeTab === 'snapshots') {
      fetchSnapshots();
    } else if (activeTab === 'holdings') {
      fetchHoldings();
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
    }
  }, [activeTab]);

  useEffect(() => {
    if (!selectedSnapshotId) {
      setSnapshotHoldingDrafts({});
      return;
    }

    const snapshotId = parseInt(selectedSnapshotId, 10);
    setSnapshotHoldingDrafts(buildSnapshotDrafts(snapshotId, true));
  }, [selectedSnapshotId, holdings, snapshotHoldings]);

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

  const openProductEdit = (product: Product) => {
    setEditingProduct({
      product_id: product.product_id,
      product_name: product.product_name,
      asset_class: product.asset_class,
      region: product.region,
      currency: product.currency,
      investment_type: product.investment_type,
      risk_level: product.risk_level,
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

    const targets = holdings
      .filter((holding) => !holding.deleted_at)
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
      const endpoint = cloneForm.period_type === 'weekly' ? 'weekly-snapshots' : 'annual-snapshots';
      const response = await fetch(
        `${API_BASE_URL}/portfolio/${endpoint}?source_snapshot_id=${cloneForm.source_snapshot_id}`,
        { method: 'POST' }
      );
      if (!response.ok) throw new Error('Failed to clone snapshot');
      alert(`${cloneForm.period_type === 'weekly' ? '주간' : '연간'} 스냅샷이 생성되었습니다.`);
      setCloneForm({ source_snapshot_id: '', period_type: 'weekly' });
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
        url = `${API_BASE_URL}/portfolio/reports/weekly-account/${account_id}?reference_date=${reference_date}`;
      } else if (report_type === 'annual_account' && account_id) {
        url = `${API_BASE_URL}/portfolio/reports/annual-account/${account_id}?reference_date=${reference_date}`;
      } else if (report_type === 'weekly_account_group' && account_group_id) {
        url = `${API_BASE_URL}/portfolio/reports/weekly-account-group/${account_group_id}?reference_date=${reference_date}`;
      } else if (report_type === 'asset_class') {
        url = `${API_BASE_URL}/portfolio/reports/asset-class?reference_date=${reference_date}`;
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
      if (!response.ok) throw new Error('Failed to lock snapshot');
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

  const clearHoldingsFilter = () => {
    setHoldingsAccountFilter(null);
    setHoldingsProductFilter(null);
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>포트폴리오 관리</h1>
        <nav className={styles.nav}>
          <a href="/" className={styles.navLink}>Users</a>
          <a href="/portfolio" className={styles.navLink}>Portfolio</a>
        </nav>
      </header>

      <div className={styles.tabs}>
        <button
          className={activeTab === 'institutions' ? styles.activeTab : ''}
          onClick={() => setActiveTab('institutions')}
        >
          금융기관
        </button>
        <button
          className={activeTab === 'accounts' ? styles.activeTab : ''}
          onClick={() => setActiveTab('accounts')}
        >
          계좌
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
        <button
          className={activeTab === 'snapshots' ? styles.activeTab : ''}
          onClick={() => setActiveTab('snapshots')}
        >
          일일 스냅샷
        </button>
        <button
          className={activeTab === 'snapshotHoldings' ? styles.activeTab : ''}
          onClick={() => setActiveTab('snapshotHoldings')}
        >
          일일 스냅샷 보유자산
        </button>
        <button
          className={activeTab === 'clone' ? styles.activeTab : ''}
          onClick={() => setActiveTab('clone')}
        >
          스냅샷 복제
        </button>
        <button
          className={activeTab === 'reports' ? styles.activeTab : ''}
          onClick={() => setActiveTab('reports')}
        >
          보고서
        </button>
      </div>

      {error && <div className={styles.error}>{error}</div>}

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
                    <td>
                      <div className={styles.actionButtons}>
                        <button onClick={() => openProductEdit(prod)}>수정</button>
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
            <select
              value={snapshotHoldingDataSource}
              onChange={(e) => setSnapshotHoldingDataSource(e.target.value)}
              disabled={!selectedSnapshotId || isSelectedSnapshotLocked}
            >
              <option value="manual">수동입력</option>
              <option value="auto">API연동</option>
              <option value="missing">엑셀업로드</option>
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
              const holdingMap = new Map<number, SnapshotHolding>();
              snapshotHoldings
                .filter((item) => item.snapshot_id === snapshotId)
                .forEach((item) => {
                  holdingMap.set(item.holding_id, item);
                });

              const views = holdings
                .filter((holding) => !holding.deleted_at)
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

              const totalSum = views.reduce((sum, view) => {
                const draftValue = snapshotHoldingDrafts[view.holding.holding_id] ?? '';
                return sum + parseAmount(draftValue);
              }, 0);
              let accountSum = 0;
              let currentAccountId: number | null = null;
              let currentAccountLabel = '';
              const rows: React.ReactNode[] = [];

              views.forEach((view, index) => {
                const accountId = view.account?.account_id ?? view.holding.account_id;
                const accountLabel = `${view.institution?.name || '-'} - ${view.account?.name || '-'}`;
                const amount = parseAmount(snapshotHoldingDrafts[view.holding.holding_id] ?? '');

                if (currentAccountId === null) {
                  currentAccountId = accountId;
                  currentAccountLabel = accountLabel;
                  accountSum = 0;
                } else if (currentAccountId !== accountId) {
                  rows.push(
                    <tr key={`summary-${currentAccountId}`}>
                      <td colSpan={4}>계좌 합계 ({currentAccountLabel})</td>
                      <td className={styles.amountCell}>{formatAmount(accountSum)}</td>
                      <td className={styles.amountCell}>
                        {formatRatio(totalSum > 0 ? (accountSum / totalSum) * 100 : 0)}
                      </td>
                      <td></td>
                    </tr>
                  );
                  currentAccountId = accountId;
                  currentAccountLabel = accountLabel;
                  accountSum = 0;
                }

                accountSum += amount;

                rows.push(
                  <tr key={`${snapshotId}-${view.holding.holding_id}`}>
                    <td>{snapshot?.reference_date || '-'}</td>
                    <td>{view.institution?.name || '-'}</td>
                    <td>{view.account?.name || '-'}</td>
                    <td>{view.product?.product_name || '-'}</td>
                    <td>
                      {(() => {
                        const draftValue = snapshotHoldingDrafts[view.holding.holding_id] ?? '';
                        const isDirty = isDraftDifferent(draftValue, view.existing?.valuation_amount);
                        return (
                      <input
                          type="text"
                          inputMode="decimal"
                          className={`${styles.amountInput}${isDirty ? ` ${styles.amountInputDirty}` : ''}`}
                        data-index={index}
                          data-holding-id={view.holding.holding_id}
                          value={draftValue}
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

              if (currentAccountId !== null) {
                rows.push(
                  <tr key={`summary-${currentAccountId}-final`}>
                    <td colSpan={4}>계좌 합계 ({currentAccountLabel})</td>
                    <td className={styles.amountCell}>{formatAmount(accountSum)}</td>
                    <td className={styles.amountCell}>
                      {formatRatio(totalSum > 0 ? (accountSum / totalSum) * 100 : 0)}
                    </td>
                    <td></td>
                  </tr>
                );
              }

              return (
                <table className={styles.table} ref={snapshotHoldingsTableRef}>
                  <thead>
                    <tr>
                      <th>스냅샷일자</th>
                      <th>금융기관</th>
                      <th>계좌이름</th>
                      <th>상품이름</th>
                      <th>평가금액</th>
                      <th>비중</th>
                      <th>데이터소스</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colSpan={4}>전체 합계</td>
                      <td className={styles.amountCell}>{formatAmount(totalSum)}</td>
                      <td className={styles.amountCell}>{formatRatio(totalSum > 0 ? 100 : 0)}</td>
                      <td></td>
                    </tr>
                    {rows}
                    <tr>
                      <td colSpan={4}>전체 합계</td>
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

      {/* Clone Tab */}
      {activeTab === 'clone' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>스냅샷 복제</h2>
            <button onClick={() => setShowCloneForm(!showCloneForm)}>
              {showCloneForm ? '취소' : '복제 시작'}
            </button>
          </div>

          {showCloneForm && (
            <form onSubmit={handleCloneSnapshot} className={styles.form}>
              <select
                value={cloneForm.source_snapshot_id}
                onChange={(e) => setCloneForm({ ...cloneForm, source_snapshot_id: e.target.value })}
                required
              >
                <option value="">원본 스냅샷 선택</option>
                {snapshots.filter(s => s.status === 'locked').map((snap) => (
                  <option key={snap.snapshot_id} value={snap.snapshot_id}>
                    {snap.reference_date} (ID: {snap.snapshot_id}) - 잠금됨
                  </option>
                ))}
              </select>
              <select
                value={cloneForm.period_type}
                onChange={(e) => setCloneForm({ ...cloneForm, period_type: e.target.value })}
              >
                <option value="weekly">주간 스냅샷</option>
                <option value="annual">연간 스냅샷</option>
              </select>
              <button type="submit">복제</button>
            </form>
          )}

          <div className={styles.infoBox}>
            <p>✏️ 잠금된 스냅샷만 복제할 수 있습니다.</p>
            <p>📅 주간 스냅샷: 주간 보고서용 데이터</p>
            <p>📊 연간 스냅샷: 연간 보고서용 데이터</p>
          </div>
        </div>
      )}

      {/* Reports Tab */}
      {activeTab === 'reports' && (
        <div className={styles.tabContent}>
          <div className={styles.sectionHeader}>
            <h2>보고서 조회</h2>
            <button onClick={handleLoadReport}>조회</button>
          </div>

          <div className={styles.form}>
            <select
              value={reportFilter.report_type}
              onChange={(e) => setReportFilter({ ...reportFilter, report_type: e.target.value })}
            >
              <option value="weekly_account">주간 계좌 보고서</option>
              <option value="annual_account">연간 계좌 보고서</option>
              <option value="weekly_account_group">주간 계좌그룹 보고서</option>
              <option value="asset_class">자산클래스 보고서</option>
            </select>
            <input
              type="date"
              value={reportFilter.reference_date}
              onChange={(e) => setReportFilter({ ...reportFilter, reference_date: e.target.value })}
            />
            {(reportFilter.report_type === 'weekly_account' || reportFilter.report_type === 'annual_account') && (
              <input
                type="number"
                placeholder="계좌 ID"
                value={reportFilter.account_id}
                onChange={(e) => setReportFilter({ ...reportFilter, account_id: e.target.value })}
              />
            )}
            {reportFilter.report_type === 'weekly_account_group' && (
              <input
                type="number"
                placeholder="계좌그룹 ID"
                value={reportFilter.account_group_id}
                onChange={(e) => setReportFilter({ ...reportFilter, account_group_id: e.target.value })}
              />
            )}
          </div>

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : reports.length > 0 ? (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>기간유형</th>
                  <th>기준일</th>
                  <th>계좌/그룹/자산</th>
                  <th>총 평가금액</th>
                </tr>
              </thead>
              <tbody>
                {reports.map((report, idx) => (
                  <tr key={idx}>
                    <td>{report.period_type}</td>
                    <td>{report.reference_date}</td>
                    <td>{report.account_name || report.account_group_name || report.asset_class || '-'}</td>
                    <td>{report.total_value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className={styles.infoBox}>
              <p>보고서 타입을 선택하고 조회 버튼을 클릭하세요.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
