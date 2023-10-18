from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from const import OrderStatusEnum


class BaseModel(Model):
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)
    # modified_by = fields.CharField(max_length=255, default='') # get from request user

    class Meta:
        abstract = True


class Category(BaseModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    description = fields.TextField(default='')


class Product(BaseModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    description = fields.TextField(default='')
    stock_quantity = fields.IntField(default=0)
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
                                          'Category', related_name='products')


class Profile(BaseModel):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, index=True)
    email = fields.CharField(max_length=255)
    password_hash = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=255, index=True)
    last_name = fields.CharField(max_length=255, index=True)
    address = fields.TextField(default='')
    phone = fields.CharField(max_length=20)


class Order(BaseModel):
    id = fields.IntField(pk=True)
    profile: fields.ForeignKeyRelation[Profile] = fields.ForeignKeyField(
                                'models.Profile', related_name='orders')
    status = fields.IntEnumField(enum_type=OrderStatusEnum, index=True)
    total_price = fields.IntField()


class OrderItem(BaseModel):
    id = fields.IntField(pk=True)
    quantity = fields.IntField(default=1)
    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
                              'models.Product', related_name='order_items')
    order: fields.ForeignKeyRelation[Order] = fields.ForeignKeyField(
                                'models.Order', related_name='order_items')


class Comment(BaseModel):
    id = fields.IntField(pk=True)
    content = fields.TextField(default='')
    likes = fields.IntField(default=0)
    dislikes = fields.IntField(default=0)
    parent: fields.ForeignKeyRelation['Comment'] = fields.ForeignKeyField(
                                'models.Comment', related_name='children',
                                null=True, default=None)
    profile: fields.ForeignKeyRelation[Profile] = fields.ForeignKeyField(
                                'models.Profile', related_name='comments')
    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
                              'models.Product', related_name='comments')
    order: fields.ForeignKeyRelation[Order] = fields.ForeignKeyField(
                                'models.Order', related_name='comments',
                                null=True, default=None)


ProductPydantic = pydantic_model_creator(Product, name='Product')
ProductInPydantic = pydantic_model_creator(Product, name='ProductIn',
                                           exclude=('id', 'created', 'modified'))
