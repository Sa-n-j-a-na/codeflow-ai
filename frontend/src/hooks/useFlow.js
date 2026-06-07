import { useState } from "react"
import { uploadCodebase, analyzeGithub, refreshFlow } from "../api/client"

export function useFlow() {
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
  const [lastSourceUrl, setLastSourceUrl] = useState(null)
  const [diff, setDiff] = useState(null)

  const applyResult = (data) => {
    if (data.error) {
      setError(data.error)
      return
    }

    const validFlows = {}
    Object.entries(data.flows).forEach(([key, flow]) => {
      if (!flow.error) {
        validFlows[key] = flow
      } else {
        console.warn(`Flow ${key} failed:`, flow.error)
        validFlows[key] = {
          nodes: [],
          edges: [],
          title: `${key} generation failed`,
          description: "This flow failed to generate. Try refreshing."
        }
      }
    })

    setFlows(validFlows)
    setMeta(data.meta)
    setDiff(data.diff || null)
    setError(null)
  }

  const handleGithub = async (githubUrl) => {
    setLoading(true)
    setError(null)
    try {
      const res = await analyzeGithub(githubUrl, "all")
      setLastPath(res.data.source_path)
      setLastSourceUrl(githubUrl)
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
      setLastSourceUrl(`upload_${file.name}`)
      applyResult(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || "Upload failed")
    }
    setLoading(false)
  }

  const handleRefresh = async () => {
    if (!lastPath) {
      setError("No codebase loaded yet")
      return
    }
    setLoading(true)
    setError(null)
    try {
      const res = await refreshFlow(lastPath, "all", lastSourceUrl)
      applyResult(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || "Refresh failed")
    }
    setLoading(false)
  }

  const currentFlow = flows[activeTab]

  return {
    flows,
    currentFlow,
    activeTab, setActiveTab,
    loading, error, meta,
    lastPath, lastSourceUrl,
    diff,
    handleGithub, handleUpload, handleRefresh
  }
}