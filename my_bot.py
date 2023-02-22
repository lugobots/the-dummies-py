from lugo4py.loader import EnvVarLoader
from lugo4py.snapshot import GameSnapshotReader
from lugo4py.mapper import Mapper, Region
from lugo4py.stub import Bot, PLAYER_STATE
# from lugo4py.client import NewClientFromConfig

from lugo4py.protos import server_pb2 as Lugo 
from lugo4py.protos.physics_pb2 import Point, Vector 

import traceback

def getMyExpectedPosition(reader, mapper, number):
    MAPPER_COLS = 10
    MAPPER_ROWS = 6
    # here we define the initial positions
    PLAYER_INITIAL_POSITIONS = {
        1: {'Col': 0, 'Row': 0},
        2: {'Col': 1, 'Row': 1},
        3: {'Col': 2, 'Row': 2},
        4: {'Col': 2, 'Row': 3},
        5: {'Col': 1, 'Row': 4},
        6: {'Col': 3, 'Row': 1},
        7: {'Col': 3, 'Row': 2},
        8: {'Col': 3, 'Row': 3},
        9: {'Col': 3, 'Row': 4},
        10: {'Col': 4, 'Row': 3},
        11: {'Col': 4, 'Row': 2},
    }
    
    PLAYER_TACTIC_POSITIONS = {
        'DEFENSIVE' : {
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
        },
        'NORMAL': {
            2:  {'Col': 2, 'Row': 1},
            3:  {'Col': 4, 'Row': 2},
            4:  {'Col': 4, 'Row': 3},
            5:  {'Col': 2, 'Row': 4},
            6:  {'Col': 6, 'Row': 1},
            7:  {'Col': 8, 'Row': 2},
            8:  {'Col': 8, 'Row': 3},
            9:  {'Col': 6, 'Row': 4},
            10: {'Col': 7, 'Row': 4},
            11: {'Col': 7, 'Row': 1},
        },
        'OFFENSIVE' : {
            2:  {'Col': 3, 'Row': 1},
            3:  {'Col': 5, 'Row': 2},
            4:  {'Col': 5, 'Row': 3},
            5:  {'Col': 3, 'Row': 4},
            6:  {'Col': 7, 'Row': 1},
            7:  {'Col': 8, 'Row': 2},
            8:  {'Col': 8, 'Row': 3},
            9:  {'Col': 7, 'Row': 4},
            10: {'Col': 9, 'Row': 4},
            11: {'Col': 9, 'Row': 1},
        }
    }

    ballRegion = mapper.getRegionFromPoint(reader.getBall().position)
    fieldThird = MAPPER_COLS  / 3
    ballCols = ballRegion.getCol()

    teamState = "OFFENSIVE"
    if (ballCols < fieldThird) :
        teamState = "DEFENSIVE"
    elif (ballCols < fieldThird * 2):
        teamState = "NORMAL"

    expectedRegion = mapper.getRegion(PLAYER_TACTIC_POSITIONS[teamState][number]['Col'], PLAYER_TACTIC_POSITIONS[teamState][number]['Row'])
    return expectedRegion.getCenter()

