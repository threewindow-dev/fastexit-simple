import { describe, expect, it } from 'vitest';

import {
  filterSnapshotInputEligibleHoldings,
  isProductAllowedForSnapshotInput,
} from './snapshotInputPolicy';

describe('snapshotInputPolicy', () => {
  it('treats missing product policy as allowed for backward compatibility', () => {
    expect(isProductAllowedForSnapshotInput(undefined)).toBe(true);
  });

  it('filters out deleted holdings and products with snapshot input disabled', () => {
    const products = [
      { product_id: 1, allow_snapshot_input: true },
      { product_id: 2, allow_snapshot_input: false },
    ];
    const holdings = [
      { holding_id: 10, product_id: 1, deleted_at: null },
      { holding_id: 11, product_id: 2, deleted_at: null },
      { holding_id: 12, product_id: 1, deleted_at: '2026-01-01T00:00:00' },
    ];

    const result = filterSnapshotInputEligibleHoldings(holdings, products);

    expect(result).toEqual([{ holding_id: 10, product_id: 1, deleted_at: null }]);
  });
});
