from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime, Float, Date, Boolean
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.functions import current_timestamp
import uuid

Base = declarative_base()

def create_table(engine):
    Base.metadata.create_all(engine)


class SearchResult(Base):
    __tablename__ = 'search_result'
    __table_args__ = (
        UniqueConstraint('search_term', 'asin', name='unique_search_result'),
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_term_id = Column(String, nullable=False)
    search_term = Column(String, nullable=False)
    name = Column(String, nullable=False)
    asin = Column(String, nullable=False)
    url = Column(String)
    amazon_search_url = Column(String)
    star_rating = Column(Float)
    num_of_ratings = Column(Integer)
    price = Column(Float)
    currency = Column(String)
    discount_pct = Column(Float)
    image_urls = Column(ARRAY(String))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=current_timestamp())

class Image(Base):
    __tablename__ = "image"
    checksum = Column(String, primary_key=True)
    related_item_id = Column(String, primary_key=True)
    path = Column(String)
    status = Column(String)
    url = Column(String)


class Asin(Base):
    __tablename__ = "asin"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    __table_args__ = (
        UniqueConstraint('keyword_id', 'asin', name='unique_kw_asin_result'),
    )
    name = Column(String)
    asin = Column(String)
    keyword_id = Column(Integer)
    page_id = Column(Integer)
    price = Column(Float)
    url = Column(String)
    features = Column(String)
    total_ratings = Column(Integer)
    image_urls = Column(ARRAY(String))
    average_rating = Column(Float)
    brand = Column(String)
    brand_url = Column(String)
    details = Column(JSON)
    best_seller_rank = Column(Integer)
    best_seller_category = Column(String)
    other_category_rank = Column(Integer)
    other_category = Column(String)
    description = Column(String)
    is_valid_asin = Column(Boolean)

class Review(Base):
    __tablename__ = 'review'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    related_item_id = Column(UUID(as_uuid=True), ForeignKey('asin.id'))
    header = Column(String)
    body = Column(String)
    review_date = Column(Date)
    reviewer = Column(String)
    purchase_type = Column(String)
    reviewer_location = Column(String)
    reviewer_rating = Column(Float)

class AmazonQuestion(Base):
    __tablename__ = 'question'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    related_item_id = Column(UUID(as_uuid=True), ForeignKey('asin.id'))
    body = Column(String)
    answer = Column(String)
    num_of_votes = Column(Integer)
    num_of_answers = Column(Integer)
    date_answered = Column(Date)
    answered_by = Column(String)
