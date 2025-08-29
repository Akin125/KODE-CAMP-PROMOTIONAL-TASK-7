from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..models import Product, ProductCreate, ProductUpdate, ProductRead, User
from ..database import get_session
from ..auth import get_current_user, get_admin_user

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductRead])
def get_products(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all products (public endpoint)"""
    products = session.exec(select(Product).offset(skip).limit(limit)).all()
    return products


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific product by ID (public endpoint)"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/admin/", response_model=ProductRead)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_admin_user)
):
    """Create a new product (admin only)"""
    db_product = Product(**product.dict())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.put("/admin/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_admin_user)
):
    """Update a product (admin only)"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = product_update.dict(exclude_unset=True)
    for field, value in product_data.items():
        setattr(product, field, value)

    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete("/admin/{product_id}")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_admin_user)
):
    """Delete a product (admin only)"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}
