"""Base CRUD operations for all entities"""

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy import select, update, delete, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from datetime import datetime

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class CRUDBase(Generic[ModelType]):
    """
    Base class for CRUD operations with async support
    
    Provides common database operations:
    - Create, Read, Update, Delete (CRUD)
    - Soft delete support
    - Pagination
    - Filtering and search
    - Bulk operations
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD with model class
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    # ==================== CREATE ====================
    
    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: Dict[str, Any]
    ) -> ModelType:
        """
        Create a new record
        
        Args:
            db: Database session
            obj_in: Dictionary of attributes
            
        Returns:
            Created model instance
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def create_many(
        self,
        db: AsyncSession,
        *,
        objs_in: List[Dict[str, Any]]
    ) -> List[ModelType]:
        """
        Create multiple records in bulk
        
        Args:
            db: Database session
            objs_in: List of attribute dictionaries
            
        Returns:
            List of created model instances
        """
        db_objs = [self.model(**obj) for obj in objs_in]
        db.add_all(db_objs)
        await db.commit()
        for obj in db_objs:
            await db.refresh(obj)
        return db_objs
    
    # ==================== READ ====================
    
    async def get(
        self,
        db: AsyncSession,
        id: int,
        *,
        include_deleted: bool = False
    ) -> Optional[ModelType]:
        """
        Get a record by ID
        
        Args:
            db: Database session
            id: Record ID
            include_deleted: Include soft-deleted records
            
        Returns:
            Model instance or None
        """
        query = select(self.model).where(self.model.id == id)
        
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> List[ModelType]:
        """
        Get multiple records with pagination
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Include soft-deleted records
            order_by: Field name to order by (defaults to 'id')
            order_desc: Order descending if True
            
        Returns:
            List of model instances
        """
        query = select(self.model)
        
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            order_field = getattr(self.model, order_by)
            query = query.order_by(order_field.desc() if order_desc else order_field)
        else:
            query = query.order_by(self.model.id)
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_field(
        self,
        db: AsyncSession,
        *,
        field_name: str,
        field_value: Any,
        include_deleted: bool = False
    ) -> Optional[ModelType]:
        """
        Get a record by any field value
        
        Args:
            db: Database session
            field_name: Name of the field to filter by
            field_value: Value to match
            include_deleted: Include soft-deleted records
            
        Returns:
            Model instance or None
        """
        if not hasattr(self.model, field_name):
            raise ValueError(f"Model {self.model.__name__} has no field '{field_name}'")
        
        query = select(self.model).where(
            getattr(self.model, field_name) == field_value
        )
        
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_multi_by_field(
        self,
        db: AsyncSession,
        *,
        field_name: str,
        field_value: Any,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False
    ) -> List[ModelType]:
        """
        Get multiple records by field value
        
        Args:
            db: Database session
            field_name: Name of the field to filter by
            field_value: Value to match
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Include soft-deleted records
            
        Returns:
            List of model instances
        """
        if not hasattr(self.model, field_name):
            raise ValueError(f"Model {self.model.__name__} has no field '{field_name}'")
        
        query = select(self.model).where(
            getattr(self.model, field_name) == field_value
        )
        
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def count(
        self,
        db: AsyncSession,
        *,
        filter_dict: Optional[Dict[str, Any]] = None,
        include_deleted: bool = False
    ) -> int:
        """
        Count total records
        
        Args:
            db: Database session
            filter_dict: Optional filters
            include_deleted: Include soft-deleted records
            
        Returns:
            Total count
        """
        query = select(func.count()).select_from(self.model)
        
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        
        if filter_dict:
            for field_name, field_value in filter_dict.items():
                if hasattr(self.model, field_name):
                    query = query.where(getattr(self.model, field_name) == field_value)
        
        result = await db.execute(query)
        return result.scalar_one()
    
    # ==================== UPDATE ====================
    
    async def update(
        self,
        db: AsyncSession,
        *,
        id: int,
        obj_in: Dict[str, Any]
    ) -> Optional[ModelType]:
        """
        Update a record
        
        Args:
            db: Database session
            id: Record ID
            obj_in: Dictionary of attributes to update
            
        Returns:
            Updated model instance or None
        """
        db_obj = await self.get(db, id=id)
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        # Update last_modified_date if it exists
        if hasattr(db_obj, 'last_modified_date'):
            db_obj.last_modified_date = datetime.utcnow()
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update_multi(
        self,
        db: AsyncSession,
        *,
        filter_dict: Dict[str, Any],
        update_dict: Dict[str, Any]
    ) -> int:
        """
        Update multiple records matching filters
        
        Args:
            db: Database session
            filter_dict: Fields to filter by
            update_dict: Fields to update
            
        Returns:
            Number of updated records
        """
        stmt = update(self.model)
        
        for field_name, field_value in filter_dict.items():
            if hasattr(self.model, field_name):
                stmt = stmt.where(getattr(self.model, field_name) == field_value)
        
        stmt = stmt.where(self.model.deleted_at.is_(None))
        stmt = stmt.values(**update_dict)
        stmt = stmt.execution_options(synchronize_session="fetch")
        
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount
    
    # ==================== DELETE ====================
    
    async def delete(
        self,
        db: AsyncSession,
        *,
        id: int,
        soft: bool = True
    ) -> bool:
        """
        Delete a record (soft or hard delete)
        
        Args:
            db: Database session
            id: Record ID
            soft: Use soft delete if True, hard delete if False
            
        Returns:
            True if deleted, False otherwise
        """
        db_obj = await self.get(db, id=id, include_deleted=not soft)
        if not db_obj:
            return False
        
        if soft:
            # Soft delete
            db_obj.deleted_at = datetime.utcnow()
            await db.commit()
        else:
            # Hard delete
            await db.delete(db_obj)
            await db.commit()
        
        return True
    
    async def restore(
        self,
        db: AsyncSession,
        *,
        id: int
    ) -> Optional[ModelType]:
        """
        Restore a soft-deleted record
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            Restored model instance or None
        """
        db_obj = await self.get(db, id=id, include_deleted=True)
        if not db_obj or db_obj.deleted_at is None:
            return None
        
        db_obj.deleted_at = None
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete_multi(
        self,
        db: AsyncSession,
        *,
        filter_dict: Dict[str, Any],
        soft: bool = True
    ) -> int:
        """
        Delete multiple records matching filters
        
        Args:
            db: Database session
            filter_dict: Fields to filter by
            soft: Use soft delete if True
            
        Returns:
            Number of deleted records
        """
        if soft:
            return await self.update_multi(
                db,
                filter_dict=filter_dict,
                update_dict={"deleted_at": datetime.utcnow()}
            )
        else:
            stmt = delete(self.model)
            
            for field_name, field_value in filter_dict.items():
                if hasattr(self.model, field_name):
                    stmt = stmt.where(getattr(self.model, field_name) == field_value)
            
            result = await db.execute(stmt)
            await db.commit()
            return result.rowcount
    
    # ==================== SEARCH & FILTER ====================
    
    async def search(
        self,
        db: AsyncSession,
        *,
        search_term: str,
        search_fields: List[str],
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False
    ) -> List[ModelType]:
        """
        Search records by term across multiple fields
        
        Args:
            db: Database session
            search_term: Term to search for
            search_fields: List of field names to search in
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Include soft-deleted records
            
        Returns:
            List of matching model instances
        """
        query = select(self.model)
        
        # Build OR conditions for all search fields
        conditions = []
        for field_name in search_fields:
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                conditions.append(field.ilike(f"%{search_term}%"))
        
        if conditions:
            query = query.where(or_(*conditions))
        
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def filter(
        self,
        db: AsyncSession,
        *,
        filters: Dict[str, Any],
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> List[ModelType]:
        """
        Filter records by multiple criteria
        
        Args:
            db: Database session
            filters: Dictionary of field filters
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Include soft-deleted records
            order_by: Field name to order by
            order_desc: Order descending if True
            
        Returns:
            List of matching model instances
        """
        query = select(self.model)
        
        # Apply filters
        for field_name, field_value in filters.items():
            if hasattr(self.model, field_name):
                if isinstance(field_value, (list, tuple)):
                    # IN clause for multiple values
                    query = query.where(getattr(self.model, field_name).in_(field_value))
                else:
                    query = query.where(getattr(self.model, field_name) == field_value)
        
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            order_field = getattr(self.model, order_by)
            query = query.order_by(order_field.desc() if order_desc else order_field)
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    # ==================== EXISTS ====================
    
    async def exists(
        self,
        db: AsyncSession,
        *,
        id: int,
        include_deleted: bool = False
    ) -> bool:
        """
        Check if a record exists
        
        Args:
            db: Database session
            id: Record ID
            include_deleted: Check including soft-deleted records
            
        Returns:
            True if exists, False otherwise
        """
        query = select(func.count()).select_from(self.model).where(self.model.id == id)
        
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        
        result = await db.execute(query)
        count = result.scalar_one()
        return count > 0
    
    async def exists_by_field(
        self,
        db: AsyncSession,
        *,
        field_name: str,
        field_value: Any,
        exclude_id: Optional[int] = None,
        include_deleted: bool = False
    ) -> bool:
        """
        Check if a record exists with given field value
        
        Args:
            db: Database session
            field_name: Name of the field to check
            field_value: Value to match
            exclude_id: Exclude this ID from check (for updates)
            include_deleted: Check including soft-deleted records
            
        Returns:
            True if exists, False otherwise
        """
        if not hasattr(self.model, field_name):
            raise ValueError(f"Model {self.model.__name__} has no field '{field_name}'")
        
        query = select(func.count()).select_from(self.model).where(
            getattr(self.model, field_name) == field_value
        )
        
        if exclude_id:
            query = query.where(self.model.id != exclude_id)
        
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        
        result = await db.execute(query)
        count = result.scalar_one()
        return count > 0
    
    # ==================== UTILITY METHODS ====================
    
    def _apply_filters(self, query: Select, filters: Dict[str, Any]) -> Select:
        """Apply filter dictionary to query"""
        for field_name, field_value in filters.items():
            if hasattr(self.model, field_name):
                query = query.where(getattr(self.model, field_name) == field_value)
        return query
    
    async def get_all_deleted(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Get all soft-deleted records
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of soft-deleted model instances
        """
        query = select(self.model).where(
            self.model.deleted_at.is_not(None)
        ).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
