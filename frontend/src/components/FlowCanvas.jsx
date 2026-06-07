import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState
} from "reactflow"
import "reactflow/dist/style.css"
import { useEffect } from "react"
import NodeCard from "./NodeCard"

// Outside component — React Flow requires this
const nodeTypes = { custom: NodeCard }

export default function FlowCanvas({ nodes: rawNodes, edges: rawEdges, flowTitle, flowDescription }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  useEffect(() => {
    if (!rawNodes?.length) return

    const mappedNodes = rawNodes.map(node => ({
      id: node.id,
      type: "custom",
      position: node.position || { x: 0, y: 0 },
      data: {
        label: node.label,
        description: node.description,
        type: node.type,
        technology: node.technology,
        method: node.method,
        path: node.path,
        data_type: node.data_type
      }
    }))

    const mappedEdges = rawEdges.map(edge => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      animated: true,
      style: { stroke: "#6366f1", strokeWidth: 2 },
      labelStyle: { fill: "#9090b0", fontSize: 10 },
      labelBgStyle: { fill: "#1a1a2e", fillOpacity: 0.9 },
      labelBgPadding: [4, 8],
      labelBgBorderRadius: 4
    }))

    setNodes(mappedNodes)
    setEdges(mappedEdges)

  }, [rawNodes, rawEdges])

  if (!rawNodes?.length) {
    return (
      <div style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "#0d0d1a",
        gap: "12px"
      }}>
        <div style={{ fontSize: "40px" }}>⚡</div>
        <div style={{ color: "white", fontSize: "18px", fontWeight: "bold" }}>
          Ready to analyze
        </div>
        <div style={{ color: "#4a4a6a", fontSize: "13px", textAlign: "center" }}>
          Paste a GitHub URL above and click Analyze<br />
          All 3 diagrams generate in one shot
        </div>
      </div>
    )
  }

  return (
    <div style={{ width: "100%", height: "100%", position: "relative" }}>
      {flowTitle && (
        <div style={{
          position: "absolute",
          top: 16, left: 16,
          zIndex: 10,
          background: "#1a1a2eee",
          border: "1px solid #1e1e3a",
          borderRadius: "10px",
          padding: "12px 16px",
          maxWidth: "360px",
          backdropFilter: "blur(8px)"
        }}>
          <div style={{
            color: "white",
            fontWeight: "bold",
            fontSize: "13px",
            marginBottom: "4px"
          }}>
            {flowTitle}
          </div>
          <div style={{
            color: "#6b6b8a",
            fontSize: "11px",
            lineHeight: "1.5"
          }}>
            {flowDescription}
          </div>
        </div>
      )}

      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.1}
        maxZoom={2}
      >
        <Background color="#1e1e3a" gap={24} size={1} />
        <Controls style={{
          background: "#1a1a2e",
          border: "1px solid #1e1e3a",
          borderRadius: "8px"
        }} />
        <MiniMap
          nodeColor="#6366f1"
          maskColor="#0d0d1a99"
          style={{
            background: "#1a1a2e",
            border: "1px solid #1e1e3a",
            borderRadius: "8px"
          }}
        />
      </ReactFlow>
    </div>
  )
}