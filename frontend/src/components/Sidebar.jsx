import { useState } from "react"
import FlowTypeSelector from "./FlowTypeSelector"

export default function Sidebar({
  onUpload,
  onGithub,
  onRefresh,
  loading,
  flowType,
  setFlowType,
  lastPath,
  flowMeta
}) {
  const [githubUrl, setGithubUrl] = useState("")
  const [tab, setTab] = useState("github")

  const handleGithubSubmit = () => {
    if (githubUrl.trim()) {
      onGithub(githubUrl.trim())
    }
  }

  return (
    <div style={{
      width: "280px",
      minWidth: "280px",
      background: "#0a0a16",
      borderRight: "1px solid #1e1e3a",
      padding: "20px",
      display: "flex",
      flexDirection: "column",
      gap: "16px",
      overflowY: "auto",
      height: "100vh"
    }}>
      {/* Logo */}
      <div>
        <div style={{
          fontSize: "20px",
          fontWeight: "bold",
          color: "white",
          marginBottom: "4px"
        }}>
          ⚡ CodeFlow AI
        </div>
        <div style={{ fontSize: "11px", color: "#4a4a6a" }}>
          Understand any codebase visually
        </div>
      </div>

      <hr style={{ border: "none", borderTop: "1px solid #1e1e3a" }} />

      {/* Flow type selector */}
      <div>
        <div style={{
          fontSize: "11px",
          color: "#4a4a6a",
          marginBottom: "8px",
          textTransform: "uppercase",
          letterSpacing: "1px"
        }}>
          Flow Type
        </div>
        <FlowTypeSelector selected={flowType} onChange={setFlowType} />
      </div>

      {/* Tab switcher */}
      <div style={{ display: "flex", gap: "8px" }}>
        {["github", "upload"].map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            style={{
              flex: 1,
              padding: "8px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              background: tab === t ? "#6366f1" : "#1e1e2e",
              color: tab === t ? "white" : "#6b6b8a",
              fontSize: "12px",
              fontWeight: tab === t ? "bold" : "normal"
            }}
          >
            {t === "github" ? "🐙 GitHub" : "📁 Upload"}
          </button>
        ))}
      </div>

      {/* GitHub tab */}
      {tab === "github" && (
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          <input
            type="text"
            placeholder="https://github.com/user/repo"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleGithubSubmit()}
            style={{
              padding: "10px 12px",
              borderRadius: "8px",
              border: "1px solid #1e1e3a",
              background: "#1a1a2e",
              color: "white",
              fontSize: "12px",
              outline: "none"
            }}
          />
          <button
            onClick={handleGithubSubmit}
            disabled={loading || !githubUrl.trim()}
            style={{
              padding: "10px",
              background: loading ? "#2a2a4a" : "#6366f1",
              color: loading ? "#4a4a6a" : "white",
              border: "none",
              borderRadius: "8px",
              cursor: loading ? "not-allowed" : "pointer",
              fontSize: "13px",
              fontWeight: "bold"
            }}
          >
            {loading ? "⏳ Analyzing..." : "Analyze Repo →"}
          </button>
        </div>
      )}

      {/* Upload tab */}
      {tab === "upload" && (
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          <label style={{
            padding: "20px",
            border: "2px dashed #1e1e3a",
            borderRadius: "8px",
            textAlign: "center",
            cursor: "pointer",
            color: "#4a4a6a",
            fontSize: "12px",
            lineHeight: "1.6"
          }}>
            <input
              type="file"
              accept=".zip"
              style={{ display: "none" }}
              onChange={(e) => e.target.files[0] && onUpload(e.target.files[0])}
            />
            📁 Click to upload<br />
            <span style={{ fontSize: "10px" }}>
              Zip your project first<br />
              (excludes node_modules, venv)
            </span>
          </label>
        </div>
      )}

      <hr style={{ border: "none", borderTop: "1px solid #1e1e3a" }} />

      {/* Refresh button */}
      <button
        onClick={onRefresh}
        disabled={loading || !lastPath}
        style={{
          padding: "10px",
          background: lastPath ? "#0f4c35" : "#1a1a2e",
          color: lastPath ? "#10b981" : "#4a4a6a",
          border: `1px solid ${lastPath ? "#10b981" : "#1e1e3a"}`,
          borderRadius: "8px",
          cursor: loading || !lastPath ? "not-allowed" : "pointer",
          fontSize: "13px",
          fontWeight: "bold"
        }}
      >
        🔄 Refresh Flow
      </button>

      {/* Flow metadata */}
      {flowMeta && (
        <div style={{
          background: "#1a1a2e",
          borderRadius: "8px",
          padding: "12px",
          border: "1px solid #1e1e3a"
        }}>
          <div style={{
            fontSize: "12px",
            fontWeight: "bold",
            color: "white",
            marginBottom: "6px"
          }}>
            {flowMeta.title}
          </div>
          <div style={{
            fontSize: "11px",
            color: "#6b6b8a",
            lineHeight: "1.5",
            marginBottom: "8px"
          }}>
            {flowMeta.description}
          </div>
          {flowMeta.filesAnalyzed && (
            <div style={{
              fontSize: "10px",
              color: "#4a4a6a"
            }}>
              📄 {flowMeta.filesAnalyzed} files analyzed
            </div>
          )}
        </div>
      )}

      {/* Bottom credit */}
      <div style={{
        marginTop: "auto",
        fontSize: "10px",
        color: "#2a2a4a",
        textAlign: "center"
      }}>
        Powered by Gemini 2.5 Flash
      </div>
    </div>
  )
}