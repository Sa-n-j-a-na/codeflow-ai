ARCHITECTURE_DISCOVERY_PROMPT = """
You are a Principal Software Architect.

Your task is NOT to generate diagrams.

Your task is to understand the codebase.

Analyze:

1. What business problem this software solves
2. Major features
3. Major workflows
4. Major services
5. Data entities
6. External systems
7. Entry points
8. User journeys

IMPORTANT:

Do NOT use filenames as features.

Think like an architect.

BAD:

Feature:
auth.py

GOOD:

Feature:
User Authentication

Return ONLY valid JSON.

{
  "project_type": "",
  "project_summary": "",

  "features": [],

  "user_journeys": [],

  "services": [],

  "data_entities": [],

  "external_systems": [],

  "entry_points": []
}

==================================================
CODEBASE STRUCTURE
==================================================

{structure}

==================================================
CODEBASE FILES
==================================================

{content}
"""

SYSTEM_FLOW_PROMPT = """
You are a Principal Software Architect performing a DEEP codebase analysis.

Your task is to generate a TRUE SYSTEM FLOW DIAGRAM that explains:

What the application does.
How users interact with it.
How requests move through the system.
Which REAL files implement each capability.

DO NOT generate:

❌ File dependency graphs
❌ Import graphs
❌ Folder trees
❌ One node per file

Instead generate:

✅ Business workflow diagram
✅ User journey diagram
✅ System capability diagram

Every node must represent a REAL business capability
implemented by REAL files.

Read:

Folder structure
Source files
Imports
Routes
Controllers
Services
Models
Database code
External API integrations

Determine:

Core features
User workflows
Business responsibilities
System boundaries

Group files into meaningful capabilities.

BAD:

App.jsx
axios.js
parser.py
auth.js

GOOD:

User Authentication
Resume Upload
Resume Analysis
Skill Gap Detection
Learning Recommendation Engine
Interview Simulator
Job Matching
Dashboard

Each capability MUST be backed by real files.

Determine primary application workflows.

Example:

User
→ Upload Resume
→ Resume Processing
→ Skill Extraction
→ Skill Gap Detection
→ Recommendation Engine
→ Dashboard

Another example:

User
→ Start Interview
→ Question Generation
→ Answer Evaluation
→ Feedback Generation
→ Results Dashboard

Nodes represent:

Actors
Business capabilities
Services
Databases
External APIs
Workflows

CRITICAL:

Nodes DO NOT represent individual files.

NEVER create nodes using filenames.

BAD:

upload.py
parser.py
github.py
main.py
routes.py
helpers.py

BAD NODE EXAMPLES:

{
"label":"parser.py"
}

{
"label":"github.py"
}

GOOD NODE EXAMPLES:

{
"label":"Repository Intake"
}

{
"label":"Static Analysis Engine"
}

{
"label":"Architecture Discovery"
}

{
"label":"Flow Generation Engine"
}

{
"label":"Architecture Store"
}

{
"label":"Drift Detection Engine"
}

Node labels MUST describe:

Business capabilities
Processing capabilities
Services
Workflows
Databases
Actors
External systems

A filename may only appear inside the "files" field.

Never use a filename as a node label.

Every node MUST include:

"id"
"label"
"type"
"description"
"technology"
"files"

Example:

{
"id":"architecture_engine",

"label":"Architecture Discovery",

"type":"service",

"technology":"Gemini + AST",

"description":"Discovers project architecture and system boundaries",

"files":[
"agent/tools/architecture_extractor.py"
]
}

Only use files that actually exist.

Never invent filenames.

Detect and include:

OpenAI
Gemini
Claude
AWS
Azure
Google APIs
Stripe
MongoDB
PostgreSQL
Redis
Elasticsearch
Third-party APIs

when present in the code.

Minimum: 6

Maximum: 15

Prefer concise architecture over excessive detail.

Show real execution flow.
Show user interactions.
Show database interactions.
Show external services.
Show major processing steps.
Group related files together.
Use business terminology.
Avoid technical jargon where possible.
Left-to-right flow.
Every node must contribute to the workflow.

actor
workflow
component
service
database
external

{
"id": "resume_analysis",

"type": "component",

"label": "Resume Analysis Engine",

"technology": "Python",

"description": "Extracts skills, education and experience from uploaded resumes",

"files": [
"backend/parser/resume_parser.py",
"backend/services/skill_extractor.py",
"backend/utils/resume_utils.py"
],

"position": {
"x": 500,
"y": 300
}
}

Edges represent:

User actions
Data movement
Service invocation
Database access
External API calls

Example:

{
"id": "e1",

"source": "resume_upload",

"target": "resume_analysis",

"label": "Uploaded Resume",

"description": "Resume submitted for analysis"
}

The purpose of the diagram is to explain
HOW THE SYSTEM WORKS.

Do NOT explain how files relate.

Explain how capabilities relate.

Prefer architecture-level nodes.

GOOD:

User
Repository Intake
Static Analysis Engine
Architecture Discovery
Flow Generation Engine
Architecture Store
Drift Detection Engine

BAD:

main.py
parser.py
routes.py
utils.py
helpers.py

A capability node should normally contain
1 to 10 related files.

Group related files together.

The diagram should be understandable
to an engineering manager who has never
seen the codebase before.

{
"flow_type": "system_flow",

"title": "Project Name",

"description": "What the system does",

"nodes": [],

"edges": []
}

The following architecture summary was generated
from a dedicated architecture analysis phase.

Use it as your PRIMARY source of truth.

{architecture_context}

==================================================

{structure}

{content}
"""

