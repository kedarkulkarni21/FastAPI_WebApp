from fastapi import FastAPI, HTTPException, Depends, status, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Web Application",
    description="A boilerplate for FastAPI applications",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "items",
            "description": "Operations with items",
        },
        {
            "name": "forms",
            "description": "Form submission operations",
        },
        {
            "name": "health",
            "description": "Health check endpoints",
        },
    ],
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ensure the static/scripts directory exists
os.makedirs("static/scripts", exist_ok=True)

# Models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Example Item",
                "description": "This is an example item",
                "price": 42.99
            }
        }

class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "subject": "Product Inquiry",
                "message": "I would like more information about your product."
            }
        }

# Mock database
items_db = []
item_id_counter = 4
contact_submissions = []

# Function to initialize the database with sample items
def initialize_db():
    sample_items = [
        Item(id=1, name="Laptop", description="High-performance gaming laptop", price=1299.99),
        Item(id=2, name="Smartphone", description="Latest model with advanced camera", price=899.99),
        Item(id=3, name="Coffee Maker", description="Programmable with multiple brewing options", price=149.95)
    ]
    
    for item in sample_items:
        items_db.append(item)
    
    print(f"Database initialized with {len(items_db)} items")

# Initialize the database with sample items
initialize_db()

# Routes
@app.get('/items', response_model=List[Item], tags=["items"])
async def get_all_items():
    return items_db

@app.get('/items/{item_id}', response_model=Item, tags=["items"])
async def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"])
async def create_item(item: Item):
    global item_id_counter
    
    new_item = {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "id": item_id_counter
    }
    
    item_id_counter += 1
    
    item_obj = Item(**new_item)
    items_db.append(item_obj)
    return item_obj

# Form submission routes
@app.get("/contact", response_class=HTMLResponse, tags=["forms"])
async def get_contact_form(request: Request):
    """
    Renders the contact form page.
    """
    return templates.TemplateResponse(
        "contact_form.html", 
        {"request": request, "title": "Contact Us"}
    )

@app.post("/submit-form", response_model=ContactForm, tags=["forms"])
async def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    """
    Handles the submission of the contact form.
    """
    form_data = ContactForm(
        name=name,
        email=email,
        subject=subject,
        message=message
    )
    
    contact_submissions.append(form_data)
    print(f"Form submitted by {name} ({email}): {subject}")
    
    return form_data

@app.get("/submissions", response_model=List[ContactForm], tags=["forms"])
async def get_submissions():
    """
    Returns all form submissions (for demonstration purposes).
    """
    return contact_submissions

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)