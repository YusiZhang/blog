from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.posts import router as posts_router
from backend.app.db.database import engine
from backend.app.models import post

# Create the database tables
post.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API", description="API for a personal blog")

# Configure CORS
origins = [
    "http://localhost:3000",  # React development server
    "http://localhost:8000",  # FastAPI server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(posts_router, prefix="/api/posts", tags=["posts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}