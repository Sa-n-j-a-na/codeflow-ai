import { useState } from "react"
import { uploadCodebase, analyzeGithub, refreshFlow } from "../api/client"

export function useFlow() {
  // Store ALL 3 flows
  const [flows, setFlows] = useState({
    system_flow: null,
    api_flow: null,
    data_flow: null
  })

  const [activeTab, setActiveTab] = useState("system_flow")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [meta, setMeta] = useState(null)
  const [lastPath, setLastPath] = useState(null)

  const applyResult = (data) => {
    if (data.error) { setError(data.error); return }
  
    // Filter out failed flows — keep successful ones
    const validFlows = {}
    Object.entries(data.flows).forEach(([key, flow]) => {
      if (!flow.error) {
        validFlows[key] = flow
      } else {
        console.warn(`Flow ${key} failed:`, flow.error)
        // Keep empty so tab shows "failed" state
        validFlows[key] = { nodes: [], edges: [], title: `${key} generation failed`, description: "This flow failed to generate. Try refreshing." }
      }
    })
  
    setFlows(validFlows)
    setMeta(data.meta)
    setError(null)
  }

  const handleGithub = async (url) => {
    setLoading(true)
    setError(null)
    try {
      const res = await analyzeGithub(url, "all")
      setLastPath(res.data.source_path)
      applyResult(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || "GitHub analysis failed")
    }
    setLoading(false)
  }

  const handleUpload = async (file) => {
    setLoading(true)
    setError(null)
    try {
      const res = await uploadCodebase(file, "all")
      setLastPath(res.data.source_path)
      applyResult(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || "Upload failed")
    }
    setLoading(false)
  }

  const handleRefresh = async () => {
    if (!lastPath) { setError("No codebase loaded yet"); return }
    setLoading(true)
    setError(null)
    try {
      const res = await refreshFlow(lastPath, "all")
      applyResult(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || "Refresh failed")
    }
    setLoading(false)
  }

  // Get current active flow data
  const currentFlow = flows[activeTab]

  return {
    flows,
    currentFlow,
    activeTab, setActiveTab,
    loading, error, meta, lastPath,
    handleGithub, handleUpload, handleRefresh
  }
}