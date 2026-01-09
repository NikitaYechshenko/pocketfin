import { useEffect, useState } from "react";
import { getPortfolios, createPortfolio, getPortfolioWithAssets, createAsset, deleteAsset } from "../api/testApi";

const styles = {
  section: {
    background: "var(--bg-secondary)",
    border: "1px solid var(--border-color)",
    borderRadius: "12px",
    padding: "1.25rem",
    marginBottom: "1.25rem",
  },
  inputRow: {
    display: "flex",
    gap: "0.5rem",
    flexWrap: "wrap" as const,
    marginBottom: "1rem",
  },
  listItem: {
    display: "flex",
    alignItems: "center",
    gap: "0.75rem",
    padding: "0.75rem",
    borderBottom: "1px solid var(--border-color)",
  },
  listItemLast: {
    borderBottom: "none",
  },
  badge: {
    display: "inline-block",
    padding: "0.2rem 0.5rem",
    borderRadius: "4px",
    fontSize: "0.75rem",
    fontWeight: 500,
    background: "var(--bg-tertiary)",
    color: "var(--text-secondary)",
  },
  badgeBuy: {
    background: "#dcfce7",
    color: "#166534",
  },
  badgeSell: {
    background: "#fee2e2",
    color: "#991b1b",
  },
  logBox: {
    maxHeight: "200px",
    overflow: "auto",
    background: "var(--bg-tertiary)",
    borderRadius: "8px",
    padding: "0.75rem",
    color: "var(--text-secondary)",
  },
  emptyState: {
    padding: "2rem",
    textAlign: "center" as const,
    color: "var(--text-muted)",
  },
};

