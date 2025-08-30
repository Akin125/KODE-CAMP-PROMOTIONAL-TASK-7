from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import json
import os
from datetime import datetime
from ..models import CartItem, CartItemCreate, CartItemRead, Product, User, Order
from ..database import get_session
from ..auth import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/add", response_model=CartItemRead)
def add_to_cart(
    cart_item: CartItemCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Add item to cart"""
    # Check if product exists and has enough stock
    product = session.get(Product, cart_item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # Check if item already in cart
    existing_item = session.exec(
        select(CartItem).where(
            CartItem.user_id == current_user.id,
            CartItem.product_id == cart_item.product_id
        )
    ).first()

    if existing_item:
        # Update quantity
        new_quantity = existing_item.quantity + cart_item.quantity
        if product.stock < new_quantity:
            raise HTTPException(status_code=400, detail="Not enough stock for requested quantity")
        existing_item.quantity = new_quantity
        session.add(existing_item)
        session.commit()
        session.refresh(existing_item)
        return existing_item
    else:
        # Create new cart item
        db_cart_item = CartItem(
            product_id=cart_item.product_id,
            user_id=current_user.id,
            quantity=cart_item.quantity
        )
        session.add(db_cart_item)
        session.commit()
        session.refresh(db_cart_item)
        return db_cart_item


@router.get("/", response_model=List[CartItemRead])
def get_cart_items(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all items in user's cart"""
    cart_items = session.exec(
        select(CartItem).where(CartItem.user_id == current_user.id)
    ).all()
    return cart_items


@router.delete("/remove/{item_id}")
def remove_from_cart(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Remove item from cart"""
    cart_item = session.exec(
        select(CartItem).where(
            CartItem.id == item_id,
            CartItem.user_id == current_user.id
        )
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    session.delete(cart_item)
    session.commit()
    return {"message": "Item removed from cart"}


@router.post("/checkout")
def checkout_cart(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Checkout cart and create order"""
    # Get all cart items for user
    cart_items = session.exec(
        select(CartItem).where(CartItem.user_id == current_user.id)
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0.0
    order_items = []

    # Calculate total and check stock
    for cart_item in cart_items:
        product = session.get(Product, cart_item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {cart_item.product_id} not found")

        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}. Available: {product.stock}, Requested: {cart_item.quantity}"
            )

        item_total = product.price * cart_item.quantity
        total_amount += item_total

        order_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": cart_item.quantity,
            "price": product.price,
            "total": item_total
        })

    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status="completed"
    )
    session.add(order)

    # Update product stock and clear cart
    for cart_item in cart_items:
        product = session.get(Product, cart_item.product_id)
        product.stock -= cart_item.quantity
        session.add(product)
        session.delete(cart_item)

    session.commit()
    session.refresh(order)

    # Save order to JSON backup
    save_order_to_json({
        "order_id": order.id,
        "user_id": current_user.id,
        "username": current_user.username,
        "total_amount": total_amount,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "items": order_items
    })

    return {
        "message": "Order placed successfully",
        "order_id": order.id,
        "total_amount": total_amount,
        "items": order_items
    }


def save_order_to_json(order_data: dict):
    """Save order to orders.json for backup"""
    orders_file = "orders.json"

    # Load existing orders
    if os.path.exists(orders_file):
        with open(orders_file, 'r') as f:
            orders = json.load(f)
    else:
        orders = []

    # Add new order
    orders.append(order_data)

    # Save back to file
    with open(orders_file, 'w') as f:
        json.dump(orders, f, indent=2)
