
from typing import final

from logging import Logger
from logging import getLogger

from math import pi
from math import sin
from math import atan
from math import cos
from typing import Tuple

from fpdf import FPDF

from pyumldiagrams.IDiagramLine import IDiagramLine
from pyumldiagrams.UnsupportedException import UnsupportedException

from pyumldiagrams.Internal import ArrowPoints
from pyumldiagrams.Internal import DiamondPoints
from pyumldiagrams.Internal import PolygonPoints
from pyumldiagrams.Internal import InternalPosition
from pyumldiagrams.Internal import ScanPoints

from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import Position

from pyumldiagrams.pdf.PdfCommon import PdfCommon


class PdfDiagramLine(IDiagramLine):
    """
    This class takes responsibility for drawing the various types of lines within the
    described UML classes.  End users generally do not directly use this class.
    It is split off as part of the separation of responsibility principle.
    """
    INHERITANCE_ARROW_HEIGHT: final = 10
    DIAMOND_HEIGHT:           final = 8

    def __init__(self, pdf: FPDF, diagramPadding: DiagramPadding, dpi: int):

        super().__init__(docMaker=pdf, diagramPadding=diagramPadding, dpi=dpi)
        self.logger: Logger = getLogger(__name__)

        # self._pdf: FPDF = pdf
        # self._dpi: int  = dpi
        # self._diagramPadding: diagramPadding  = diagramPadding

    def draw(self, lineDefinition: UmlLineDefinition):
        """
        Draw the line described by the input parameter
        Args:
            lineDefinition:  Describes the line to draw
        """

        linePositions: LinePositions = lineDefinition.linePositions
        lineType:      LineType      = lineDefinition.lineType

        if lineType == LineType.Inheritance:
            self._drawInheritanceArrow(linePositions=linePositions)
        elif lineType == LineType.Composition:
            self._drawCompositionSolidDiamond(linePositions=linePositions)
        elif lineType == LineType.Aggregation:
            self._drawAggregationDiamond(linePositions=linePositions)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def _drawInheritanceArrow(self, linePositions: LinePositions):
        """
        Must account for the margins and gaps between drawn shapes
        Must convert to points from screen coordinates
        Draw the arrow first
        Compute the mid point of the bottom line of the arrow
        That is where the line ends

        Args:
            linePositions - The points that describe the line
        """
        lastIdx:       int = len(linePositions) - 1
        beforeLastIdx: int = lastIdx - 1
        endPoints: Tuple[InternalPosition, InternalPosition] = self.__convertEndPoints(linePositions[beforeLastIdx], linePositions[lastIdx])

        convertedSrc:  InternalPosition = endPoints[0]
        convertedDest: InternalPosition = endPoints[1]

        points: ArrowPoints = self.__computeTheArrowVertices(convertedSrc, convertedDest)
        self.__drawPolygon(points)

        newEndPoint: InternalPosition = self.__computeMidPointOfBottomLine(points[0], points[2])

        self.__finishDrawingLine(linePositions=linePositions, newEndPoint=newEndPoint)

    def _drawCompositionSolidDiamond(self, linePositions: LinePositions):

        lastIdx:       int = len(linePositions) - 1
        beforeLastIdx: int = lastIdx - 1
        endPoints: Tuple[InternalPosition, InternalPosition] = self.__convertEndPoints(linePositions[beforeLastIdx], linePositions[lastIdx])

        convertedSrc:  InternalPosition = endPoints[0]
        convertedDest: InternalPosition = endPoints[1]

        points: DiamondPoints = self.__computeDiamondVertices(convertedSrc, convertedDest)
        self.__drawPolygon(points)
        self.__fillInDiamond(points)

        newEndPoint: InternalPosition = points[3]

        self.__finishDrawingLine(linePositions=linePositions, newEndPoint=newEndPoint)

    def _drawAggregationDiamond(self, linePositions: LinePositions):

        lastIdx:   int = len(linePositions) - 1
        beforeLastIdx: int = lastIdx - 1

        endPoints: Tuple[InternalPosition, InternalPosition] = self.__convertEndPoints(linePositions[beforeLastIdx], linePositions[lastIdx])

        convertedSrc:  InternalPosition = endPoints[0]
        convertedDest: InternalPosition = endPoints[1]

        points: ArrowPoints = self.__computeDiamondVertices(convertedSrc, convertedDest)
        self.__drawPolygon(points)

        newEndPoint: InternalPosition = points[3]

        self.__finishDrawingLine(linePositions=linePositions, newEndPoint=newEndPoint)

    def __convertEndPoints(self, src: Position, dest: Position) -> Tuple[InternalPosition, InternalPosition]:

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        x1, y1 = PdfCommon.convertPosition(pos=src, dpi=self._dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)
        x2, y2 = PdfCommon.convertPosition(pos=dest, dpi=self._dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)

        convertedSrc:  InternalPosition = InternalPosition(x1, y1)
        convertedDest: InternalPosition = InternalPosition(x2, y2)

        return convertedSrc, convertedDest

    def __computeTheArrowVertices(self, src: InternalPosition, dest: InternalPosition)  -> ArrowPoints:
        """
        Draw an arrow at the end of the line source-dest.

        Args:
            src:  points of the segment
            dest:  points of the segment

        Returns:
            A list of positions that describes a diamond to draw
        """
        # x1: float = src.x
        # y1: float = src.y
        # x2: float = dest.x
        # y2: float = dest.y
        #
        # deltaX: float = x2 - x1
        # deltaY: float = y2 - y1
        deltaX, deltaY = self.__computeDeltaXDeltaY(src, dest)
        if abs(deltaX) < 0.01:   # vertical segment
            if deltaY > 0:
                alpha = -pi/2
            else:
                alpha = pi/2
        else:
            if deltaX == 0:
                alpha = pi/2
            else:
                alpha = atan(deltaY/deltaX)
        if deltaX > 0:
            alpha += pi

        pi_6: float = pi/6      # radians for 30 degree angle

        alpha1: float = alpha + pi_6
        alpha2: float = alpha - pi_6
        size:   float = PdfDiagramLine.INHERITANCE_ARROW_HEIGHT
        x2: float = dest.x
        y2: float = dest.y
        #
        # The names for the left and right points are correct for upward facing arrows
        # They are inverted for downward facing arrows
        #
        arrowTip:   InternalPosition = InternalPosition(x2, y2)
        rightPoint: InternalPosition = InternalPosition(x2 + size * cos(alpha1), y2 + size * sin(alpha1))
        leftPoint:  InternalPosition = InternalPosition(x2 + size * cos(alpha2), y2 + size * sin(alpha2))

        points: ArrowPoints = [rightPoint, arrowTip, leftPoint]

        return points

    def __computeDiamondVertices(self, src: InternalPosition, dest: InternalPosition) -> DiamondPoints:
        """
        Args:
            src:
            dest:
        """
        pi_6: float = pi/6     # radians for 30 degree angle
        x2:   float = dest.x
        y2:   float = dest.y

        deltaX, deltaY = self.__computeDeltaXDeltaY(src, dest)

        if abs(deltaX) < 0.01:  # vertical segment
            if deltaY > 0:
                alpha = -pi/2
            else:
                alpha = pi/2
        else:
            if deltaX == 0:
                if deltaY > 0:
                    alpha = pi/2
                else:
                    alpha = 3 * pi / 2
            else:
                alpha = atan(deltaY/deltaX)
        if deltaX > 0:
            alpha += pi

        alpha1: float = alpha + pi_6
        alpha2: float = alpha - pi_6
        size:   int   = PdfDiagramLine.DIAMOND_HEIGHT

        # noinspection PyListCreation
        points: DiamondPoints = []

        points.append((InternalPosition(x2 + size * cos(alpha1), y2 + size * sin(alpha1))))
        points.append(InternalPosition(x2, y2))
        points.append(InternalPosition(x2 + size * cos(alpha2), y2 + size * sin(alpha2)))
        points.append(InternalPosition(x2 + 2 * size * cos(alpha), y2 + 2 * size * sin(alpha)))

        return points

    def __drawPolygon(self, points: PolygonPoints):

        pdf: FPDF = self._docMaker
        ptNumber: int = 0
        for point in points:

            x1: float = point.x
            y1: float = point.y

            if ptNumber == len(points) - 1:
                nextPoint = points[0]
                x2: float = nextPoint.x
                y2: float = nextPoint.y
                pdf.line(x1, y1, x2, y2)
                break
            else:
                nextPoint = points[ptNumber + 1]
                x2: float = nextPoint.x
                y2: float = nextPoint.y
                pdf.line(x1, y1, x2, y2)

            ptNumber += 1

    def __computeMidPointOfBottomLine(self, startPos: InternalPosition, endPos: InternalPosition) -> InternalPosition:
        """
        These two coordinates are the two end-points of the bottom leg of the inheritance arrow
        midPoint = (x1+x2/2, y1+y2/2)

        Args:
            startPos: start of line
            endPos:   end of line

        Returns:  Midpoint between startPos - endPos

        """
        x1: float = startPos.x
        y1: float = startPos.y
        x2: float = endPos.x
        y2: float = endPos.y

        midX: float = (x1 + x2) / 2
        midY: float = (y1 + y2) / 2

        return InternalPosition(midX, midY)

    def __computeDeltaXDeltaY(self, src: InternalPosition, dest: InternalPosition) -> Tuple[float, float]:

        x1: float = src.x
        y1: float = src.y
        x2: float = dest.x
        y2: float = dest.y

        deltaX: float = x2 - x1
        deltaY: float = y2 - y1

        return deltaX, deltaY

    def __fillInDiamond(self, points: DiamondPoints):
        """

        Args:
            points:  The polygon that defines the composition diamond

        """
        scanPoints: ScanPoints = PdfCommon.buildScanPoints(points)

        startX: float = scanPoints.startScan.x
        startY: float = scanPoints.startScan.y

        endX: float = scanPoints.endScan.x
        endY: float = scanPoints.endScan.y

        x = startX
        while x <= endX:
            y = startY
            while y <= endY:
                if PdfCommon.pointInsidePolygon(pos=InternalPosition(x, y), polygon=points):
                    self._docMaker.line(x1=x, y1=y, x2=x, y2=y)
                y += 1
            x += 1

    def __finishDrawingLine(self, linePositions: LinePositions, newEndPoint: InternalPosition):

        linePositionsCopy: LinePositions = linePositions[:-1]  # Makes a copy; remove last one

        verticalGap:   int  = self._diagramPadding.verticalGap
        horizontalGap: int  = self._diagramPadding.horizontalGap
        dpi:           int  = self._dpi
        docMaker:      FPDF = self._docMaker
        #
        # Ok, ok, I get it.  This is not a Pythonic 'for' loop.  But, I am not a purist
        #
        numPositions: int      = len(linePositionsCopy)
        currentPos:   Position = linePositionsCopy[0]
        for idx in range(numPositions):

            nextIdx: int = idx + 1
            currentPos = linePositionsCopy[idx]
            if nextIdx == numPositions:
                break
            nextPos: Position = linePositionsCopy[nextIdx]

            curX, curY = PdfCommon.convertPosition(pos=currentPos, dpi=dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)
            nxtX, nxtY = PdfCommon.convertPosition(pos=nextPos, dpi=dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)

            docMaker.line(x1=curX, y1=curY, x2=nxtX, y2=nxtY)

        curX, curY = PdfCommon.convertPosition(pos=currentPos, dpi=dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)
        docMaker.line(x1=curX, y1=curY, x2=newEndPoint.x, y2=newEndPoint.y)
