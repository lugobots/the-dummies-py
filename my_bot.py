from lugo4py.loader import EnvVarLoader
from lugo4py.snapshot import GameSnapshotReader
from lugo4py.mapper import Mapper, Region
from lugo4py.stub import Bot, PLAYER_STATE
# from lugo4py.client import NewClientFromConfig

from lugo4py.protos import server_pb2 as Lugo 
from lugo4py.protos.physics_pb2 import Point, Vector 

class MyBot(Bot):

    def __init__(self, side: Lugo.Team.Side, number: int, initPosition: Point, mapper: Mapper):
        self.number = number
        self.mapper = mapper
        self.initPosition = initPosition
        mapper.getRegionFromPoint(initPosition)

    def makeReader(self, snapshot: Lugo.GameSnapshot):
        reader = GameSnapshotReader(snapshot, self.side)
        me = reader.getPlayer(self.side, self.number)
        if me is None:
            raise AttributeError("did not find myself in the game")

        return (reader, me)

    def isNear(self, regionOrigin : Region, destOrigin: Region) -> bool : 
        maxDistance = 2
        return abs(regionOrigin.getRow() - destOrigin.getRow()) <= maxDistance and abs(regionOrigin.getCol() - destOrigin.getCol()) <= maxDistance

    def onDisputing(self,orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot) -> Lugo.OrderSet:
        try:
            # the Lugo.GameSnapshot helps us to read the game state
            (reader, me) = self.makeReader(snapshot)
            ballPosition = reader.getBall().getPosition()

            ballRegion = self.mapper.getRegionFromPoint(ballPosition)
            myRegion = self.mapper.getRegionFromPoint(me.getPosition())

            # by default, let's stay on our region
            moveDestination = self.initPosition

            # but if the ball is near to me, I will try to catch it
            if (self.isNear(ballRegion, myRegion)):
                moveDestination = ballPosition

            moveOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), moveDestination)
            
            # we can ALWAYS try to catch the ball
            catchOrder = reader.makeOrderCatch()

            orderSet.setOrdersList([moveOrder, catchOrder])
            return orderSet

        except Exception:
            print('did not play this turn')

    def onDefending(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot) -> Lugo.OrderSet: 
        try:
            (reader, me) = self.makeReader(snapshot)
            ballPosition = snapshot.getBall().getPosition()
            ballRegion = self.mapper.getRegionFromPoint(ballPosition)
            myRegion = self.mapper.getRegionFromPoint(self.initPosition)

            moveDest = self.initPosition
            if (abs(myRegion.getRow() - ballRegion.getRow()) <= 2 and abs(myRegion.getCol() - ballRegion.getCol()) <= 2):
                moveDest = ballPosition

            moveOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), moveDest)
            catchOrder = reader.makeOrderCatch()

            orderSet = Lugo.OrderSet()
            orderSet.setTurn(snapshot.getTurn())
            orderSet.setDebugMessage("trying to catch the ball")
            orderSet.setOrdersList([moveOrder, catchOrder])
            return orderSet
        except Exception:
            print('did not play this turn')


    def onHolding(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot) -> Lugo.OrderSet: 
        try:
            (reader, me) = self.makeReader(snapshot)

            myGoalCenter = self.mapper.getRegionFromPoint(reader.getOpponentGoal().getCenter())
            currentRegion = self.mapper.getRegionFromPoint(me.getPosition())

            myOrder = None
            if (abs(currentRegion.getRow() - myGoalCenter.getRow()) <= 1 and abs(currentRegion.getCol() - myGoalCenter.getCol()) <= 1):
                myOrder = reader.makeOrderKickMaxSpeed(snapshot.getBall(), reader.getOpponentGoal().getCenter())
            else:
                myOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), reader.getOpponentGoal().getCenter())

            orderSet = Lugo.OrderSet()
            orderSet.setTurn(snapshot.getTurn())
            orderSet.setDebugMessage("attack!")
            orderSet.setOrdersList([myOrder])
            return orderSet
        except Exception:
            print('did not play this turn')

    def onSupporting(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot) -> Lugo.OrderSet: 
        try:
            (reader, me) = self.makeReader(snapshot)
            ballHolderPosition = snapshot.getBall().getPosition()
            myOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), ballHolderPosition)

            orderSet = Lugo.OrderSet()
            orderSet.setTurn(snapshot.getTurn())
            orderSet.setDebugMessage("supporting")
            orderSet.setOrdersList([myOrder])
            return orderSet
        except Exception:
            print('did not play this turn')

    def asGoalkeeper(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot, state) -> Lugo.OrderSet:
        try:
            (reader, me) = self.makeReader(snapshot)
            position = snapshot.getBall().getPosition()
            if (state != PLAYER_STATE.DISPUTING_THE_BALL):
                position = reader.getMyGoal().getCenter()

            myOrder = reader.makeOrderMoveMaxSpeed(me.getPosition(), position)

            orderSet = Lugo.OrderSet()
            orderSet.setTurn(snapshot.getTurn())
            orderSet.setDebugMessage("supporting")
            orderSet.setOrdersList([myOrder, reader.makeOrderCatch()])
            return orderSet
        except Exception:
            print('did not play this turn')


    def gettingReady(self, snapshot: Lugo.GameSnapshot):
        pass

PLAYER_POSITIONS = {
    1:  {'Col': 0, 'Row': 0},
    2:  {'Col': 1, 'Row': 1},
    3:  {'Col': 2, 'Row': 2},
    4:  {'Col': 2, 'Row': 3},
    5:  {'Col': 1, 'Row': 4},
    6:  {'Col': 3, 'Row': 1},
    7:  {'Col': 3, 'Row': 2},
    8:  {'Col': 3, 'Row': 3},
    9:  {'Col': 3, 'Row': 4},
    10: {'Col': 4, 'Row': 3},
    11: {'Col': 4, 'Row': 2},
}