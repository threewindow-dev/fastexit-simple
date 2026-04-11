export interface SnapshotInputPolicyProduct {
  product_id: number;
  allow_snapshot_input?: boolean;
}

export interface SnapshotInputPolicyAccount {
  account_id: number;
  allow_snapshot_input?: boolean;
}

export interface SnapshotInputPolicyHolding {
  holding_id: number;
  account_id: number;
  product_id: number;
  deleted_at: string | null;
}

export const isProductAllowedForSnapshotInput = (
  product: SnapshotInputPolicyProduct | null | undefined
): boolean => product?.allow_snapshot_input !== false;

export const isAccountAllowedForSnapshotInput = (
  account: SnapshotInputPolicyAccount | null | undefined
): boolean => account?.allow_snapshot_input !== false;

export interface SnapshotInputVisibilityOptions {
  currentValueHoldingIds?: Iterable<number>;
  previousValueHoldingIds?: Iterable<number>;
}

const buildSnapshotPolicyMaps = (
  products: SnapshotInputPolicyProduct[],
  accounts: SnapshotInputPolicyAccount[]
) => ({
  productById: new Map(products.map((product) => [product.product_id, product])),
  accountById: new Map(accounts.map((account) => [account.account_id, account])),
});

export const filterSnapshotInputEligibleHoldings = <T extends SnapshotInputPolicyHolding>(
  holdings: T[],
  products: SnapshotInputPolicyProduct[],
  accounts: SnapshotInputPolicyAccount[]
): T[] => {
  const { productById, accountById } = buildSnapshotPolicyMaps(products, accounts);

  return holdings.filter((holding) => {
    if (holding.deleted_at) {
      return false;
    }
    return (
      isProductAllowedForSnapshotInput(productById.get(holding.product_id))
      && isAccountAllowedForSnapshotInput(accountById.get(holding.account_id))
    );
  });
};

export const filterSnapshotInputVisibleHoldings = <T extends SnapshotInputPolicyHolding>(
  holdings: T[],
  products: SnapshotInputPolicyProduct[],
  accounts: SnapshotInputPolicyAccount[],
  options: SnapshotInputVisibilityOptions = {}
): T[] => {
  const { productById, accountById } = buildSnapshotPolicyMaps(products, accounts);
  const currentValueHoldingIds = new Set(options.currentValueHoldingIds ?? []);
  const previousValueHoldingIds = new Set(options.previousValueHoldingIds ?? []);

  return holdings.filter((holding) => {
    if (holding.deleted_at) {
      return false;
    }

    const isAllowed = (
      isProductAllowedForSnapshotInput(productById.get(holding.product_id))
      && isAccountAllowedForSnapshotInput(accountById.get(holding.account_id))
    );

    return (
      isAllowed
      || currentValueHoldingIds.has(holding.holding_id)
      || previousValueHoldingIds.has(holding.holding_id)
    );
  });
};
