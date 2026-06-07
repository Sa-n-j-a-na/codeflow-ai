export default function DiffPanel({ diff }) {
    if (!diff || diff.is_first_run) return null
    if (!diff.has_changes) {
      return (
        <div style={{
          position: "absolute", bottom: 16, right: 16,
          zIndex: 10, background: "#1a1a2e",
          border: "1px solid #10b981",
          borderRadius: "10px", padding: "12px 16px",
          fontSize: "12px", color: "#10b981"
        }}>
          ✅ No architecture changes detected
        </div>
      )
    }
  
    const { nodes, edges, summary, version_from, version_to } = diff
  
    return (
      <div style={{
        position: "absolute", bottom: 16, right: 16,
        zIndex: 10, background: "#1a1a2e",
        border: "1px solid #6366f1",
        borderRadius: "10px", padding: "16px",
        maxWidth: "300px", maxHeight: "400px",
        overflowY: "auto",
        boxShadow: "0 0 20px #6366f133"
      }}>
        {/* Header */}
        <div style={{
          fontSize: "11px", color: "#6366f1",
          fontWeight: "bold", marginBottom: "8px",
          textTransform: "uppercase", letterSpacing: "1px"
        }}>
          🔄 Architecture Changes
        </div>
  
        <div style={{
          fontSize: "12px", color: "#818cf8",
          marginBottom: "12px"
        }}>
          v{version_from} → v{version_to} · {summary}
        </div>
  
        {/* Added nodes */}
        {nodes.added?.length > 0 && (
          <div style={{ marginBottom: "10px" }}>
            <div style={{ fontSize: "10px", color: "#6b6b8a", marginBottom: "4px" }}>
              ADDED
            </div>
            {nodes.added.map((n, i) => (
              <div key={i} style={{
                display: "flex", alignItems: "center",
                gap: "6px", marginBottom: "4px"
              }}>
                <span style={{ color: "#10b981", fontSize: "12px" }}>+</span>
                <span style={{ color: "#10b981", fontSize: "11px", fontWeight: "bold" }}>
                  {n.label}
                </span>
                {n.technology && (
                  <span style={{ color: "#4a4a6a", fontSize: "10px" }}>
                    ({n.technology})
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
  
        {/* Removed nodes */}
        {nodes.removed?.length > 0 && (
          <div style={{ marginBottom: "10px" }}>
            <div style={{ fontSize: "10px", color: "#6b6b8a", marginBottom: "4px" }}>
              REMOVED
            </div>
            {nodes.removed.map((n, i) => (
              <div key={i} style={{
                display: "flex", alignItems: "center",
                gap: "6px", marginBottom: "4px"
              }}>
                <span style={{ color: "#ef4444", fontSize: "12px" }}>−</span>
                <span style={{ color: "#ef4444", fontSize: "11px", fontWeight: "bold" }}>
                  {n.label}
                </span>
              </div>
            ))}
          </div>
        )}
  
        {/* Changed nodes */}
        {nodes.changed?.length > 0 && (
          <div style={{ marginBottom: "10px" }}>
            <div style={{ fontSize: "10px", color: "#6b6b8a", marginBottom: "4px" }}>
              CHANGED
            </div>
            {nodes.changed.map((n, i) => (
              <div key={i} style={{ marginBottom: "6px" }}>
                <div style={{
                  display: "flex", alignItems: "center",
                  gap: "6px"
                }}>
                  <span style={{ color: "#f59e0b", fontSize: "12px" }}>~</span>
                  <span style={{ color: "#f59e0b", fontSize: "11px", fontWeight: "bold" }}>
                    {n.label}
                  </span>
                </div>
                {n.changes.map((c, j) => (
                  <div key={j} style={{
                    color: "#6b6b8a", fontSize: "10px",
                    paddingLeft: "16px", marginTop: "2px"
                  }}>
                    {c}
                  </div>
                ))}
              </div>
            ))}
          </div>
        )}
  
        {/* Added edges */}
        {edges.added?.length > 0 && (
          <div style={{ marginBottom: "10px" }}>
            <div style={{ fontSize: "10px", color: "#6b6b8a", marginBottom: "4px" }}>
              NEW CONNECTIONS
            </div>
            {edges.added.map((e, i) => (
              <div key={i} style={{
                color: "#10b981", fontSize: "10px",
                marginBottom: "2px"
              }}>
                + {e.from} → {e.to}
              </div>
            ))}
          </div>
        )}
      </div>
    )
  }