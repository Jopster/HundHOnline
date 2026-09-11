from collections.abc import Generator
from decimal import Decimal
import os
from pathlib import Path
from secrets import compare_digest

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, Integer, Numeric, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from starlette.middleware.sessions import SessionMiddleware

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://hhonline_user:hh2026_Mysql@localhost:3306/hhonline?charset=utf8mb4",
)
AUTH_USERNAME = os.getenv("AUTH_USERNAME", "HHOnline")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "HHOnline")
SESSION_SECRET = os.getenv("SESSION_SECRET", "change-this-before-public-deployment")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_name: Mapped[str] = mapped_column(String(100), index=True)
    article_number: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), index=True)
    supplier: Mapped[str] = mapped_column(String(255), default="")
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), default=Decimal("1.000"))
    sales_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    vat_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("19.00"))
    unit: Mapped[str] = mapped_column(String(24), default="Stueck")
    archived: Mapped[bool] = mapped_column(Boolean, default=False)


class ArticlePayload(BaseModel):
    group_name: str = Field(min_length=1, max_length=100)
    article_number: str = Field(min_length=1, max_length=64)
    description: str = Field(min_length=1, max_length=255)
    supplier: str = Field(default="", max_length=255)
    quantity: Decimal = Field(default=Decimal("1.000"), ge=0)
    sales_price: Decimal = Field(default=Decimal("0.00"), ge=0)
    vat_rate: Decimal = Field(default=Decimal("19.00"), ge=0, le=100)
    unit: str = Field(default="Stueck", max_length=24)
    archived: bool = False


class ArticleResponse(ArticlePayload):
    model_config = ConfigDict(from_attributes=True)

    id: int


class LoginPayload(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=255)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def require_authenticated_user(request: Request) -> str:
    username = request.session.get("username")
    if username != AUTH_USERNAME:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Anmeldung erforderlich.")
    return username


def seed_articles(session: Session) -> None:
    if session.scalar(select(Article.id).limit(1)):
        return
    session.add_all([
        Article(group_name="Abfallsammler", article_number="AA 130", description="Abfallsammler fuer Schränke mit Frontauszug", supplier="Frank-Michael Stoltenberg", quantity=Decimal("1"), sales_price=Decimal("528.00")),
        Article(group_name="Abfallsammler", article_number="AA 131", description="Abfallsammler Unterbau", supplier="Susanne Schneider", quantity=Decimal("1"), sales_price=Decimal("349.00")),
        Article(group_name="Auszüge", article_number="AZ_71", description="Auszug System 71", supplier="Digital Dynamic", quantity=Decimal("1"), sales_price=Decimal("274.75")),
        Article(group_name="Auszüge", article_number="U_TIG_71", description="Unterflurauszug TIG 71", supplier="Digital Dynamic", quantity=Decimal("1"), sales_price=Decimal("74.11")),
        Article(group_name="Beschläge", article_number="TUER", description="Tuer", supplier="Beschläge Mueller", quantity=Decimal("1"), sales_price=Decimal("0")),
        Article(group_name="Arbeitsplatten", article_number="AP_DESIGN", description="Artikel Designer Gruppe", supplier="Arbeitsplatten GmbH", quantity=Decimal("1"), sales_price=Decimal("380.13")),
    ])
    session.commit()


app = FastAPI(
    title="HHOnline API",
    version="0.1.0",
    middleware=[Middleware(SessionMiddleware, secret_key=SESSION_SECRET, same_site="lax", https_only=False)],
)


@app.on_event("startup")
def initialise_database() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        seed_articles(session)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/auth/login")
def login(payload: LoginPayload, request: Request) -> dict[str, str]:
    if not (
        compare_digest(payload.username, AUTH_USERNAME)
        and compare_digest(payload.password, AUTH_PASSWORD)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Benutzername oder Passwort ist ungültig.")
    request.session.clear()
    request.session["username"] = AUTH_USERNAME
    return {"username": AUTH_USERNAME}


@app.get("/api/auth/session")
def get_authenticated_user(username: str = Depends(require_authenticated_user)) -> dict[str, str]:
    return {"username": username}


@app.post("/api/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request) -> None:
    request.session.clear()


@app.get("/api/articles", response_model=list[ArticleResponse])
def list_articles(
    search: str | None = None,
    group_name: str | None = None,
    session: Session = Depends(get_session),
    _: str = Depends(require_authenticated_user),
) -> list[Article]:
    statement = select(Article).order_by(Article.article_number)
    if group_name and group_name != "Alle":
        statement = statement.where(Article.group_name == group_name)
    if search:
        pattern = f"%{search.strip()}%"
        statement = statement.where(
            Article.description.ilike(pattern) | Article.article_number.ilike(pattern) | Article.supplier.ilike(pattern)
        )
    return list(session.scalars(statement))


@app.post("/api/articles", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    payload: ArticlePayload,
    session: Session = Depends(get_session),
    _: str = Depends(require_authenticated_user),
) -> Article:
    if session.scalar(select(Article).where(Article.article_number == payload.article_number)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Artikelnummer existiert bereits.")
    article = Article(**payload.model_dump())
    session.add(article)
    session.commit()
    session.refresh(article)
    return article


@app.put("/api/articles/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    payload: ArticlePayload,
    session: Session = Depends(get_session),
    _: str = Depends(require_authenticated_user),
) -> Article:
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artikel wurde nicht gefunden.")
    duplicate = session.scalar(select(Article).where(Article.article_number == payload.article_number, Article.id != article_id))
    if duplicate:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Artikelnummer existiert bereits.")
    for field_name, value in payload.model_dump().items():
        setattr(article, field_name, value)
    session.commit()
    session.refresh(article)
    return article


@app.delete("/api/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(require_authenticated_user),
) -> None:
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artikel wurde nicht gefunden.")
    session.delete(article)
    session.commit()


app.mount("/", StaticFiles(directory=BASE_DIR / "frontend", html=True), name="frontend")
