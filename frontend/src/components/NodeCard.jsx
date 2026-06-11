import { Handle, Position } from "reactflow"

const TYPE_COLORS = {
  component:        "#6366f1",
  service:          "#3b82f6",
  database:         "#ef4444",
  storage:          "#ef4444",
  external:         "#8b5cf6",
  external_service: "#8b5cf6",
  endpoint:         "#10b981",
  module:           "#06b6d4",
  middleware:       "#f59e0b",
  cache:            "#f59e0b",
  queue:            "#ec4899",
  input:            "#10b981",
  output:           "#6366f1",
  transform:        "#06b6d4",
  actor:            "#64748b",
  datastore:        "#ef4444",
  default:          "#6366f1"
}

const TYPE_SHAPES = {
  database:  "cylinder",
  storage:   "cylinder",
  datastore: "cylinder",
  actor:     "circle",
  default:   "rect"
}

export default function NodeCard({ data, selected }) {
  const color = TYPE_COLORS[data.type] || TYPE_COLORS.default
  const shape = TYPE_SHAPES[data.type] || TYPE_SHAPES.default

  const baseStyle = {
    background: `${color}15`,
    border: `2px solid ${color}`,
    fontFamily: "Inter, sans-serif",
    cursor: "pointer",
    transition: "all 0.2s",
    boxShadow: selected
      ? `0 0 0 3px ${color}55, 0 8px 24px ${color}33`
      : `0 2px 12px ${color}22`,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "14px 16px",
    minWidth: "120px",
    maxWidth: "150px",
    textAlign: "center",
    position: "relative"
  }

  const shapeStyle = shape === "cylinder" ? {
    ...baseStyle,
    borderRadius: "8px",
    borderTop: `4px solid ${color}`,
    borderBottom: `4px solid ${color}`,
  } : shape === "circle" ? {
    ...baseStyle,
    borderRadius: "50%",
    width: "100px",
    height: "100px",
    minWidth: "100px",
    padding: "8px"
  } : {
    ...baseStyle,
    borderRadius: "12px"
  }

  return (
    <div style={shapeStyle}>
      <Handle
        type="target"
        position={Position.Left}
        style={{
          background: color,
          width: 8, height: 8,
          border: "2px solid #0d0d1a"
        }}
      />

      {/* Short label only — no description */}
      <div style={{
        color: "#ffffff",
        fontWeight: "700",
        fontSize: "12px",
        lineHeight: "1.3",
        marginBottom: data.technology ? "6px" : "0"
      }}>
        {data.label}
      </div>

      {/* One tech tag max */}
      {data.technology && (
        <div style={{
          background: `${color}25`,
          color: color,
          fontSize: "9px",
          padding: "2px 7px",
          borderRadius: "20px",
          fontWeight: "600",
          maxWidth: "130px",
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap"
        }}>
          {data.technology.split(",")[0].trim()}
        </div>
      )}

      {/* Method badge for API nodes */}
      {data.method && (
        <div style={{
          background: color,
          color: "white",
          fontSize: "9px",
          padding: "2px 7px",
          borderRadius: "4px",
          fontWeight: "700",
          marginTop: "4px"
        }}>
          {data.method}
        </div>
      )}

      {/* File path — shows actual file */}
      {data.file_path && (
        <div style={{
          color: "#3d3d6d",
          fontSize: "8px",
          fontFamily: "monospace",
          marginTop: "4px",
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
          maxWidth: "130px"
        }}>
          {data.file_path}
        </div>
      )}

      <Handle
        type="source"
        position={Position.Right}
        style={{
          background: color,
          width: 8, height: 8,
          border: "2px solid #0d0d1a"
        }}
      />
    </div>
  )
}