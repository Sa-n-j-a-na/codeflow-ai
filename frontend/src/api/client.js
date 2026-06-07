import axios from "axios"

// All API calls go to this base URL
const API = axios.create({
  baseURL: "http://localhost:8000/api"
})

// Upload a zip file
export const uploadCodebase = (file, flowType) => {
  const formData = new FormData()
  formData.append("file", file)
  formData.append("flow_type", flowType)
  return API.post("/upload", formData)
}

// Analyze a GitHub repo
export const analyzeGithub = (githubUrl, flowType) => {
  return API.post("/github", {
    github_url: githubUrl,
    flow_type: flowType
  })
}

// Refresh existing analysis
export const refreshFlow = (path, flowType, sourceUrl) =>
  API.post("/refresh", {
    path,
    flow_type: flowType,
    source_url: sourceUrl
  })

// Get available flow types
export const getFlowTypes = () => {
  return API.get("/flow-types")
}