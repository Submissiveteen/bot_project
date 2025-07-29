# repositories/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

Base = declarative_base()



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    eco_balance: Mapped[float] = mapped_column(default=0.0)
    xp: Mapped[int] = mapped_column(default=0)
    level: Mapped[int] = mapped_column(default=1)
    plastic_total: Mapped[float] = mapped_column(default=0.0)
    upgrade_available: Mapped[bool] = mapped_column(default=False)
    xp_multiplier: Mapped[float] = mapped_column(default=1.0)
    custom_title: Mapped[str] = mapped_column(default=None)




class EcoTransaction(Base):
    __tablename__ = "eco_transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
