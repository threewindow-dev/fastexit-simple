'use client';

import React, { useEffect, useState } from 'react';
import styles from './portfolio.module.css';

interface Institution {
  institution_id: number;
  name: string;
  type: string;
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
  created_at: string;
}

interface Account {
  account_id: number;
  institution_id: number;
  name: string;
  type: string;
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

interface SnapshotHolding {
  snapshot_holding_id: number;
  snapshot_id: number;
  holding_id: number;
  valuation_amount: string;
  data_source: string;
  created_at: string;
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
  const [newInstitution, setNewInstitution] = useState({ name: '', type: '증권사' });
  const [showInstitutionForm, setShowInstitutionForm] = useState(false);

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

  // Account Form
  const [newAccount, setNewAccount] = useState({
    institution_id: '',
    name: '',
    type: '위탁계좌',
  });
  const [showAccountForm, setShowAccountForm] = useState(false);

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

  // Snapshot Holding Form
  const [newSnapshotHolding, setNewSnapshotHolding] = useState({
    snapshot_id: '',
    holding_id: '',
    valuation_amount: '',
    data_source: 'manual',
  });
  const [showSnapshotHoldingForm, setShowSnapshotHoldingForm] = useState(false);

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

  useEffect(() => {
    if (activeTab === 'institutions') {
      fetchInstitutions();
    } else if (activeTab === 'products') {
      fetchProducts();
    } else if (activeTab === 'accounts') {
      fetchAccounts();
      fetchInstitutions(); // For dropdown
    } else if (activeTab === 'snapshots') {
      fetchSnapshots();
    } else if (activeTab === 'holdings') {
      fetchHoldings();
      fetchAccounts(); // For dropdown
      fetchProducts(); // For dropdown
    } else if (activeTab === 'snapshotHoldings') {
      fetchSnapshotHoldings();
      fetchSnapshots(); // For dropdown
      fetchHoldings(); // For dropdown
    }
  }, [activeTab]);

  const fetchInstitutions = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/portfolio/institutions`);
      if (!response.ok) throw new Error('Failed to fetch institutions');
      const result = await response.json();
      // 백엔드가 배열로 직접 반환한다고 가정
      setInstitutions(Array.isArray(result) ? result : result.data?.items || []);
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

  const handleCreateInstitution = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/portfolio/institutions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newInstitution),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to create institution');
      setNewInstitution({ name: '', type: '증권사' });
      setShowInstitutionForm(false);
      fetchInstitutions();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create institution');
    }
  };

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        ...newProduct,
        characteristics: newProduct.characteristics
          ? newProduct.characteristics.split(',').map((s) => s.trim())
          : undefined,
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
      fetchProducts();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create product');
    }
  };

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        institution_id: parseInt(newAccount.institution_id, 10),
        name: newAccount.name,
        type: newAccount.type,
      };
      const response = await fetch(`${API_BASE_URL}/portfolio/accounts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Failed to create account');
      setNewAccount({ institution_id: '', name: '', type: '위탁계좌' });
      setShowAccountForm(false);
      fetchAccounts();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create account');
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

