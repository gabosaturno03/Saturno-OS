# Create the complete backend structure and API documentation
import os
import json

# Backend API structure and endpoints
backend_api = {
    "api_version": "1.0.0",
    "base_url": "http://localhost:3001/api",
    "endpoints": {
        "authentication": {
            "POST /auth/login": {
                "description": "User login with email/password",
                "body": {"email": "string", "password": "string"},
                "response": {"token": "string", "user": "object"}
            },
            "POST /auth/register": {
                "description": "User registration",
                "body": {"email": "string", "password": "string", "name": "string"},
                "response": {"token": "string", "user": "object"}
            },
            "POST /auth/refresh": {
                "description": "Refresh JWT token",
                "body": {"refreshToken": "string"},
                "response": {"token": "string"}
            }
        },
        "documents": {
            "GET /documents": {
                "description": "Get all user documents",
                "query": {"folder": "string", "tags": "array", "search": "string"},
                "response": {"documents": "array", "total": "number"}
            },
            "POST /documents": {
                "description": "Create new document",
                "body": {"title": "string", "content": "string", "type": "string", "tags": "array"},
                "response": {"document": "object"}
            },
            "PUT /documents/:id": {
                "description": "Update document",
                "body": {"title": "string", "content": "string", "tags": "array"},
                "response": {"document": "object"}
            },
            "DELETE /documents/:id": {
                "description": "Delete document",
                "response": {"success": "boolean"}
            }
        },
        "ai": {
            "POST /ai/chat": {
                "description": "Send message to AI assistant",
                "body": {"message": "string", "context": "array", "model": "string"},
                "response": {"response": "string", "usage": "object"}
            },
            "POST /ai/generate": {
                "description": "Generate content using AI",
                "body": {"prompt": "string", "type": "string", "context": "array"},
                "response": {"content": "string", "usage": "object"}
            },
            "GET /ai/models": {
                "description": "Get available AI models",
                "response": {"models": "array"}
            }
        },
        "projects": {
            "GET /projects": {
                "description": "Get all user projects",
                "response": {"projects": "array"}
            },
            "POST /projects": {
                "description": "Create new project",
                "body": {"name": "string", "description": "string", "type": "string"},
                "response": {"project": "object"}
            },
            "PUT /projects/:id": {
                "description": "Update project",
                "body": {"name": "string", "description": "string", "tasks": "array"},
                "response": {"project": "object"}
            }
        },
        "assets": {
            "GET /assets": {
                "description": "Get all user assets",
                "query": {"type": "string", "search": "string"},
                "response": {"assets": "array"}
            },
            "POST /assets/upload": {
                "description": "Upload new asset",
                "body": "multipart/form-data",
                "response": {"asset": "object", "url": "string"}
            },
            "DELETE /assets/:id": {
                "description": "Delete asset",
                "response": {"success": "boolean"}
            }
        },
        "collaboration": {
            "GET /collaboration/rooms": {
                "description": "Get user's collaboration rooms",
                "response": {"rooms": "array"}
            },
            "POST /collaboration/rooms": {
                "description": "Create collaboration room",
                "body": {"name": "string", "documentId": "string", "members": "array"},
                "response": {"room": "object"}
            },
            "WebSocket /collaboration/rooms/:id": {
                "description": "Real-time collaboration socket",
                "events": ["document-change", "cursor-move", "user-join", "user-leave"]
            }
        }
    }
}

# Backend package.json
backend_package = {
    "name": "kortex-writing-hub-backend",
    "version": "1.0.0",
    "description": "Backend API for Kortex Writing Hub",
    "main": "src/server.js",
    "scripts": {
        "start": "node src/server.js",
        "dev": "nodemon src/server.js",
        "test": "jest",
        "test:watch": "jest --watch",
        "lint": "eslint src/",
        "migrate": "knex migrate:latest",
        "seed": "knex seed:run"
    },
    "dependencies": {
        "express": "^4.18.2",
        "cors": "^2.8.5",
        "helmet": "^7.1.0",
        "morgan": "^1.10.0",
        "bcryptjs": "^2.4.3",
        "jsonwebtoken": "^9.0.2",
        "multer": "^1.4.5-lts.1",
        "socket.io": "^4.7.4",
        "knex": "^3.0.1",
        "sqlite3": "^5.1.6",
        "pg": "^8.11.3",
        "openai": "^4.20.1",
        "anthropic": "^0.6.0",
        "dotenv": "^16.3.1",
        "joi": "^17.11.0",
        "rate-limiter-flexible": "^3.0.8"
    },
    "devDependencies": {
        "nodemon": "^3.0.2",
        "jest": "^29.7.0",
        "supertest": "^6.3.3",
        "eslint": "^8.55.0"
    }
}