class MyBot(Bot):

    def __init__(self, side: Lugo.Team.Side, number: int, initPosition: Point, mapper: Mapper):
        self.number = number
        self.side = side
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

    def onDisputing(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot) -> Lugo.OrderSet:
        try:
            orderSet = Lugo.OrderSet()
            
            # the Lugo.GameSnapshot helps us to read the game state
            (reader, me) = self.makeReader(snapshot)
            ballPosition = reader.getBall().position

            ballRegion = self.mapper.getRegionFromPoint(ballPosition)
            myRegion = self.mapper.getRegionFromPoint(me.position)

            # by default, let's stay on our region  
            moveDestination = getMyExpectedPosition(reader, self.mapper, self.number)
            orderSet.debug_message = "Disputing: Returning to my position"

            # but if the ball is near to me, I will try to catch it
            if self.isNear(ballRegion, myRegion):
                moveDestination = ballPosition
                orderSet.debug_message = "Disputing: Trying to catch the ball"

            moveOrder = reader.makeOrderMoveMaxSpeed(me.position, moveDestination)
            
            # we can ALWAYS try to catch the ball
            catchOrder = reader.makeOrderCatch()

            orderSet.turn = snapshot.turn
            orderSet.orders.extend([moveOrder, catchOrder])
            
            return orderSet

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def onDefending(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot) -> Lugo.OrderSet: 
        try:
            orderSet = Lugo.OrderSet()
            
            (reader, me) = self.makeReader(snapshot)
            ballPosition = snapshot.ball.position
            ballRegion = self.mapper.getRegionFromPoint(ballPosition)
            myRegion = self.mapper.getRegionFromPoint(self.initPosition)

            # by default, I will stay at my tactic position
            moveDest = getMyExpectedPosition(reader, self.mapper, self.number)
            orderSet.debug_message = "Defending: returning to my position"
            
            if self.isNear(ballRegion, myRegion):
                moveDest = ballPosition
                orderSet.debug_message = "Defending: trying to catch the ball"

            moveOrder = reader.makeOrderMoveMaxSpeed(me.position, moveDest)
            catchOrder = reader.makeOrderCatch()

            orderSet.turn = snapshot.turn
            orderSet.orders.extend([moveOrder, catchOrder])
            return orderSet
        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()


    def onHolding(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot) -> Lugo.OrderSet: 
        try:
            orderSet = Lugo.OrderSet()
            
            (reader, me) = self.makeReader(snapshot)

            myGoalCenter = self.mapper.getRegionFromPoint(reader.getOpponentGoal().getCenter())
            currentRegion = self.mapper.getRegionFromPoint(me.position)

            myOrder = None
            if self.isNear(currentRegion, myGoalCenter):
                myOrder = reader.makeOrderKickMaxSpeed(snapshot.ball, reader.getOpponentGoal().getCenter())
            else:
                myOrder = reader.makeOrderMoveMaxSpeed(me.position, reader.getOpponentGoal().getCenter())

            orderSet.turn = snapshot.turn
            orderSet.debug_message = "attack!"
            orderSet.orders.append(myOrder)
            return orderSet

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def onSupporting(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot) -> Lugo.OrderSet: 
        try:
            orderSet = Lugo.OrderSet()

            (reader, me) = self.makeReader(snapshot)
            ballHolderPosition = snapshot.ball.position
            ballHolderRegion= self.mapper.getRegionFromPoint(ballHolderPosition)
            myRegion = self.mapper.getRegionFromPoint(self.initPosition)

            moveDest = getMyExpectedPosition(reader, self.mapper, self.number)
            
            if self.isNear(ballHolderRegion, myRegion):
                moveDest = ballHolderPosition

            moveOrder = reader.makeOrderMoveMaxSpeed(me.position, moveDest)

            orderSet.turn = snapshot.turn
            orderSet.debug_message = "supporting"
            orderSet.orders.append(moveOrder)
            return orderSet

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def asGoalkeeper(self, orderSet: Lugo.OrderSet, snapshot: Lugo.GameSnapshot, state) -> Lugo.OrderSet:
        try:
            (reader, me) = self.makeReader(snapshot)
            position = snapshot.ball.position
            if (state != PLAYER_STATE.DISPUTING_THE_BALL):
                position = reader.getMyGoal().getCenter()

            myOrder = reader.makeOrderMoveMaxSpeed(me.position, position)

            orderSet = Lugo.OrderSet()
            orderSet.turn = snapshot.turn
            orderSet.debug_message = "defending the goal"
            orderSet.orders.extend([myOrder, reader.makeOrderCatch()])
            return orderSet

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()


    async def gettingReady(self, snapshot: Lugo.GameSnapshot):
        print('getting ready')

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