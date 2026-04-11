import { describe, expect, it } from 'vitest';

import {
  filterSnapshotInputEligibleHoldings,
  filterSnapshotInputVisibleHoldings,
  isAccountAllowedForSnapshotInput,
  isProductAllowedForSnapshotInput,
} from './snapshotInputPolicy';

describe('snapshotInputPolicy', () => {
  it('treats missing product policy as allowed for backward compatibility', () => {
    expect(isProductAllowedForSnapshotInput(undefined)).toBe(true);
  });

  it('treats missing account policy as allowed for backward compatibility', () => {
    expect(isAccountAllowedForSnapshotInput(undefined)).toBe(true);
  });

  it('filters out deleted holdings and products/accounts with snapshot input disabled', () => {
    const products = [
      { product_id: 1, allow_snapshot_input: true },
      { product_id: 2, allow_snapshot_input: false },
    ];
    const accounts = [
      { account_id: 101, allow_snapshot_input: true },
      { account_id: 102, allow_snapshot_input: false },
    ];
    const holdings = [
      { holding_id: 10, account_id: 101, product_id: 1, deleted_at: null },
      { holding_id: 11, account_id: 101, product_id: 2, deleted_at: null },
      { holding_id: 12, account_id: 101, product_id: 1, deleted_at: '2026-01-01T00:00:00' },
      { holding_id: 13, account_id: 102, product_id: 1, deleted_at: null },
    ];

    const result = filterSnapshotInputEligibleHoldings(holdings, products, accounts);

    expect(result).toEqual([{ holding_id: 10, account_id: 101, product_id: 1, deleted_at: null }]);
  });

  it('keeps excluded holdings visible when current or previous snapshot values exist', () => {
    const products = [
      { product_id: 1, allow_snapshot_input: true },
      { product_id: 2, allow_snapshot_input: false },
    ];
    const accounts = [{ account_id: 101, allow_snapshot_input: true }];
    const holdings = [
      { holding_id: 10, account_id: 101, product_id: 1, deleted_at: null },
      { holding_id: 11, account_id: 101, product_id: 2, deleted_at: null },
      { holding_id: 12, account_id: 101, product_id: 2, deleted_at: null },
    ];

    const result = filterSnapshotInputVisibleHoldings(holdings, products, accounts, {
      currentValueHoldingIds: [11],
      previousValueHoldingIds: [12],
    });

    expect(result.map((holding) => holding.holding_id)).toEqual([10, 11, 12]);
  });

  it('hides excluded holdings when neither current nor previous values exist', () => {
    const products = [
      { product_id: 1, allow_snapshot_input: true },
      { product_id: 2, allow_snapshot_input: false },
    ];
    const accounts = [{ account_id: 101, allow_snapshot_input: true }];
    const holdings = [
      { holding_id: 10, account_id: 101, product_id: 1, deleted_at: null },
      { holding_id: 11, account_id: 101, product_id: 2, deleted_at: null },
    ];

    const result = filterSnapshotInputVisibleHoldings(holdings, products, accounts);

    expect(result.map((holding) => holding.holding_id)).toEqual([10]);
  });
});
