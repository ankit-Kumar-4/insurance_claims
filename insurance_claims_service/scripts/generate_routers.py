"""
Script to generate router files for all entities
"""

ROUTER_TEMPLATE = """\"\"\"
{entity_title} management endpoints
\"\"\"

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user, require_agent
from app.crud import {entity_name} as {entity_name}_crud
from app.schemas.{entity_name} import (
    {entity_class}Create,
    {entity_class}Update,
    {entity_class}Response,
)
from app.schemas.base import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/{entity_plural}", tags=["{entity_plural}"])


@router.get("/", response_model=PaginatedResponse[{entity_class}Response])
async def list_{function_name}(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    \"\"\"
    Get list of {entity_plural} with pagination
    \"\"\"
    items = await {entity_name}_crud.get_multi(db, skip=skip, limit=limit)
    total = await {entity_name}_crud.count(db)
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{{item_id}}", response_model={entity_class}Response)
async def get_{entity_name}(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    \"\"\"
    Get specific {entity_name} by ID
    \"\"\"
    item = await {entity_name}_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{entity_class} not found"
        )
    return item


@router.post("/", response_model={entity_class}Response, status_code=status.HTTP_201_CREATED)
async def create_{entity_name}(
    item_in: {entity_class}Create,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    \"\"\"
    Create new {entity_name}
    \"\"\"
    item = await {entity_name}_crud.create(db, obj_in=item_in)
    return item


@router.put("/{{item_id}}", response_model={entity_class}Response)
async def update_{entity_name}(
    item_id: int,
    item_update: {entity_class}Update,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    \"\"\"
    Update existing {entity_name}
    \"\"\"
    item = await {entity_name}_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{entity_class} not found"
        )
    
    updated_item = await {entity_name}_crud.update(db, db_obj=item, obj_in=item_update)
    return updated_item


@router.delete("/{{item_id}}", response_model=SuccessResponse)
async def delete_{entity_name}(
    item_id: int,
    current_user: User = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    \"\"\"
    Soft delete {entity_name}
    \"\"\"
    item = await {entity_name}_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{entity_class} not found"
        )
    
    await {entity_name}_crud.remove(db, id=item_id)
    return SuccessResponse(message="{entity_class} deleted successfully")
"""

# Entity definitions (name, plural, class name, title)
ENTITIES = [
    ("claim", "claims", "Claim", "Claim"),
    ("customer", "customers", "Customer", "Customer"),
    ("agent", "agents", "Agent", "Agent"),
    ("insurer", "insurers", "Insurer", "Insurer"),
    ("premium", "premiums", "Premium", "Premium"),
    ("coverage", "coverages", "Coverage", "Coverage"),
    ("beneficiary", "beneficiaries", "Beneficiary", "Beneficiary"),
    ("underwriter", "underwriters", "Underwriter", "Underwriter"),
    ("risk_assessment", "risk-assessments", "RiskAssessment", "Risk Assessment"),
    ("payment", "payments", "Payment", "Payment"),
    ("document", "documents", "Document", "Document"),
    ("incident", "incidents", "Incident", "Incident"),
    ("vehicle", "vehicles", "Vehicle", "Vehicle"),
    ("property", "properties", "Property", "Property"),
    ("medical_record", "medical-records", "MedicalRecord", "Medical Record"),
    ("quote", "quotes", "Quote", "Quote"),
    ("policy_renewal", "policy-renewals", "PolicyRenewal", "Policy Renewal"),
    ("commission", "commissions", "Commission", "Commission"),
    ("endorsement", "endorsements", "Endorsement", "Endorsement"),
]


def generate_router(entity_name, entity_plural, entity_class, entity_title):
    """Generate router content for an entity"""
    # Convert hyphens to underscores for function names
    function_name = entity_plural.replace('-', '_')
    return ROUTER_TEMPLATE.format(
        entity_name=entity_name,
        entity_plural=entity_plural,
        entity_class=entity_class,
        entity_title=entity_title,
        function_name=function_name
    )


def main():
    """Generate all router files"""
    import os
    
    router_dir = os.path.join(os.path.dirname(__file__), '..', 'app', 'routers')
    
    for entity_name, entity_plural, entity_class, entity_title in ENTITIES:
        file_path = os.path.join(router_dir, f"{entity_name}.py")
        content = generate_router(entity_name, entity_plural, entity_class, entity_title)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Generated router: {file_path}")
    
    print(f"\n🎉 Successfully generated {len(ENTITIES)} routers!")


if __name__ == "__main__":
    main()
