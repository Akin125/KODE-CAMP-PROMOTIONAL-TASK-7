from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class ProductBase(SQLModel):
    name: str
    price: float
    stock: int
    description: Optional[str] = None


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    cart_items: List["CartItem"] = Relationship(back_populates="product")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    description: Optional[str] = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime


class UserBase(SQLModel):
    username: str
    email: str
    role: UserRole = UserRole.USER


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    cart_items: List["CartItem"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime


class CartItemBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    user_id: int = Field(foreign_key="user.id")
    quantity: int = Field(default=1, ge=1)


class CartItem(CartItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    added_at: datetime = Field(default_factory=datetime.utcnow)
    product: Optional[Product] = Relationship(back_populates="cart_items")
    user: Optional[User] = Relationship(back_populates="cart_items")


class CartItemCreate(SQLModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemRead(CartItemBase):
    id: int
    added_at: datetime
    product: ProductRead


class OrderBase(SQLModel):
    user_id: int
    total_amount: float
    status: str = "pending"


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    created_at: datetime


# Token models
class Token(SQLModel):
    access_token: str
    token_type: str


class LoginRequest(SQLModel):
    username: str
    password: str


# Update forward references
ProductRead.model_rebuild()
CartItemRead.model_rebuild()
