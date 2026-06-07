SYSTEM_FLOW_PROMPT = """
You are a senior software architect with 15 years of experience.
Analyze the codebase below and generate a SYSTEM FLOW diagram.

YOUR JOB:
- Identify all major components, services, and modules
- Understand what each component does in plain English
- Find how they connect and communicate
- Show the overall architecture clearly

RULES:
1. Labels must be human readable — not variable names
2. Descriptions must explain WHAT it does, not HOW
3. Every node needs a clear description
4. Return ONLY valid JSON — no markdown, no explanation
5. Minimum 5 nodes, maximum 20 nodes
6. 5. Position nodes LEFT TO RIGHT as main flow direction
   - Start nodes at x=100, y=300
   - Each next layer adds 300 to x
   - Branch nodes go above/below main line (y ± 150)
   - Keep x spacing at 300, y spacing at 150
   - This creates a clean horizontal flow diagram

RETURN THIS EXACT JSON STRUCTURE:
{
  "flow_type": "system_flow",
  "title": "Short descriptive title",
  "description": "2-3 sentence plain English overview of this system",
  "nodes": [
    {
      "id": "node_1",
      "type": "component",
      "label": "Human Readable Name",
      "description": "What this component does in plain English",
      "technology": "Python / React / PostgreSQL etc",
      "position": {"x": 100, "y": 100}
    }
  ],
  "edges": [
    {
      "id": "edge_1",
      "source": "node_1",
      "target": "node_2",
      "label": "calls",
      "description": "What data or action flows between these"
    }
  ]
}

CODEBASE STRUCTURE:
{structure}

CODEBASE CONTENT:
{content}
"""


API_FLOW_PROMPT = """
You are a senior backend engineer with 15 years of experience.
Analyze the codebase below and generate an API FLOW diagram.

YOUR JOB:
- Find all API endpoints and routes
- Show the complete request to response journey
- Include middleware, validation, authentication steps
- Show what happens at each step in plain English

RULES:
1. Labels must be human readable
2. Show the flow from client request to final response
3. Include error handling paths if visible
4. Return ONLY valid JSON — no markdown, no explanation
5. Minimum 5 nodes, maximum 20 nodes

RETURN THIS EXACT JSON STRUCTURE:
{
  "flow_type": "api_flow",
  "title": "Short descriptive title",
  "description": "2-3 sentence plain English overview of the API flow",
  "nodes": [
    {
      "id": "node_1",
      "type": "endpoint",
      "label": "Human Readable Name",
      "description": "What happens at this step",
      "method": "GET or POST or PUT or DELETE or empty",
      "path": "/api/path or empty",
      "position": {"x": 100, "y": 100}
    }
  ],
  "edges": [
    {
      "id": "edge_1",
      "source": "node_1",
      "target": "node_2",
      "label": "sends request",
      "description": "What data moves between these steps"
    }
  ]
}

CODEBASE STRUCTURE:
{structure}

CODEBASE CONTENT:
{content}
"""


DATA_FLOW_PROMPT = """
You are a senior data engineer with 15 years of experience.
Analyze the codebase below and generate a DATA FLOW diagram.

YOUR JOB:
- Find all data models, databases, storage systems
- Show how data enters the system
- Show how data transforms at each step
- Show where data is stored and retrieved

RULES:
1. Labels must be human readable
2. Focus on data movement not code execution
3. Show transformations clearly
4. Return ONLY valid JSON — no markdown, no explanation
5. Minimum 5 nodes, maximum 20 nodes

RETURN THIS EXACT JSON STRUCTURE:
{
  "flow_type": "data_flow",
  "title": "Short descriptive title",
  "description": "2-3 sentence plain English overview of data flow",
  "nodes": [
    {
      "id": "node_1",
      "type": "data",
      "label": "Human Readable Name",
      "description": "What data lives here or what transformation happens",
      "data_type": "input or storage or transform or output",
      "position": {"x": 100, "y": 100}
    }
  ],
  "edges": [
    {
      "id": "edge_1",
      "source": "node_1",
      "target": "node_2",
      "label": "transforms to",
      "description": "How the data changes between these steps"
    }
  ]
}

CODEBASE STRUCTURE:
{structure}

CODEBASE CONTENT:
{content}
"""


# Map flow type string to prompt template
PROMPT_MAP = {
    "system_flow": SYSTEM_FLOW_PROMPT,
    "api_flow": API_FLOW_PROMPT,
    "data_flow": DATA_FLOW_PROMPT,
}