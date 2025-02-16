from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, config, jobs, posts, trends

app = FastAPI(title="LinkedIn Discord Bot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(trends.router, prefix="/api/trends", tags=["trends"]) 