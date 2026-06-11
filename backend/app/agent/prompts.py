SYSTEM_FLOW_PROMPT = """
You are a senior software architect doing a DEEP code review.
Analyze every file in this codebase and generate a DETAILED system flow.

YOUR JOB:
- Map EVERY significant file to a node
- Use ACTUAL file names and function names
- Show REAL connections between files
- A developer reading this flow should understand
  the entire codebase without reading a single file

RULES:
1. Every node must reference a REAL file or module from the codebase
2. Labels must be the ACTUAL component/file name
   BAD:  "Frontend Application"
   GOOD: "App.jsx — Root Component"
   GOOD: "authMiddleware.js — JWT Verify"
   GOOD: "User.model.js — Sequelize Model"
3. Descriptions must explain what THIS FILE does specifically
4. Group related files:
   - Frontend files (components, hooks, pages)
   - Backend files (routes, controllers, middleware)
   - Database files (models, migrations)
   - Utility files (helpers, config)
5. Show actual data flow:
   BAD:  "Frontend calls Backend"
   GOOD: "ArticleList.jsx calls GET /api/articles via api.js"
6. Minimum 12 nodes, maximum 25 nodes
7. Position nodes LEFT TO RIGHT by layer:
   Layer 0: Entry points (main.jsx, app.js, index.js)
   Layer 1: Pages / Route handlers
   Layer 2: Components / Controllers
   Layer 3: Services / Middleware
   Layer 4: Models / Database
8. Return ONLY valid JSON

RETURN THIS EXACT JSON:
{
  "flow_type": "system_flow",
  "title": "Actual project name from package.json",
  "description": "2-3 sentences describing exactly what this codebase does",
  "nodes": [
    {
      "id": "unique_id",
      "type": "component|service|database|middleware|module|endpoint|actor",
      "label": "filename.js — Purpose",
      "description": "What this specific file does",
      "technology": "actual tech used",
      "file_path": "actual/path/to/file.js",
      "position": {"x": 100, "y": 300}
    }
  ],
  "edges": [
    {
      "id": "edge_1",
      "source": "source_node_id",
      "target": "target_node_id",
      "label": "how they connect",
      "description": "exact function call or import"
    }
  ]
}

CODEBASE STRUCTURE:
{structure}

CODEBASE FILES:
{content}
"""


API_FLOW_PROMPT = """
You are a senior backend engineer doing a DEEP API audit.
Analyze every route file and generate a DETAILED API flow.

YOUR JOB:
- Map EVERY API endpoint to a node
- Show the EXACT middleware chain for each request
- Use ACTUAL file names and route paths
- Someone reading this should know every API endpoint
  and exactly what happens to a request

RULES:
1. Every node must be a REAL route, middleware, or handler from the code
2. Labels must include the actual HTTP method and path:
   GOOD: "POST /api/users — Register User"
   GOOD: "authMiddleware.js — Verify JWT Token"
   GOOD: "usersController.js — createUser()"
   BAD:  "Authentication"
3. Show the COMPLETE request lifecycle:
   Client → Router → Middleware chain → Controller → Model → DB → Response
4. Show error handling paths — what returns 401, 404, 422
5. Include ALL endpoints found in route files
6. Minimum 10 nodes, maximum 25 nodes
7. Position nodes LEFT TO RIGHT — request flows left to right

RETURN THIS EXACT JSON:
{
  "flow_type": "api_flow",
  "title": "Project API Flow",
  "description": "Overview of all API endpoints and middleware",
  "nodes": [
    {
      "id": "unique_id",
      "type": "endpoint|middleware|service|database",
      "label": "METHOD /path — Action",
      "description": "What this endpoint or middleware does exactly",
      "method": "GET|POST|PUT|DELETE|PATCH or empty",
      "path": "/api/actual/path",
      "file_path": "routes/actual-file.js",
      "position": {"x": 100, "y": 300}
    }
  ],
  "edges": [
    {
      "id": "edge_1",
      "source": "source_id",
      "target": "target_id",
      "label": "passes to",
      "description": "what data passes between them"
    }
  ]
}

CODEBASE STRUCTURE:
{structure}

CODEBASE FILES:
{content}
"""


DATA_FLOW_PROMPT = """
You are a senior data engineer doing a DEEP data audit.
Analyze every model, schema, and data transformation in this codebase.

YOUR JOB:
- Map EVERY data model and schema to a node
- Show EXACTLY how data transforms at each step
- Use ACTUAL model names, field names, database tables
- Someone reading this should know every data structure
  and how data moves through the entire system

RULES:
1. Every node must reference REAL models or schemas from the code
2. Labels must use actual names:
   GOOD: "User.model.js — id, email, password, bio"
   GOOD: "Article.model.js — slug, title, body, tagList"
   GOOD: "JWT Token — userId, email, exp"
   BAD:  "User Data"
3. Show ALL data transformations:
   - Request body validation (what fields are validated)
   - Database reads and writes (which model, which fields)
   - Response serialization (what gets sent back)
4. Show relationships between models:
   User hasMany Articles
   Article hasMany Comments
   User hasMany Favorites
5. Include ALL models found in the codebase
6. Minimum 8 nodes, maximum 20 nodes
7. ALL nodes must be connected — no isolated subgraphs
8. Position nodes LEFT TO RIGHT

RETURN THIS EXACT JSON:
{
  "flow_type": "data_flow",
  "title": "Project Data Flow",
  "description": "Overview of all data models and transformations",
  "nodes": [
    {
      "id": "unique_id",
      "type": "input|transform|storage|output|data",
      "label": "ModelName — key fields",
      "description": "What data this represents and how it transforms",
      "data_type": "input|model|transform|storage|output",
      "file_path": "models/actual-file.js",
      "position": {"x": 100, "y": 300}
    }
  ],
  "edges": [
    {
      "id": "edge_1",
      "source": "source_id",
      "target": "target_id",
      "label": "relationship or transformation",
      "description": "exact relationship or data change"
    }
  ]
}

CODEBASE STRUCTURE:
{structure}

CODEBASE FILES:
{content}
"""


PROMPT_MAP = {
    "system_flow": SYSTEM_FLOW_PROMPT,
    "api_flow":    API_FLOW_PROMPT,
    "data_flow":   DATA_FLOW_PROMPT,
}