# Server configuration
server_config = {
    "development": {
        "database": {
            "client": "sqlite3",
            "connection": "./data/dev.db",
            "useNullAsDefault": True
        },
        "ai": {
            "openai": {
                "apiKey": "process.env.OPENAI_API_KEY",
                "model": "gpt-4",
                "maxTokens": 4000
            },
            "anthropic": {
                "apiKey": "process.env.ANTHROPIC_API_KEY",
                "model": "claude-3-sonnet-20240229",
                "maxTokens": 3000
            }
        },
        "auth": {
            "jwtSecret": "process.env.JWT_SECRET",
            "jwtExpiration": "24h",
            "refreshTokenExpiration": "7d"
        },
        "server": {
            "port": 3001,
            "corsOrigin": "http://localhost:5173"
        }
    },
    "production": {
        "database": {
            "client": "postgresql",
            "connection": "process.env.DATABASE_URL",
            "pool": {"min": 2, "max": 10}
        },
        "ai": {
            "openai": {
                "apiKey": "process.env.OPENAI_API_KEY",
                "model": "gpt-4",
                "maxTokens": 4000
            },
            "anthropic": {
                "apiKey": "process.env.ANTHROPIC_API_KEY",
                "model": "claude-3-sonnet-20240229",
                "maxTokens": 3000
            }
        },
        "auth": {
            "jwtSecret": "process.env.JWT_SECRET",
            "jwtExpiration": "24h",
            "refreshTokenExpiration": "7d"
        },
        "server": {
            "port": "process.env.PORT || 3001",
            "corsOrigin": "process.env.FRONTEND_URL"
        }
    }
}

# Database schema
database_schema = {
    "users": {
        "id": "primary key",
        "email": "string unique",
        "password": "string hashed",
        "name": "string",
        "avatar": "string optional",
        "preferences": "json",
        "created_at": "timestamp",
        "updated_at": "timestamp"
    },
    "documents": {
        "id": "primary key",
        "user_id": "foreign key -> users.id",
        "title": "string",
        "content": "text",
        "type": "string (markdown, text, etc)",
        "folder_path": "string",
        "tags": "json array",
        "metadata": "json",
        "created_at": "timestamp",
        "updated_at": "timestamp"
    },
    "projects": {
        "id": "primary key",
        "user_id": "foreign key -> users.id",
        "name": "string",
        "description": "text",
        "type": "string",
        "status": "string",
        "data": "json (tasks, timeline, etc)",
        "created_at": "timestamp",
        "updated_at": "timestamp"
    },
    "assets": {
        "id": "primary key",
        "user_id": "foreign key -> users.id",
        "filename": "string",
        "original_name": "string",
        "mime_type": "string",
        "size": "integer",
        "url": "string",
        "folder_path": "string",
        "metadata": "json",
        "created_at": "timestamp"
    },
    "ai_conversations": {
        "id": "primary key",
        "user_id": "foreign key -> users.id",
        "document_id": "foreign key -> documents.id optional",
        "messages": "json array",
        "model_used": "string",
        "tokens_used": "integer",
        "created_at": "timestamp"
    },
    "collaboration_rooms": {
        "id": "primary key",
        "document_id": "foreign key -> documents.id",
        "owner_id": "foreign key -> users.id",
        "name": "string",
        "members": "json array",
        "settings": "json",
        "created_at": "timestamp"
    }
}

# Save all backend configuration files
with open("backend-api.json", "w") as f:
    json.dump(backend_api, f, indent=2)

with open("backend-package.json", "w") as f:
    json.dump(backend_package, f, indent=2)

with open("server-config.json", "w") as f:
    json.dump(server_config, f, indent=2)

with open("database-schema.json", "w") as f:
    json.dump(database_schema, f, indent=2)

print("🚀 Backend configuration files created successfully!")
print("📁 Files generated:")
print("  - backend-api.json (API documentation)")
print("  - backend-package.json (Node.js dependencies)")
print("  - server-config.json (Environment configuration)")
print("  - database-schema.json (Database structure)")