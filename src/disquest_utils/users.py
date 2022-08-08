import asyncio

import uvloop
from sqlalchemy import (BigInteger, Boolean, Column, Integer, String, Text,
                        select, update, func)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
class DisQuest(Base):
    __tablename__ = "disquest_users"
    
    user_id = Column(BigInteger)
    guild_id = Column(BigInteger)
    xp = Column(Integer)
    
    def __iter__(self):
        yield "user_id", self.user_id
        yield "guild_id", self.guild_id
        yield "xp", self.xp
        
    def __repr__(self):
        return f"DisQuest(user_id={self.user_id!r}, guild_id={self.guild_id!r}, xp={self.xp!r})"
    
class DisQuestUsers:
    def __init__(self):
        self.self = self
        
    async def initTables(self, uri: str) -> None:
        """Initializes the tables needed for DisQuest

        Args:
            uri (str): Postgres Connection URI
        """
        engine = create_async_engine(uri, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def getUserXP(self, user_id: int, guild_id: int, uri: str):
        """Gets the User's XP

        Args:
            user_id (int): Discord User ID
            guild_id (int): Discord Guild ID
            uri (str): Postgres Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(DisQuest).filter(DisQuest.user_id == user_id).filter(DisQuest.guild_id == guild_id)
                getItemSelected = await session.scalars(selectItem)
                getItemSelectedOne = getItemSelected.first()
                return getItemSelectedOne

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
                
    async def insUser(self, user_id: int, guild_id: int, uri: str) -> None:
        """Inserts a user into the DB for the first time

        Args:
            user_id (int): Discord User ID
            guild_id (int): Discord Guild ID
            uri (str): Postgres Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selItem = select(DisQuest.xp).filter(DisQuest.user_id == user_id).filter(DisQuest.guild_id == guild_id)
                results = await session.execute(selItem)
                resFetchedOne = results.one()
                fullResults = [row for row in resFetchedOne]
                if len(fullResults) == 0:
                    insertData = DisQuest(user_id=user_id, guild_id=guild_id, xp=0)
                    session.add_all([insertData])
                    await session.commit()
                    
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def setUserXP(self, xp: int, user_id: int, guild_id: int, uri: str) -> None:
        """Sets the amount of XP that a user has

        Args:
            xp (int): The amount of XP to set to
            user_id (int): Discord User ID
            guild_id (int): Discord Guild ID
            uri (str): Postgres Connection URI
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateUserXP = update(DisQuest, values={DisQuest.xp: xp}).filter(DisQuest.user_id == user_id).filter(DisQuest.guild_id == guild_id)
                await session.execute(updateUserXP)
                await session.commit()
                
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def addxp(self, offset: int, user_id: int, guild_id: int, uri):
        """Adds the XP to the user

        Args:
            offset (int): The amount to offset by
            uid (int): Discord User ID
            gid (int): Discord Guild ID
            uri (str): Postgres Connection URI
        """
        pxp = await self.getUserXP(user_id, guild_id, uri)
        pxp += offset
        await self.setUserXP(pxp, user_id=user_id, guild_id=guild_id, uri=uri)
        
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def userRank(self, guild_id: int, uri: str) -> list:
        """Gets the user's rank

        Args:
            guild_id (int): Discord Guild ID
            uri (str): Postgres Connection URI

        Returns:
            list: List of results
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(DisQuest.user_id, DisQuest.xp).filter(DisQuest.guild_id == guild_id).order_by(DisQuest.xp.desc())
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]
    
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def globalRank(self, uri: str) -> list:
        """Gets the global rank

        Args:
            uri (str): Postgres Connection URI

        Returns:
            list: List of results
        """
        engine = create_async_engine(uri)
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectGlobalRank = select(DisQuest.id, func.sum(DisQuest.xp).label("txp")).group_by(DisQuest.id).group_by(DisQuest.xp).order_by(DisQuest.xp.desc()).limit(10)
                res = await session.execute(selectGlobalRank)
                return [row for row in res.scalars()]
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())