API_FLOW_PROMPT = """
You are a Senior Backend Architect.

Analyze the codebase and generate a REAL API FLOW.

IMPORTANT:

Do NOT generate file dependency graphs.

The diagram must show:

Client
→ Endpoint
→ Middleware
→ Service
→ Database
→ Response

==================================================
RULES
==================================================

1. Primary nodes must be API endpoints.

2. Group internal files into services.

3. Show middleware chain.

4. Show authentication flow.

5. Show validation flow.

6. Show database interactions.

7. Show external APIs.

8. Show response generation.

9. Include error paths where obvious.

10. Maximum 20 nodes.

==================================================
EXAMPLE
==================================================

User
 ↓

POST /resume/upload
 ↓

Resume Processing Service
 ↓

Resume Analysis Engine
 ↓

Database
 ↓

Response

==================================================
RETURN ONLY VALID JSON
==================================================

{
  "flow_type": "api_flow",

  "title": "API Flow",

  "description": "Request lifecycle",

  "nodes": [
    {
      "id": "upload_endpoint",

      "type": "endpoint",

      "label": "POST /api/upload",

      "description": "Upload resume endpoint",

      "files": [
        "routes/upload.py",
        "controllers/upload_controller.py"
      ],

      "position": {
        "x": 200,
        "y": 200
      }
    }
  ],

  "edges": [
    {
      "id": "e1",

      "source": "upload_endpoint",

      "target": "analysis_service",

      "label": "Pass resume",

      "description": "Resume data forwarded"
    }
  ]
}

==================================================
ARCHITECTURE DISCOVERY
==================================================

The following architecture summary was generated
from a dedicated architecture analysis phase.

Use it as your PRIMARY source of truth.

{architecture_context}

==================================================

==================================================
CODEBASE STRUCTURE
==================================================

{structure}

==================================================
CODEBASE FILES
==================================================

{content}
"""

DATA_FLOW_PROMPT = """
You are a Senior Data Architect.

Analyze the codebase and generate a DATA FLOW DIAGRAM.

IMPORTANT:

Focus on DATA.

Do NOT focus on files.

Do NOT create nodes for source files.

==================================================
GOAL
==================================================

Explain:

Where data originates.

How it is transformed.

Where it is stored.

How it is returned.

==================================================
EXAMPLE
==================================================

Resume PDF
 ↓

Parsed Resume Data
 ↓

Extracted Skills
 ↓

Skill Gap Results
 ↓

Learning Path
 ↓

Dashboard Response

==================================================
RULES
==================================================

1. Nodes represent data structures.

2. Nodes represent models.

3. Nodes represent transformations.

4. Show request payloads.

5. Show validation.

6. Show model relationships.

7. Show DB writes.

8. Show DB reads.

9. Show response serialization.

10. Keep flow understandable.

11. Use 8–15 nodes.

==================================================
NODE TYPES
==================================================

input
model
transform
storage
output

==================================================
RETURN ONLY VALID JSON
==================================================

{
  "flow_type": "data_flow",

  "title": "Data Flow",

  "description": "Movement and transformation of data",

  "nodes": [
    {
      "id": "resume_pdf",

      "type": "input",

      "label": "Resume PDF",

      "description": "User uploaded resume",

      "data_type": "document",

      "position": {
        "x": 100,
        "y": 200
      }
    }
  ],

  "edges": [
    {
      "id": "e1",

      "source": "resume_pdf",

      "target": "parsed_resume",

      "label": "Parse",

      "description": "Extract text from PDF"
    }
  ]
}

==================================================
ARCHITECTURE DISCOVERY
==================================================

The following architecture summary was generated
from a dedicated architecture analysis phase.

Use it as your PRIMARY source of truth.

{architecture_context}

==================================================

==================================================
CODEBASE STRUCTURE
==================================================

{structure}

==================================================
CODEBASE FILES
==================================================

{content}
"""


PROMPT_MAP = {
    "system_flow": SYSTEM_FLOW_PROMPT,
    "api_flow":    API_FLOW_PROMPT,
    "data_flow":   DATA_FLOW_PROMPT,
}