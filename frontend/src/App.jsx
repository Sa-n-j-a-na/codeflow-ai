import { useState } from "react"
import FlowCanvas from "./components/FlowCanvas"
import { useFlow } from "./hooks/useFlow"

const TABS = [
  { id: "system_flow", label: "⚙️ System Flow" },
  { id: "api_flow",    label: "🔗 API Flow" },
  { id: "data_flow",   label: "📊 Data Flow" },
]

export default function App() {
  const [githubUrl, setGithubUrl] = useState("")
  const [inputTab, setInputTab] = useState("github")

  const {
    currentFlow,
    activeTab, setActiveTab,
    loading, error, meta, lastPath,
    handleGithub, handleUpload, handleRefresh
  } = useFlow()

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "100vh",
      width: "100vw",
      background: "#0d0d1a",
      fontFamily: "Inter, -apple-system, sans-serif",
      overflow: "hidden"
    }}>

      {/* TOP BAR */}
      <div style={{
        display: "flex",
        alignItems: "center",
        gap: "16px",
        padding: "12px 20px",
        background: "#0a0a16",
        borderBottom: "1px solid #1e1e3a",
        flexShrink: 0
      }}>
        {/* Logo */}
        <div style={{
          fontSize: "16px",
          fontWeight: "bold",
          color: "white",
          whiteSpace: "nowrap"
        }}>
          ⚡ CodeFlow AI
        </div>

        <div style={{ width: "1px", height: "24px", background: "#1e1e3a" }} />

        {/* Input type toggle */}
        <div style={{ display: "flex", gap: "4px" }}>
          {["github", "upload"].map(t => (
            <button key={t} onClick={() => setInputTab(t)} style={{
              padding: "6px 12px",
              borderRadius: "6px",
              border: "none",
              cursor: "pointer",
              background: inputTab === t ? "#1e1e3a" : "transparent",
              color: inputTab === t ? "white" : "#4a4a6a",
              fontSize: "12px"
            }}>
              {t === "github" ? "🐙 GitHub" : "📁 Upload"}
            </button>
          ))}
        </div>

        {/* Input area */}
        {inputTab === "github" ? (
          <div style={{ display: "flex", gap: "8px", flex: 1, maxWidth: "500px" }}>
            <input
              type="text"
              placeholder="https://github.com/user/repo"
              value={githubUrl}
              onChange={e => setGithubUrl(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleGithub(githubUrl)}
              style={{
                flex: 1,
                padding: "8px 12px",
                borderRadius: "8px",
                border: "1px solid #1e1e3a",
                background: "#1a1a2e",
                color: "white",
                fontSize: "13px",
                outline: "none"
              }}
            />
            <button
              onClick={() => handleGithub(githubUrl)}
              disabled={loading || !githubUrl.trim()}
              style={{
                padding: "8px 16px",
                background: loading ? "#2a2a4a" : "#6366f1",
                color: loading ? "#4a4a6a" : "white",
                border: "none",
                borderRadius: "8px",
                cursor: loading ? "not-allowed" : "pointer",
                fontSize: "13px",
                fontWeight: "bold",
                whiteSpace: "nowrap"
              }}
            >
              {loading ? "⏳ Analyzing..." : "Analyze →"}
            </button>
          </div>
        ) : (
          <label style={{
            padding: "8px 16px",
            background: "#1a1a2e",
            border: "1px dashed #1e1e3a",
            borderRadius: "8px",
            cursor: "pointer",
            color: "#6b6b8a",
            fontSize: "12px"
          }}>
            <input
              type="file"
              accept=".zip"
              style={{ display: "none" }}
              onChange={e => e.target.files[0] && handleUpload(e.target.files[0])}
            />
            📁 Upload ZIP
          </label>
        )}

        {/* Refresh */}
        <button
          onClick={handleRefresh}
          disabled={loading || !lastPath}
          style={{
            padding: "8px 14px",
            background: "transparent",
            color: lastPath ? "#10b981" : "#2a2a4a",
            border: `1px solid ${lastPath ? "#10b981" : "#1e1e3a"}`,
            borderRadius: "8px",
            cursor: loading || !lastPath ? "not-allowed" : "pointer",
            fontSize: "12px",
            whiteSpace: "nowrap"
          }}
        >
          🔄 Refresh
        </button>

        {/* Meta info */}
        {meta && (
          <div style={{
            marginLeft: "auto",
            fontSize: "11px",
            color: "#4a4a6a"
          }}>
            📄 {meta.files_analyzed} files analyzed
          </div>
        )}
      </div>

      {/* FLOW TYPE TABS */}
      <div style={{
        display: "flex",
        gap: "0",
        padding: "0 20px",
        background: "#0a0a16",
        borderBottom: "1px solid #1e1e3a",
        flexShrink: 0
      }}>
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: "12px 24px",
              border: "none",
              borderBottom: activeTab === tab.id
                ? "2px solid #6366f1"
                : "2px solid transparent",
              background: "transparent",
              color: activeTab === tab.id ? "#818cf8" : "#4a4a6a",
              cursor: "pointer",
              fontSize: "13px",
              fontWeight: activeTab === tab.id ? "bold" : "normal",
              transition: "all 0.15s"
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* ERROR BANNER */}
      {error && (
        <div style={{
          background: "#2d1b1b",
          borderBottom: "1px solid #ef4444",
          color: "#ef4444",
          padding: "8px 20px",
          fontSize: "12px",
          flexShrink: 0
        }}>
          ⚠️ {error}
        </div>
      )}

      {/* LOADING BANNER */}
      {loading && (
        <div style={{
          background: "#1a1a2e",
          borderBottom: "1px solid #6366f1",
          color: "#818cf8",
          padding: "8px 20px",
          fontSize: "12px",
          textAlign: "center",
          flexShrink: 0
        }}>
          ⏳ Generating all 3 flow diagrams — this takes about 30-60 seconds...
        </div>
      )}

      {/* MAIN CANVAS */}
      <div style={{ flex: 1, overflow: "hidden" }}>
        <FlowCanvas
          nodes={currentFlow?.nodes || []}
          edges={currentFlow?.edges || []}
          flowTitle={currentFlow?.title}
          flowDescription={currentFlow?.description}
        />
      </div>

    </div>
  )
}