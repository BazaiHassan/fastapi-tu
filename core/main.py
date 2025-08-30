from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.user.routes import router as user_routes
from core.expense.routes import router as expense_routes
from core.category.routes import router as category_routes
from core.budget.routes import router as budget_routes
from core.src.config import settings

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("App is started")
    yield
    print("App is shuted down")


app = FastAPI(lifespan=lifespan)

app.include_router(user_routes, prefix=settings.API_VERSION)
app.include_router(expense_routes, prefix=settings.API_VERSION)
app.include_router(category_routes, prefix=settings.API_VERSION)
app.include_router(budget_routes, prefix=settings.API_VERSION)