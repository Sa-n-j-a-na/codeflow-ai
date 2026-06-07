import { Handle, Position } from "reactflow"

// Color per node type
const TYPE_COLORS = {
  component: "#6366f1",
  endpoint:  "#10b981",
  data:      "#f59e0b",
  service:   "#3b82f6",
  database:  "#ef4444",
  default:   "#6366f1"
}

export default function NodeCard({ data }) {
  const color = TYPE_COLORS[data.type] || TYPE_COLORS.default

  return (
    <div style={{
      background: "#1a1a2e",
      border: `2px solid ${color}`,
      borderRadius: "12px",
      padding: "14px 16px",
      minWidth: "200px",
      maxWidth: "240px",
      boxShadow: `0 0 16px ${color}33`,
      position: "relative"
    }}>
      {/* Top connection handle */}
      <Handle
        type="target"
        position={Position.Top}
        style={{ background: color, width: 8, height: 8 }}
      />

      {/* Type badge */}
      <div style={{
        fontSize: "9px",
        color: color,
        textTransform: "uppercase",
        letterSpacing: "1px",
        marginBottom: "6px",
        fontWeight: "bold"
      }}>
        {data.type || "component"}
      </div>

      {/* Label */}
      <div style={{
        color: "white",
        fontWeight: "bold",
        fontSize: "13px",
        marginBottom: "6px",
        lineHeight: "1.3"
      }}>
        {data.label}
      </div>

      {/* Description */}
      {data.description && (
        <div style={{
          color: "#9090b0",
          fontSize: "11px",
          lineHeight: "1.5",
          marginBottom: data.technology ? "8px" : "0"
        }}>
          {data.description}
        </div>
      )}

      {/* Technology tag */}
      {data.technology && (
        <span style={{
          display: "inline-block",
          background: `${color}22`,
          color: color,
          fontSize: "10px",
          padding: "2px 8px",
          borderRadius: "20px",
          marginTop: "4px"
        }}>
          {data.technology}
        </span>
      )}

      {/* Method + path for API nodes */}
      {data.method && (
        <div style={{
          marginTop: "6px",
          display: "flex",
          gap: "4px",
          alignItems: "center"
        }}>
          <span style={{
            background: color,
            color: "white",
            fontSize: "9px",
            padding: "2px 6px",
            borderRadius: "4px",
            fontWeight: "bold"
          }}>
            {data.method}
          </span>
          {data.path && (
            <span style={{
              color: "#6b6b8a",
              fontSize: "10px",
              fontFamily: "monospace"
            }}>
              {data.path}
            </span>
          )}
        </div>
      )}

      {/* Bottom connection handle */}
      <Handle
        type="source"
        position={Position.Bottom}
        style={{ background: color, width: 8, height: 8 }}
      />
    </div>
  )
}