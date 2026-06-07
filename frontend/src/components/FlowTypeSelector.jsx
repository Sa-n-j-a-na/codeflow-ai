const FLOW_TYPES = [
    { id: "system_flow", label: "⚙️ System Flow" },
    { id: "api_flow",    label: "🔗 API Flow" },
    { id: "data_flow",   label: "📊 Data Flow" },
  ]
  
  export default function FlowTypeSelector({ selected, onChange }) {
    return (
      <div style={{
        display: "flex",
        gap: "8px",
        marginBottom: "16px"
      }}>
        {FLOW_TYPES.map((type) => (
          <button
            key={type.id}
            onClick={() => onChange(type.id)}
            style={{
              flex: 1,
              padding: "8px 4px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              fontSize: "11px",
              fontWeight: selected === type.id ? "bold" : "normal",
              background: selected === type.id ? "#6366f1" : "#1e1e2e",
              color: selected === type.id ? "white" : "#6b6b8a",
              transition: "all 0.2s",
              borderBottom: selected === type.id
                ? "2px solid #818cf8"
                : "2px solid transparent"
            }}
          >
            {type.label}
          </button>
        ))}
      </div>
    )
  }