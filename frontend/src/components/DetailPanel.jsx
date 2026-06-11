export default function DetailPanel({ node, onClose }) {
    if (!node) return null
  
    const TYPE_COLORS = {
      component: "#6366f1", service: "#3b82f6",
      database: "#ef4444", storage: "#ef4444",
      external: "#8b5cf6", external_service: "#8b5cf6",
      endpoint: "#10b981", module: "#06b6d4",
      middleware: "#f59e0b", actor: "#64748b",
      datastore: "#ef4444", default: "#6366f1"
    }
  
    const color = TYPE_COLORS[node.data?.type] || "#6366f1"
  
    return (
      <div style={{
        position: "absolute",
        top: 0, right: 0,
        height: "100%",
        zIndex: 20,
        width: "300px",
        background: "#0f0f1e",
        borderLeft: `1px solid ${color}44`,
        padding: "24px 20px",
        overflowY: "auto",
        fontFamily: "Inter, sans-serif",
        boxShadow: "-8px 0 32px #00000066"
      }}>
        {/* Close button */}
        <button onClick={onClose} style={{
          position: "absolute",
          top: "16px", right: "16px",
          background: "#1a1a2e",
          border: "1px solid #2a2a4a",
          borderRadius: "6px",
          color: "#6b6b8a",
          cursor: "pointer",
          width: "28px", height: "28px",
          fontSize: "14px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center"
        }}>
          ✕
        </button>
  
        {/* Type badge */}
        <div style={{
          fontSize: "9px", color: color,
          textTransform: "uppercase",
          letterSpacing: "2px",
          fontWeight: "700",
          marginBottom: "8px"
        }}>
          {node.data?.type}
        </div>
  
        {/* Name */}
        <div style={{
          color: "white", fontWeight: "800",
          fontSize: "18px", lineHeight: "1.3",
          marginBottom: "16px",
          paddingRight: "32px"
        }}>
          {node.data?.label}
        </div>
  
        <div style={{
          height: "1px",
          background: "#1e1e3a",
          marginBottom: "16px"
        }} />
  
        {/* What it does */}
        {node.data?.description && (
          <div style={{ marginBottom: "20px" }}>
            <div style={{
              fontSize: "10px", color: "#4a4a6a",
              textTransform: "uppercase",
              letterSpacing: "1px",
              marginBottom: "6px",
              fontWeight: "700"
            }}>
              What it does
            </div>
            <div style={{
              color: "#9090b0",
              fontSize: "13px",
              lineHeight: "1.7"
            }}>
              {node.data.description}
            </div>
          </div>
        )}
  
        {/* Technology */}
        {node.data?.technology && (
          <div style={{ marginBottom: "20px" }}>
            <div style={{
              fontSize: "10px", color: "#4a4a6a",
              textTransform: "uppercase",
              letterSpacing: "1px",
              marginBottom: "8px",
              fontWeight: "700"
            }}>
              Technology
            </div>
            <div style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "6px"
            }}>
              {node.data.technology.split(",").map((tech, i) => (
                <span key={i} style={{
                  background: `${color}18`,
                  color: color,
                  fontSize: "11px",
                  padding: "4px 10px",
                  borderRadius: "20px",
                  fontWeight: "600"
                }}>
                  {tech.trim()}
                </span>
              ))}
            </div>
          </div>
        )}
  
        {/* Endpoint info for API nodes */}
        {node.data?.method && (
          <div style={{ marginBottom: "20px" }}>
            <div style={{
              fontSize: "10px", color: "#4a4a6a",
              textTransform: "uppercase",
              letterSpacing: "1px",
              marginBottom: "8px",
              fontWeight: "700"
            }}>
              Endpoint
            </div>
            <div style={{
              background: "#1a1a2e",
              borderRadius: "8px",
              padding: "10px 12px",
              display: "flex",
              gap: "8px",
              alignItems: "center"
            }}>
              <span style={{
                background: color,
                color: "white",
                fontSize: "10px",
                padding: "3px 8px",
                borderRadius: "4px",
                fontWeight: "700"
              }}>
                {node.data.method}
              </span>
              <span style={{
                color: "#6b6b8a",
                fontSize: "11px",
                fontFamily: "monospace"
              }}>
                {node.data.path}
              </span>
            </div>
          </div>
        )}
        {/* File path */}
        {node.data?.file_path && (
        <div style={{ marginBottom: "16px" }}>
            <div style={{
            fontSize: "10px", color: "#4a4a6a",
            textTransform: "uppercase",
            letterSpacing: "1px",
            marginBottom: "6px",
            fontWeight: "700"
            }}>
            File Location
            </div>
            <div style={{
            background: "#1a1a2e",
            borderRadius: "6px",
            padding: "8px 12px",
            color: "#6366f1",
            fontSize: "11px",
            fontFamily: "monospace"
            }}>
            {node.data.file_path}
            </div>
        </div>
        )}
      </div>
    )
  }