  const handleCreateSnapshotHolding = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        valuation_amount: parseFloat(newSnapshotHolding.valuation_amount),
        data_source: newSnapshotHolding.data_source,
      };
      const response = await fetch(
        `${API_BASE_URL}/portfolio/snapshots/${newSnapshotHolding.snapshot_id}/holdings/${newSnapshotHolding.holding_id}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        }
      );
      if (!response.ok) throw new Error('Failed to create snapshot holding');
      setNewSnapshotHolding({ snapshot_id: '', holding_id: '', valuation_amount: '', data_source: 'manual' });
      setShowSnapshotHoldingForm(false);
      fetchSnapshotHoldings();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create snapshot holding');
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
      alert('스냅샷이 잠금 처리되었습니다.');
      fetchSnapshots();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to lock snapshot');
    }
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
          className={activeTab === 'products' ? styles.activeTab : ''}
          onClick={() => setActiveTab('products')}
        >
          상품
        </button>
        <button
          className={activeTab === 'accounts' ? styles.activeTab : ''}
          onClick={() => setActiveTab('accounts')}
        >
          계좌
        </button>
        <button
          className={activeTab === 'snapshots' ? styles.activeTab : ''}
          onClick={() => setActiveTab('snapshots')}
        >
          스냅샷
        </button>
        <button
          className={activeTab === 'holdings' ? styles.activeTab : ''}
          onClick={() => setActiveTab('holdings')}
        >
          보유자산
        </button>
        <button
          className={activeTab === 'snapshotHoldings' ? styles.activeTab : ''}
          onClick={() => setActiveTab('snapshotHoldings')}
        >
          스냅샷 보유자산
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
            <button onClick={() => setShowInstitutionForm(!showInstitutionForm)}>
              {showInstitutionForm ? '취소' : '+ 추가'}
            </button>
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
                <option value="보험사">보험사</option>
                <option value="거래소">거래소</option>
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
                  <th>ID</th>
                  <th>기관명</th>
                  <th>유형</th>
                  <th>생성일</th>
                </tr>
              </thead>
              <tbody>
                {institutions.map((inst) => (
                  <tr key={inst.institution_id}>
                    <td>{inst.institution_id}</td>
                    <td>{inst.name}</td>
                    <td>{inst.type}</td>
                    <td>{new Date(inst.created_at).toLocaleDateString()}</td>
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
            <button onClick={() => setShowProductForm(!showProductForm)}>
              {showProductForm ? '취소' : '+ 추가'}
            </button>
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

          {loading ? (
            <div className={styles.loading}>로딩 중...</div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>상품명</th>
                  <th>자산군</th>
                  <th>지역</th>
                  <th>통화</th>
                  <th>투자유형</th>
                  <th>위험도</th>
                </tr>
              </thead>
              <tbody>
                {products.map((prod) => (
                  <tr key={prod.product_id}>
                    <td>{prod.product_id}</td>
                    <td>{prod.product_name}</td>
                    <td>{prod.asset_class}</td>
                    <td>{prod.region}</td>
                    <td>{prod.currency}</td>
                    <td>{prod.investment_type}</td>
                    <td>{prod.risk_level}</td>
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
            <button onClick={() => setShowAccountForm(!showAccountForm)}>
              {showAccountForm ? '취소' : '+ 추가'}
            </button>
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
                <option value="위탁계좌">위탁계좌</option>
                <option value="연금계좌">연금계좌</option>
                <option value="ISA계좌">ISA계좌</option>
                <option value="예금계좌">예금계좌</option>
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
                  <th>ID</th>
                  <th>계좌명</th>
                  <th>금융기관</th>
                  <th>유형</th>
                  <th>생성일</th>
                </tr>
              </thead>
              <tbody>
                {accounts.map((acc) => {
                  const inst = institutions.find((i) => i.institution_id === acc.institution_id);
                  return (
                    <tr key={acc.account_id}>
                      <td>{acc.account_id}</td>
                      <td>{acc.name}</td>
                      <td>{inst?.name || acc.institution_id}</td>
                      <td>{acc.type}</td>
                      <td>{new Date(acc.created_at).toLocaleDateString()}</td>
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
                  <th>ID</th>
                  <th>기준일</th>
                  <th>상태</th>
                  <th>잠금일시</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                {snapshots.map((snap) => (
                  <tr key={snap.snapshot_id}>
                    <td>{snap.snapshot_id}</td>
                    <td>{snap.reference_date}</td>
                    <td>{snap.status === 'locked' ? '🔒 잠금' : '✏️ 편집 가능'}</td>
                    <td>{snap.locked_at ? new Date(snap.locked_at).toLocaleString() : '-'}</td>
                    <td>
                      {snap.status !== 'locked' && (
                        <button onClick={() => handleLockSnapshot(snap.snapshot_id)}>잠금</button>
                      )}
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

          {showHoldingForm && (
            <form onSubmit={handleCreateHolding} className={styles.form}>
              <select
                value={newHolding.account_id}
                onChange={(e) => setNewHolding({ ...newHolding, account_id: e.target.value })}
                required
              >
                <option value="">계좌 선택</option>
                {accounts.map((acc) => (
                  <option key={acc.account_id} value={acc.account_id}>
                    {acc.name}
                  </option>
                ))}
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
                  <th>ID</th>
                  <th>계좌이름</th>
                  <th>상품이름</th>
                  <th>생성일</th>
                </tr>
              </thead>
              <tbody>
                {holdings.filter(h => !h.deleted_at).map((holding) => {
                  const account = accounts.find((a) => a.account_id === holding.account_id);
                  const product = products.find((p) => p.product_id === holding.product_id);
                  return (
                    <tr key={holding.holding_id}>
                      <td>{holding.holding_id}</td>
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
            <h2>스냅샷 보유자산 목록</h2>
            <button onClick={() => setShowSnapshotHoldingForm(!showSnapshotHoldingForm)}>
              {showSnapshotHoldingForm ? '취소' : '+ 추가'}
            </button>
          </div>

          {showSnapshotHoldingForm && (
            <form onSubmit={handleCreateSnapshotHolding} className={styles.form}>
              <select
                value={newSnapshotHolding.snapshot_id}
                onChange={(e) => setNewSnapshotHolding({ ...newSnapshotHolding, snapshot_id: e.target.value })}
                required
              >
                <option value="">스냅샷 선택</option>
                {snapshots.map((snap) => (
                  <option key={snap.snapshot_id} value={snap.snapshot_id}>
                    {snap.reference_date} (ID: {snap.snapshot_id})
                  </option>
                ))}
              </select>
              <select
                value={newSnapshotHolding.holding_id}
                onChange={(e) => setNewSnapshotHolding({ ...newSnapshotHolding, holding_id: e.target.value })}
                required
              >
                <option value="">보유자산 선택</option>
                {holdings.filter(h => !h.deleted_at).map((holding) => {
                  const account = accounts.find((a) => a.account_id === holding.account_id);
                  const product = products.find((p) => p.product_id === holding.product_id);
                  return (
                    <option key={holding.holding_id} value={holding.holding_id}>
                      {account?.name || `계좌 ${holding.account_id}`} - {product?.product_name || `상품 ${holding.product_id}`}
                    </option>
                  );
                })}
              </select>
              <input
                type="number"
                step="any"
                placeholder="평가금액"
                value={newSnapshotHolding.valuation_amount}
                onChange={(e) => setNewSnapshotHolding({ ...newSnapshotHolding, valuation_amount: e.target.value })}
                required
              />
              <select
                value={newSnapshotHolding.data_source}
                onChange={(e) => setNewSnapshotHolding({ ...newSnapshotHolding, data_source: e.target.value })}
              >
                <option value="manual">수동입력</option>
                <option value="auto">API연동</option>
                <option value="missing">엑셀업로드</option>
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
                  <th>ID</th>
                  <th>스냅샷일자</th>
                  <th>계좌이름</th>
                  <th>상품이름</th>
                  <th>평가금액</th>
                  <th>데이터소스</th>
                  <th>생성일</th>
                </tr>
              </thead>
              <tbody>
                {snapshotHoldings.map((sh) => {
                  const holding = holdings.find((h) => h.holding_id === sh.holding_id);
                  const account = holding ? accounts.find((a) => a.account_id === holding.account_id) : null;
                  const product = holding ? products.find((p) => p.product_id === holding.product_id) : null;
                  const snapshot = snapshots.find((s) => s.snapshot_id === sh.snapshot_id);
                  return (
                    <tr key={sh.snapshot_holding_id}>
                      <td>{sh.snapshot_holding_id}</td>
                      <td>{snapshot?.reference_date || sh.snapshot_id}</td>
                      <td>{account?.name || holding?.account_id || '-'}</td>
                      <td>{product?.product_name || holding?.product_id || '-'}</td>
                      <td>{sh.valuation_amount}</td>
                      <td>{getDataSourceLabel(sh.data_source)}</td>
                      <td>{new Date(sh.created_at).toLocaleDateString()}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
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
