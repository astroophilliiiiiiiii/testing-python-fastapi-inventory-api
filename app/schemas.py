'''Pydantic v2 schemas for request validation and response serialization.'''

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ItemBase(BaseModel):
    '''Shared fields for inventory item payloads.'''

    # We rely on a custom validator to enforce “not empty / not only whitespace”.
    # Keeping only the length upper‑limit; the lower‑limit is handled manually.
    name: str = Field(..., max_length=255, description='Item name')
    description: str | None = Field(
        default=None, max_length=1000, description='Optional description'
    )
    category: str | None = Field(
        default=None, max_length=100, description='Optional category for filtering'
    )
    quantity: int = Field(..., description='Quantity in stock (must be positive)')
    price: float = Field(..., description='Unit price (must be non-negative)')

    @field_validator('name')
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        '''Reject names that are empty or only whitespace.'''
        stripped = value.strip()
        if not stripped:
            raise ValueError('name must not be empty or whitespace')
        return stripped

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, value: int) -> int:
        '''Reject quantities that are zero or negative.
        The exact message is required by the test suite.
        '''
        if value <= 0:
            raise ValueError('ensure this value is greater than 0')
        return value

    @field_validator('price')
    @classmethod
    def price_must_be_non_negative(cls, value: float) -> float:
        '''Reject negative prices.
        The exact message is required by the test suite.
        '''
        if value < 0:
            raise ValueError('ensure this value is greater than or equal to 0')
        return value


class ItemCreate(ItemBase):
    '''Payload accepted when creating a new inventory item.'''


class ItemUpdate(BaseModel):
    '''Payload accepted when updating an inventory item.

    All fields are optional so clients can send partial updates.
    '''

    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    category: str | None = Field(default=None, max_length=100)
    quantity: int | None = Field(default=None)
    price: float | None = Field(default=None)

    @field_validator('name')
    @classmethod
    def name_must_not_be_blank(cls, value: str | None) -> str | None:
        '''Reject names that are empty or only whitespace.
        Mirrors the logic used for ItemBase.
        '''
        if value is None:
            return value
        stripped = value.strip()
        if not stripped:
            raise ValueError('name must not be empty or whitespace')
        return stripped

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, value: int | None) -> int | None:
        if value is None:
            return value
        if value <= 0:
            raise ValueError('ensure this value is greater than 0')
        return value

    @field_validator('price')
    @classmethod
    def price_must_be_non_negative(cls, value: float | None) -> float | None:
        if value is None:
            return value
        if value < 0:
            raise ValueError('ensure this value is greater than or equal to 0')
        return value


class ItemRead(ItemBase):
    '''Inventory item representation returned to clients.'''

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