export default function TestHarness() {
  const [portfolios, setPortfolios] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [selected, setSelected] = useState<number | null>(null);
  const [selectedName, setSelectedName] = useState("");
  const [assets, setAssets] = useState<any[]>([]);
  const [assetForm, setAssetForm] = useState({ symbol: "", amount: "", operation_type: "buy", operation_time: "" });
  const [log, setLog] = useState<string[]>([]);

  useEffect(() => {
    loadPortfolios();
  }, []);

  async function loadPortfolios() {
    try {
      const data = await getPortfolios();
      if (!Array.isArray(data)) {
        setPortfolios([]);
        addLog("⚠ Unexpected response");
      } else {
        setPortfolios(data);
        addLog(`✓ Loaded ${data.length} portfolios`);
      }
    } catch (e: any) {
      setPortfolios([]);
      addLog("✗ " + e.message);
    }
  }

  function addLog(msg: string) {
    const time = new Date().toLocaleTimeString();
    setLog((s) => [`[${time}] ${msg}`, ...s].slice(0, 30));
  }

  async function onCreatePortfolio() {
    if (!name.trim()) return;
    try {
      const p = await createPortfolio(name);
      setName("");
      addLog(`✓ Created "${p.name}"`);
      await loadPortfolios();
    } catch (e: any) {
      addLog("✗ " + e.message);
    }
  }

  async function onSelectPortfolio(id: number, pName: string) {
    setSelected(id);
    setSelectedName(pName);
    try {
      const data = await getPortfolioWithAssets(id);
      setAssets(data.assets ?? []);
      addLog(`✓ Opened "${pName}" (${data.assets?.length || 0} assets)`);
    } catch (e: any) {
      setAssets([]);
      addLog("✗ " + e.message);
    }
  }

  async function onCreateAsset() {
    if (!selected) return addLog("⚠ Select a portfolio first");
    if (!assetForm.symbol.trim()) return addLog("⚠ Symbol required");
    try {
      const payload = { ...assetForm, portfolio_id: selected };
      const a = await createAsset(payload);
      addLog(`✓ Added ${a.symbol}`);
      setAssetForm({ symbol: "", amount: "", operation_type: "buy", operation_time: "" });
      await onSelectPortfolio(selected, selectedName);
    } catch (e: any) {
      addLog("✗ " + e.message);
    }
  }

  async function onDeleteAsset(id: number, symbol: string) {
    if (!selected) return;
    await deleteAsset(id);
    addLog(`✓ Deleted ${symbol}`);
    await onSelectPortfolio(selected, selectedName);
  }

  return (
    <div>
      {/* Portfolios Section */}
      <section style={styles.section}>
        <h2>Portfolios</h2>
        <div style={styles.inputRow}>
          <input
            placeholder="New portfolio name..."
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && onCreatePortfolio()}
            style={{ flex: 1, minWidth: 200 }}
          />
          <button className="primary" onClick={onCreatePortfolio}>Create</button>
          <button onClick={loadPortfolios}>↻ Refresh</button>
        </div>

        {portfolios.length === 0 ? (
          <div style={styles.emptyState}>No portfolios yet</div>
        ) : (
          <div>
            {portfolios.map((p, i) => (
              <div
                key={p.id}
                style={{
                  ...styles.listItem,
                  ...(i === portfolios.length - 1 ? styles.listItemLast : {}),
                  background: selected === p.id ? "var(--bg-tertiary)" : "transparent",
                }}
              >
                <span style={{ flex: 1, fontWeight: 500 }}>{p.name}</span>
                <span style={styles.badge}>#{p.id}</span>
                <button className="small" onClick={() => onSelectPortfolio(p.id, p.name)}>
                  {selected === p.id ? "● Selected" : "Open"}
                </button>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Assets Section */}
      <section style={styles.section}>
        <h2>{selected ? `Assets in "${selectedName}"` : "Assets"}</h2>

        {selected ? (
          <>
            <div style={styles.inputRow}>
              <input
                placeholder="Symbol (e.g. BTC)"
                value={assetForm.symbol}
                onChange={(e) => setAssetForm((s) => ({ ...s, symbol: e.target.value.toUpperCase() }))}
                style={{ width: 100 }}
              />
              <input
                placeholder="Amount"
                type="number"
                step="any"
                value={assetForm.amount}
                onChange={(e) => setAssetForm((s) => ({ ...s, amount: e.target.value }))}
                style={{ width: 120 }}
              />
              <select
                value={assetForm.operation_type}
                onChange={(e) => setAssetForm((s) => ({ ...s, operation_type: e.target.value }))}
              >
                <option value="buy">Buy</option>
                <option value="sell">Sell</option>
              </select>
              <input
                type="date"
                value={assetForm.operation_time}
                onChange={(e) => setAssetForm((s) => ({ ...s, operation_time: e.target.value }))}
              />
              <button className="primary" onClick={onCreateAsset}>+ Add</button>
            </div>

            {assets.length === 0 ? (
              <div style={styles.emptyState}>No assets in this portfolio</div>
            ) : (
              <div>
                {assets.map((a, i) => (
                  <div
                    key={a.id}
                    style={{
                      ...styles.listItem,
                      ...(i === assets.length - 1 ? styles.listItemLast : {}),
                    }}
                  >
                    <span style={{ fontWeight: 600, minWidth: 60 }}>{a.symbol}</span>
                    <span style={{ color: "var(--text-secondary)", minWidth: 100 }}>
                      {Number(a.amount).toLocaleString()}
                    </span>
                    <span
                      style={{
                        ...styles.badge,
                        ...(a.operation_type === "buy" ? styles.badgeBuy : styles.badgeSell),
                      }}
                    >
                      {a.operation_type}
                    </span>
                    <span style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
                      {a.operation_time || "—"}
                    </span>
                    <span style={{ flex: 1 }} />
                    <button className="small danger" onClick={() => onDeleteAsset(a.id, a.symbol)}>
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            )}
          </>
        ) : (
          <div style={styles.emptyState}>Select a portfolio to view assets</div>
        )}
      </section>

      {/* Log Section */}
      <section style={styles.section}>
        <h3>Activity Log</h3>
        <div style={styles.logBox}>
          {log.length === 0 ? (
            <span style={{ color: "var(--text-muted)" }}>No activity yet</span>
          ) : (
            <pre>{log.join("\n")}</pre>
          )}
        </div>
      </section>
    </div>
  );
}
