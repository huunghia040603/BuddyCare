from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from saleappv2.app import db
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690461425/bqjr27d0xjx4u78ghp3s.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(550), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(500),
                   default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1691062682/tkeflqgroeil781yplxt.jpg')
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)

    def __str__(self):
        return self.name


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime)
    active = Column(Boolean, default=True)


class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == '__main__':
    from saleappv2.app import app
    with app.app_context():
        # db.create_all()
        #
        # import hashlib
        # u = User(name='Admin', username='admin',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        # db.session.add(u)
        # db.session.commit()
        #
        # c1 = Category(name='Mobile')
        # c2 = Category(name='Tablet')
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.commit()

        p1 = Product(name='Nước Tẩy Trang LOreal Tươi Mát Cho Da Dầu, Hỗn Hợp 400ml Micellar Water 3-in-1', price=22000000,image='https://res.cloudinary.com/duc03aacd/image/upload/f_auto,q_auto/v1/BuddyCare/f27pjwim9q98gyztkd9r', category_id=1)
        p2 = Product(name='Kem Dưỡng Estee Lauder Daywear 50ml Multi-Protection Anti-Oxidant Creme SPF15 ', price=24000000,image='https://res.cloudinary.com/duc03aacd/image/upload/v1706873840/BuddyCare/cb9xvmhojhqckxyljgzt.png', category_id=2)
        p3 = Product(name='Kem Nền Lâu Trôi Estee Lauder Double Wear Stay-in-Place Makeup SPF 10/PA++', price=27000000,image='https://res.cloudinary.com/duc03aacd/image/upload/v1706873840/BuddyCare/hrdor1s57xaa6im5ozh5.png',category_id=1)
        p4 = Product(name='SK-II SkinPower Cream - Kem dưỡng ẩm chống lão hoá 80g', price=22000000,image='https://res.cloudinary.com/duc03aacd/image/upload/v1706873840/BuddyCare/fxk74yuiglijs80agxte.jpg', category_id=1)
        p5 = Product(name='Tinh Chất Phục Hồi Chống Lão Hóa Thế Hệ Mới Estee Lauder Advanced Nigh',image='https://res.cloudinary.com/duc03aacd/image/upload/f_auto,q_auto/v1/BuddyCare/givb9chhbptzsvgpp1ge' ,price=22000000, category_id=2)
        p8 = Product(name='Mua Nước Hoa Hồng Hỗ Trợ Cấp Ẩm Estée Lauder Soft Clean Infusion Hydrating Essence Lotion 400ml - Estée Lauder', price=27000000,image='https://res.cloudinary.com/duc03aacd/image/upload/v1706873839/BuddyCare/qvzspevfbonendgenenz.webp' ,category_id=1)
        p6 = Product(name='Kem Chống Nắng Loreal Bright & Clear UV Defender Giảm Thâm', price=22000000,image='https://res.cloudinary.com/duc03aacd/image/upload/v1706873840/BuddyCare/t30k3d7dmuya0ina17uo.jpg', category_id=1)
        db.session.add_all([p1, p2, p3, p4, p5, p6, p8])
        db.session.commit()
