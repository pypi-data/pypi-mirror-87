import typing

import System
import System.Numerics

System_Numerics_Vector2 = typing.Any
System_Numerics_Vector4 = typing.Any
System_Numerics_Plane = typing.Any
System_Numerics_Vector = typing.Any
System_Numerics_Matrix3x2 = typing.Any
System_Numerics_Matrix4x4 = typing.Any
System_Numerics_Quaternion = typing.Any
System_Numerics_Vector3 = typing.Any

System_Numerics_Vector_T = typing.TypeVar('System_Numerics_Vector_T')


class Matrix3x2(System.IEquatable[System_Numerics_Matrix3x2]):
    """A structure encapsulating a 3x2 matrix."""

    @property
    def M11(self) -> float:
        """The first element of the first row"""
        ...

    @M11.setter
    def M11(self, value: float):
        """The first element of the first row"""
        ...

    @property
    def M12(self) -> float:
        """The second element of the first row"""
        ...

    @M12.setter
    def M12(self, value: float):
        """The second element of the first row"""
        ...

    @property
    def M21(self) -> float:
        """The first element of the second row"""
        ...

    @M21.setter
    def M21(self, value: float):
        """The first element of the second row"""
        ...

    @property
    def M22(self) -> float:
        """The second element of the second row"""
        ...

    @M22.setter
    def M22(self, value: float):
        """The second element of the second row"""
        ...

    @property
    def M31(self) -> float:
        """The first element of the third row"""
        ...

    @M31.setter
    def M31(self, value: float):
        """The first element of the third row"""
        ...

    @property
    def M32(self) -> float:
        """The second element of the third row"""
        ...

    @M32.setter
    def M32(self, value: float):
        """The second element of the third row"""
        ...

    Identity: System.Numerics.Matrix3x2
    """Returns the multiplicative identity matrix."""

    @property
    def IsIdentity(self) -> bool:
        """Returns whether the matrix is the identity matrix."""
        ...

    @property
    def Translation(self) -> System.Numerics.Vector2:
        """Gets or sets the translation component of this matrix."""
        ...

    @Translation.setter
    def Translation(self, value: System.Numerics.Vector2):
        """Gets or sets the translation component of this matrix."""
        ...

    def __init__(self, m11: float, m12: float, m21: float, m22: float, m31: float, m32: float) -> None:
        """Constructs a Matrix3x2 from the given components."""
        ...

    @staticmethod
    def Add(value1: System.Numerics.Matrix3x2, value2: System.Numerics.Matrix3x2) -> System.Numerics.Matrix3x2:
        """
        Adds each matrix element in value1 with its corresponding element in value2.
        
        :param value1: The first source matrix.
        :param value2: The second source matrix.
        :returns: The matrix containing the summed values.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotation(radians: float) -> System.Numerics.Matrix3x2:
        """
        Creates a rotation matrix using the given rotation in radians.
        
        :param radians: The amount of rotation, in radians.
        :returns: A rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotation(radians: float, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a rotation matrix using the given rotation in radians and a center point.
        
        :param radians: The amount of rotation, in radians.
        :param centerPoint: The center point.
        :returns: A rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scales: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a scale matrix from the given vector scale.
        
        :param scales: The scale to use.
        :returns: A scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(xScale: float, yScale: float) -> System.Numerics.Matrix3x2:
        """
        Creates a scale matrix from the given X and Y components.
        
        :param xScale: Value to scale by on the X-axis.
        :param yScale: Value to scale by on the Y-axis.
        :returns: A scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(xScale: float, yScale: float, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a scale matrix that is offset by a given center point.
        
        :param xScale: Value to scale by on the X-axis.
        :param yScale: Value to scale by on the Y-axis.
        :param centerPoint: The center point.
        :returns: A scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scales: System.Numerics.Vector2, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a scale matrix from the given vector scale with an offset from the given center point.
        
        :param scales: The scale to use.
        :param centerPoint: The center offset.
        :returns: A scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scale: float) -> System.Numerics.Matrix3x2:
        """
        Creates a scale matrix that scales uniformly with the given scale.
        
        :param scale: The uniform scale to use.
        :returns: A scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scale: float, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a scale matrix that scales uniformly with the given scale with an offset from the given center.
        
        :param scale: The uniform scale to use.
        :param centerPoint: The center offset.
        :returns: A scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateSkew(radiansX: float, radiansY: float) -> System.Numerics.Matrix3x2:
        """
        Creates a skew matrix from the given angles in radians.
        
        :param radiansX: The X angle, in radians.
        :param radiansY: The Y angle, in radians.
        :returns: A skew matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateSkew(radiansX: float, radiansY: float, centerPoint: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a skew matrix from the given angles in radians and a center point.
        
        :param radiansX: The X angle, in radians.
        :param radiansY: The Y angle, in radians.
        :param centerPoint: The center point.
        :returns: A skew matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateTranslation(position: System.Numerics.Vector2) -> System.Numerics.Matrix3x2:
        """
        Creates a translation matrix from the given vector.
        
        :param position: The translation position.
        :returns: A translation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateTranslation(xPosition: float, yPosition: float) -> System.Numerics.Matrix3x2:
        """
        Creates a translation matrix from the given X and Y components.
        
        :param xPosition: The X position.
        :param yPosition: The Y position.
        :returns: A translation matrix.
        """
        ...

    @staticmethod
    def Invert(matrix: System.Numerics.Matrix3x2, result: System.Numerics.Matrix3x2) -> bool:
        """
        Attempts to invert the given matrix. If the operation succeeds, the inverted matrix is stored in the result parameter.
        
        :param matrix: The source matrix.
        :param result: The output matrix.
        :returns: True if the operation succeeded, False otherwise.
        """
        ...

    @staticmethod
    def Lerp(matrix1: System.Numerics.Matrix3x2, matrix2: System.Numerics.Matrix3x2, amount: float) -> System.Numerics.Matrix3x2:
        """
        Linearly interpolates from matrix1 to matrix2, based on the third parameter.
        
        :param matrix1: The first source matrix.
        :param matrix2: The second source matrix.
        :param amount: The relative weighting of matrix2.
        :returns: The interpolated matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Matrix3x2, value2: System.Numerics.Matrix3x2) -> System.Numerics.Matrix3x2:
        """
        Multiplies two matrices together and returns the resulting matrix.
        
        :param value1: The first source matrix.
        :param value2: The second source matrix.
        :returns: The product matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Matrix3x2, value2: float) -> System.Numerics.Matrix3x2:
        """
        Scales all elements in a matrix by the given scalar factor.
        
        :param value1: The source matrix.
        :param value2: The scaling value to use.
        :returns: The resulting matrix.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Matrix3x2) -> System.Numerics.Matrix3x2:
        """
        Negates the given matrix by multiplying all values by -1.
        
        :param value: The source matrix.
        :returns: The negated matrix.
        """
        ...

    @staticmethod
    def Subtract(value1: System.Numerics.Matrix3x2, value2: System.Numerics.Matrix3x2) -> System.Numerics.Matrix3x2:
        """
        Subtracts each matrix element in value2 from its corresponding element in value1.
        
        :param value1: The first source matrix.
        :param value2: The second source matrix.
        :returns: The matrix containing the resulting values.
        """
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        """
        Returns a boolean indicating whether the given Object is equal to this matrix instance.
        
        :param obj: The Object to compare against.
        :returns: True if the Object is equal to this matrix; False otherwise.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Matrix3x2) -> bool:
        """
        Returns a boolean indicating whether the matrix is equal to the other given matrix.
        
        :param other: The other matrix to test equality against.
        :returns: True if this matrix is equal to other; False otherwise.
        """
        ...

    def GetDeterminant(self) -> float:
        """
        Calculates the determinant for this matrix.
        The determinant is calculated by expanding the matrix with a third column whose values are (0,0,1).
        
        :returns: The determinant.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a String representing this matrix instance.
        
        :returns: The string representation.
        """
        ...


class Vector3(System.IEquatable[System_Numerics_Vector3], System.IFormattable):
    """A structure encapsulating three single precision floating point values and provides hardware accelerated methods."""

    @property
    def X(self) -> float:
        """The X component of the vector."""
        ...

    @X.setter
    def X(self, value: float):
        """The X component of the vector."""
        ...

    @property
    def Y(self) -> float:
        """The Y component of the vector."""
        ...

    @Y.setter
    def Y(self, value: float):
        """The Y component of the vector."""
        ...

    @property
    def Z(self) -> float:
        """The Z component of the vector."""
        ...

    @Z.setter
    def Z(self, value: float):
        """The Z component of the vector."""
        ...

    Zero: System.Numerics.Vector3
    """Returns the vector (0,0,0)."""

    One: System.Numerics.Vector3
    """Returns the vector (1,1,1)."""

    UnitX: System.Numerics.Vector3
    """Returns the vector (1,0,0)."""

    UnitY: System.Numerics.Vector3
    """Returns the vector (0,1,0)."""

    UnitZ: System.Numerics.Vector3
    """Returns the vector (0,0,1)."""

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Constructs a vector whose elements are all the single specified value.
        
        :param value: The element to fill the vector with.
        """
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Vector2, z: float) -> None:
        """
        Constructs a Vector3 from the given Vector2 and a third value.
        
        :param value: The Vector to extract X and Y components from.
        :param z: The Z component.
        """
        ...

    @typing.overload
    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Constructs a vector with the given individual elements.
        
        :param x: The X component.
        :param y: The Y component.
        :param z: The Z component.
        """
        ...

    @staticmethod
    def Abs(value: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector whose elements are the absolute values of each of the source vector's elements.
        
        :param value: The source vector.
        :returns: The absolute value vector.
        """
        ...

    @staticmethod
    def Add(left: System.Numerics.Vector3, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Adds two vectors together.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The summed vector.
        """
        ...

    @staticmethod
    def Clamp(value1: System.Numerics.Vector3, min: System.Numerics.Vector3, max: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Restricts a vector between a min and max value.
        
        :param value1: The source vector.
        :param min: The minimum value.
        :param max: The maximum value.
        :returns: The restricted vector.
        """
        ...

    @staticmethod
    def Cross(vector1: System.Numerics.Vector3, vector2: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Computes the cross product of two vectors.
        
        :param vector1: The first vector.
        :param vector2: The second vector.
        :returns: The cross product.
        """
        ...

    @staticmethod
    def Distance(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3) -> float:
        """
        Returns the Euclidean distance between the two given points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance.
        """
        ...

    @staticmethod
    def DistanceSquared(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3) -> float:
        """
        Returns the Euclidean distance squared between the two given points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance squared.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector3, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Divides the first vector by the second.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The vector resulting from the division.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector3, divisor: float) -> System.Numerics.Vector3:
        """
        Divides the vector by the given scalar.
        
        :param left: The source vector.
        :param divisor: The scalar value.
        :returns: The result of the division.
        """
        ...

    @staticmethod
    def Dot(vector1: System.Numerics.Vector3, vector2: System.Numerics.Vector3) -> float:
        """
        Returns the dot product of two vectors.
        
        :param vector1: The first vector.
        :param vector2: The second vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def Lerp(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3, amount: float) -> System.Numerics.Vector3:
        """
        Linearly interpolates between two vectors based on the given weighting.
        
        :param value1: The first source vector.
        :param value2: The second source vector.
        :param amount: Value between 0 and 1 indicating the weight of the second source vector.
        :returns: The interpolated vector.
        """
        ...

    @staticmethod
    def Max(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector whose elements are the maximum of each of the pairs of elements in the two source vectors.
        
        :param value1: The first source vector.
        :param value2: The second source vector.
        :returns: The maximized vector.
        """
        ...

    @staticmethod
    def Min(value1: System.Numerics.Vector3, value2: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector whose elements are the minimum of each of the pairs of elements in the two source vectors.
        
        :param value1: The first source vector.
        :param value2: The second source vector.
        :returns: The minimized vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector3, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Multiplies two vectors together.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The product vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector3, right: float) -> System.Numerics.Vector3:
        """
        Multiplies a vector by the given scalar.
        
        :param left: The source vector.
        :param right: The scalar value.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: float, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Multiplies a vector by the given scalar.
        
        :param left: The scalar value.
        :param right: The source vector.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Negates a given vector.
        
        :param value: The source vector.
        :returns: The negated vector.
        """
        ...

    @staticmethod
    def Normalize(value: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector with the same direction as the given vector, but with a length of 1.
        
        :param value: The vector to normalize.
        :returns: The normalized vector.
        """
        ...

    @staticmethod
    def Reflect(vector: System.Numerics.Vector3, normal: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns the reflection of a vector off a surface that has the specified normal.
        
        :param vector: The source vector.
        :param normal: The normal of the surface being reflected off.
        :returns: The reflected vector.
        """
        ...

    @staticmethod
    def SquareRoot(value: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Returns a vector whose elements are the square root of each of the source vector's elements.
        
        :param value: The source vector.
        :returns: The square root vector.
        """
        ...

    @staticmethod
    def Subtract(left: System.Numerics.Vector3, right: System.Numerics.Vector3) -> System.Numerics.Vector3:
        """
        Subtracts the second vector from the first.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The difference vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector3, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector3:
        """
        Transforms a vector by the given matrix.
        
        :param position: The source vector.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector3, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector3:
        """
        Transforms a vector by the given Quaternion rotation value.
        
        :param value: The source vector to be rotated.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    def TransformNormal(normal: System.Numerics.Vector3, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector3:
        """
        Transforms a vector normal by the given matrix.
        
        :param normal: The source vector.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float]) -> None:
        """Copies the contents of the vector into the given array."""
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float], index: int) -> None:
        """Copies the contents of the vector into the given array, starting from index."""
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        """
        Returns a boolean indicating whether the given Object is equal to this Vector3 instance.
        
        :param obj: The Object to compare against.
        :returns: True if the Object is equal to this Vector3; False otherwise.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Vector3) -> bool:
        """
        Returns a boolean indicating whether the given Vector3 is equal to this Vector3 instance.
        
        :param other: The Vector3 to compare this instance to.
        :returns: True if the other Vector3 is equal to this instance; False otherwise.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def Length(self) -> float:
        """
        Returns the length of the vector.
        
        :returns: The vector's length.
        """
        ...

    def LengthSquared(self) -> float:
        """
        Returns the length of the vector squared. This operation is cheaper than Length().
        
        :returns: The vector's length squared.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        """
        Returns a String representing this Vector3 instance.
        
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str) -> str:
        """
        Returns a String representing this Vector3 instance, using the specified format to format individual elements.
        
        :param format: The format of individual elements.
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str, formatProvider: System.IFormatProvider) -> str:
        """
        Returns a String representing this Vector3 instance, using the specified format to format individual elements and the given IFormatProvider.
        
        :param format: The format of individual elements.
        :param formatProvider: The format provider to use when formatting elements.
        :returns: The string representation.
        """
        ...


class Quaternion(System.IEquatable[System_Numerics_Quaternion]):
    """Represents a vector that is used to encode three-dimensional physical rotations."""

    @property
    def X(self) -> float:
        """Specifies the X-value of the vector component of the Quaternion."""
        ...

    @X.setter
    def X(self, value: float):
        """Specifies the X-value of the vector component of the Quaternion."""
        ...

    @property
    def Y(self) -> float:
        """Specifies the Y-value of the vector component of the Quaternion."""
        ...

    @Y.setter
    def Y(self, value: float):
        """Specifies the Y-value of the vector component of the Quaternion."""
        ...

    @property
    def Z(self) -> float:
        """Specifies the Z-value of the vector component of the Quaternion."""
        ...

    @Z.setter
    def Z(self, value: float):
        """Specifies the Z-value of the vector component of the Quaternion."""
        ...

    @property
    def W(self) -> float:
        """Specifies the rotation component of the Quaternion."""
        ...

    @W.setter
    def W(self, value: float):
        """Specifies the rotation component of the Quaternion."""
        ...

    Identity: System.Numerics.Quaternion
    """Returns a Quaternion representing no rotation."""

    @property
    def IsIdentity(self) -> bool:
        """Returns whether the Quaternion is the identity Quaternion."""
        ...

    @typing.overload
    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        """
        Constructs a Quaternion from the given components.
        
        :param x: The X component of the Quaternion.
        :param y: The Y component of the Quaternion.
        :param z: The Z component of the Quaternion.
        :param w: The W component of the Quaternion.
        """
        ...

    @typing.overload
    def __init__(self, vectorPart: System.Numerics.Vector3, scalarPart: float) -> None:
        """
        Constructs a Quaternion from the given vector and rotation parts.
        
        :param vectorPart: The vector part of the Quaternion.
        :param scalarPart: The rotation part of the Quaternion.
        """
        ...

    @staticmethod
    def Add(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Adds two Quaternions element-by-element.
        
        :param value1: The first source Quaternion.
        :param value2: The second source Quaternion.
        :returns: The result of adding the Quaternions.
        """
        ...

    @staticmethod
    def Concatenate(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Concatenates two Quaternions; the result represents the value1 rotation followed by the value2 rotation.
        
        :param value1: The first Quaternion rotation in the series.
        :param value2: The second Quaternion rotation in the series.
        :returns: A new Quaternion representing the concatenation of the value1 rotation followed by the value2 rotation.
        """
        ...

    @staticmethod
    def Conjugate(value: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Creates the conjugate of a specified Quaternion.
        
        :param value: The Quaternion of which to return the conjugate.
        :returns: A new Quaternion that is the conjugate of the specified one.
        """
        ...

    @staticmethod
    def CreateFromAxisAngle(axis: System.Numerics.Vector3, angle: float) -> System.Numerics.Quaternion:
        """
        Creates a Quaternion from a normalized vector axis and an angle to rotate about the vector.
        
        :param axis: The unit vector to rotate around. This vector must be normalized before calling this function or the resulting Quaternion will be incorrect.
        :param angle: The angle, in radians, to rotate around the vector.
        :returns: The created Quaternion.
        """
        ...

    @staticmethod
    def CreateFromRotationMatrix(matrix: System.Numerics.Matrix4x4) -> System.Numerics.Quaternion:
        """
        Creates a Quaternion from the given rotation matrix.
        
        :param matrix: The rotation matrix.
        :returns: The created Quaternion.
        """
        ...

    @staticmethod
    def CreateFromYawPitchRoll(yaw: float, pitch: float, roll: float) -> System.Numerics.Quaternion:
        """
        Creates a new Quaternion from the given yaw, pitch, and roll, in radians.
        
        :param yaw: The yaw angle, in radians, around the Y-axis.
        :param pitch: The pitch angle, in radians, around the X-axis.
        :param roll: The roll angle, in radians, around the Z-axis.
        """
        ...

    @staticmethod
    def Divide(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Divides a Quaternion by another Quaternion.
        
        :param value1: The source Quaternion.
        :param value2: The divisor.
        :returns: The result of the division.
        """
        ...

    @staticmethod
    def Dot(quaternion1: System.Numerics.Quaternion, quaternion2: System.Numerics.Quaternion) -> float:
        """
        Calculates the dot product of two Quaternions.
        
        :param quaternion1: The first source Quaternion.
        :param quaternion2: The second source Quaternion.
        :returns: The dot product of the Quaternions.
        """
        ...

    @staticmethod
    def Inverse(value: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Returns the inverse of a Quaternion.
        
        :param value: The source Quaternion.
        :returns: The inverted Quaternion.
        """
        ...

    @staticmethod
    def Lerp(quaternion1: System.Numerics.Quaternion, quaternion2: System.Numerics.Quaternion, amount: float) -> System.Numerics.Quaternion:
        """
        Linearly interpolates between two quaternions.
        
        :param quaternion1: The first source Quaternion.
        :param quaternion2: The second source Quaternion.
        :param amount: The relative weight of the second source Quaternion in the interpolation.
        :returns: The interpolated Quaternion.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Multiplies two Quaternions together.
        
        :param value1: The Quaternion on the left side of the multiplication.
        :param value2: The Quaternion on the right side of the multiplication.
        :returns: The result of the multiplication.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Quaternion, value2: float) -> System.Numerics.Quaternion:
        """
        Multiplies a Quaternion by a scalar value.
        
        :param value1: The source Quaternion.
        :param value2: The scalar value.
        :returns: The result of the multiplication.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Flips the sign of each component of the quaternion.
        
        :param value: The source Quaternion.
        :returns: The negated Quaternion.
        """
        ...

    @staticmethod
    def Normalize(value: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Divides each component of the Quaternion by the length of the Quaternion.
        
        :param value: The source Quaternion.
        :returns: The normalized Quaternion.
        """
        ...

    @staticmethod
    def Slerp(quaternion1: System.Numerics.Quaternion, quaternion2: System.Numerics.Quaternion, amount: float) -> System.Numerics.Quaternion:
        """
        Interpolates between two quaternions, using spherical linear interpolation.
        
        :param quaternion1: The first source Quaternion.
        :param quaternion2: The second source Quaternion.
        :param amount: The relative weight of the second source Quaternion in the interpolation.
        :returns: The interpolated Quaternion.
        """
        ...

    @staticmethod
    def Subtract(value1: System.Numerics.Quaternion, value2: System.Numerics.Quaternion) -> System.Numerics.Quaternion:
        """
        Subtracts one Quaternion from another.
        
        :param value1: The first source Quaternion.
        :param value2: The second Quaternion, to be subtracted from the first.
        :returns: The result of the subtraction.
        """
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        """
        Returns a boolean indicating whether the given Object is equal to this Quaternion instance.
        
        :param obj: The Object to compare against.
        :returns: True if the Object is equal to this Quaternion; False otherwise.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Quaternion) -> bool:
        """
        Returns a boolean indicating whether the given Quaternion is equal to this Quaternion instance.
        
        :param other: The Quaternion to compare this instance to.
        :returns: True if the other Quaternion is equal to this instance; False otherwise.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def Length(self) -> float:
        """
        Calculates the length of the Quaternion.
        
        :returns: The computed length of the Quaternion.
        """
        ...

    def LengthSquared(self) -> float:
        """
        Calculates the length squared of the Quaternion. This operation is cheaper than Length().
        
        :returns: The length squared of the Quaternion.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a String representing this Quaternion instance.
        
        :returns: The string representation.
        """
        ...


class Matrix4x4(System.IEquatable[System_Numerics_Matrix4x4]):
    """A structure encapsulating a 4x4 matrix."""

    @property
    def M11(self) -> float:
        """Value at row 1, column 1 of the matrix."""
        ...

    @M11.setter
    def M11(self, value: float):
        """Value at row 1, column 1 of the matrix."""
        ...

    @property
    def M12(self) -> float:
        """Value at row 1, column 2 of the matrix."""
        ...

    @M12.setter
    def M12(self, value: float):
        """Value at row 1, column 2 of the matrix."""
        ...

    @property
    def M13(self) -> float:
        """Value at row 1, column 3 of the matrix."""
        ...

    @M13.setter
    def M13(self, value: float):
        """Value at row 1, column 3 of the matrix."""
        ...

    @property
    def M14(self) -> float:
        """Value at row 1, column 4 of the matrix."""
        ...

    @M14.setter
    def M14(self, value: float):
        """Value at row 1, column 4 of the matrix."""
        ...

    @property
    def M21(self) -> float:
        """Value at row 2, column 1 of the matrix."""
        ...

    @M21.setter
    def M21(self, value: float):
        """Value at row 2, column 1 of the matrix."""
        ...

    @property
    def M22(self) -> float:
        """Value at row 2, column 2 of the matrix."""
        ...

    @M22.setter
    def M22(self, value: float):
        """Value at row 2, column 2 of the matrix."""
        ...

    @property
    def M23(self) -> float:
        """Value at row 2, column 3 of the matrix."""
        ...

    @M23.setter
    def M23(self, value: float):
        """Value at row 2, column 3 of the matrix."""
        ...

    @property
    def M24(self) -> float:
        """Value at row 2, column 4 of the matrix."""
        ...

    @M24.setter
    def M24(self, value: float):
        """Value at row 2, column 4 of the matrix."""
        ...

    @property
    def M31(self) -> float:
        """Value at row 3, column 1 of the matrix."""
        ...

    @M31.setter
    def M31(self, value: float):
        """Value at row 3, column 1 of the matrix."""
        ...

    @property
    def M32(self) -> float:
        """Value at row 3, column 2 of the matrix."""
        ...

    @M32.setter
    def M32(self, value: float):
        """Value at row 3, column 2 of the matrix."""
        ...

    @property
    def M33(self) -> float:
        """Value at row 3, column 3 of the matrix."""
        ...

    @M33.setter
    def M33(self, value: float):
        """Value at row 3, column 3 of the matrix."""
        ...

    @property
    def M34(self) -> float:
        """Value at row 3, column 4 of the matrix."""
        ...

    @M34.setter
    def M34(self, value: float):
        """Value at row 3, column 4 of the matrix."""
        ...

    @property
    def M41(self) -> float:
        """Value at row 4, column 1 of the matrix."""
        ...

    @M41.setter
    def M41(self, value: float):
        """Value at row 4, column 1 of the matrix."""
        ...

    @property
    def M42(self) -> float:
        """Value at row 4, column 2 of the matrix."""
        ...

    @M42.setter
    def M42(self, value: float):
        """Value at row 4, column 2 of the matrix."""
        ...

    @property
    def M43(self) -> float:
        """Value at row 4, column 3 of the matrix."""
        ...

    @M43.setter
    def M43(self, value: float):
        """Value at row 4, column 3 of the matrix."""
        ...

    @property
    def M44(self) -> float:
        """Value at row 4, column 4 of the matrix."""
        ...

    @M44.setter
    def M44(self, value: float):
        """Value at row 4, column 4 of the matrix."""
        ...

    Identity: System.Numerics.Matrix4x4
    """Returns the multiplicative identity matrix."""

    @property
    def IsIdentity(self) -> bool:
        """Returns whether the matrix is the identity matrix."""
        ...

    @property
    def Translation(self) -> System.Numerics.Vector3:
        """Gets or sets the translation component of this matrix."""
        ...

    @Translation.setter
    def Translation(self, value: System.Numerics.Vector3):
        """Gets or sets the translation component of this matrix."""
        ...

    @typing.overload
    def __init__(self, m11: float, m12: float, m13: float, m14: float, m21: float, m22: float, m23: float, m24: float, m31: float, m32: float, m33: float, m34: float, m41: float, m42: float, m43: float, m44: float) -> None:
        """Constructs a Matrix4x4 from the given components."""
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Matrix3x2) -> None:
        """
        Constructs a Matrix4x4 from the given Matrix3x2.
        
        :param value: The source Matrix3x2.
        """
        ...

    @staticmethod
    def Add(value1: System.Numerics.Matrix4x4, value2: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Adds two matrices together.
        
        :param value1: The first source matrix.
        :param value2: The second source matrix.
        :returns: The resulting matrix.
        """
        ...

    @staticmethod
    def CreateBillboard(objectPosition: System.Numerics.Vector3, cameraPosition: System.Numerics.Vector3, cameraUpVector: System.Numerics.Vector3, cameraForwardVector: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a spherical billboard that rotates around a specified object position.
        
        :param objectPosition: Position of the object the billboard will rotate around.
        :param cameraPosition: Position of the camera.
        :param cameraUpVector: The up vector of the camera.
        :param cameraForwardVector: The forward vector of the camera.
        :returns: The created billboard matrix
        """
        ...

    @staticmethod
    def CreateConstrainedBillboard(objectPosition: System.Numerics.Vector3, cameraPosition: System.Numerics.Vector3, rotateAxis: System.Numerics.Vector3, cameraForwardVector: System.Numerics.Vector3, objectForwardVector: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a cylindrical billboard that rotates around a specified axis.
        
        :param objectPosition: Position of the object the billboard will rotate around.
        :param cameraPosition: Position of the camera.
        :param rotateAxis: Axis to rotate the billboard around.
        :param cameraForwardVector: Forward vector of the camera.
        :param objectForwardVector: Forward vector of the object.
        :returns: The created billboard matrix.
        """
        ...

    @staticmethod
    def CreateFromAxisAngle(axis: System.Numerics.Vector3, angle: float) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix that rotates around an arbitrary vector.
        
        :param axis: The axis to rotate around.
        :param angle: The angle to rotate around the given axis, in radians.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    def CreateFromQuaternion(quaternion: System.Numerics.Quaternion) -> System.Numerics.Matrix4x4:
        """
        Creates a rotation matrix from the given Quaternion rotation value.
        
        :param quaternion: The source Quaternion.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    def CreateFromYawPitchRoll(yaw: float, pitch: float, roll: float) -> System.Numerics.Matrix4x4:
        """
        Creates a rotation matrix from the specified yaw, pitch, and roll.
        
        :param yaw: Angle of rotation, in radians, around the Y-axis.
        :param pitch: Angle of rotation, in radians, around the X-axis.
        :param roll: Angle of rotation, in radians, around the Z-axis.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    def CreateLookAt(cameraPosition: System.Numerics.Vector3, cameraTarget: System.Numerics.Vector3, cameraUpVector: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a view matrix.
        
        :param cameraPosition: The position of the camera.
        :param cameraTarget: The target towards which the camera is pointing.
        :param cameraUpVector: The direction that is "up" from the camera's point of view.
        :returns: The view matrix.
        """
        ...

    @staticmethod
    def CreateOrthographic(width: float, height: float, zNearPlane: float, zFarPlane: float) -> System.Numerics.Matrix4x4:
        """
        Creates an orthographic perspective matrix from the given view volume dimensions.
        
        :param width: Width of the view volume.
        :param height: Height of the view volume.
        :param zNearPlane: Minimum Z-value of the view volume.
        :param zFarPlane: Maximum Z-value of the view volume.
        :returns: The orthographic projection matrix.
        """
        ...

    @staticmethod
    def CreateOrthographicOffCenter(left: float, right: float, bottom: float, top: float, zNearPlane: float, zFarPlane: float) -> System.Numerics.Matrix4x4:
        """
        Builds a customized, orthographic projection matrix.
        
        :param left: Minimum X-value of the view volume.
        :param right: Maximum X-value of the view volume.
        :param bottom: Minimum Y-value of the view volume.
        :param top: Maximum Y-value of the view volume.
        :param zNearPlane: Minimum Z-value of the view volume.
        :param zFarPlane: Maximum Z-value of the view volume.
        :returns: The orthographic projection matrix.
        """
        ...

    @staticmethod
    def CreatePerspective(width: float, height: float, nearPlaneDistance: float, farPlaneDistance: float) -> System.Numerics.Matrix4x4:
        """
        Creates a perspective projection matrix from the given view volume dimensions.
        
        :param width: Width of the view volume at the near view plane.
        :param height: Height of the view volume at the near view plane.
        :param nearPlaneDistance: Distance to the near view plane.
        :param farPlaneDistance: Distance to the far view plane.
        :returns: The perspective projection matrix.
        """
        ...

    @staticmethod
    def CreatePerspectiveFieldOfView(fieldOfView: float, aspectRatio: float, nearPlaneDistance: float, farPlaneDistance: float) -> System.Numerics.Matrix4x4:
        """
        Creates a perspective projection matrix based on a field of view, aspect ratio, and near and far view plane distances.
        
        :param fieldOfView: Field of view in the y direction, in radians.
        :param aspectRatio: Aspect ratio, defined as view space width divided by height.
        :param nearPlaneDistance: Distance to the near view plane.
        :param farPlaneDistance: Distance to the far view plane.
        :returns: The perspective projection matrix.
        """
        ...

    @staticmethod
    def CreatePerspectiveOffCenter(left: float, right: float, bottom: float, top: float, nearPlaneDistance: float, farPlaneDistance: float) -> System.Numerics.Matrix4x4:
        """
        Creates a customized, perspective projection matrix.
        
        :param left: Minimum x-value of the view volume at the near view plane.
        :param right: Maximum x-value of the view volume at the near view plane.
        :param bottom: Minimum y-value of the view volume at the near view plane.
        :param top: Maximum y-value of the view volume at the near view plane.
        :param nearPlaneDistance: Distance to the near view plane.
        :param farPlaneDistance: Distance to of the far view plane.
        :returns: The perspective projection matrix.
        """
        ...

    @staticmethod
    def CreateReflection(value: System.Numerics.Plane) -> System.Numerics.Matrix4x4:
        """
        Creates a Matrix that reflects the coordinate system about a specified Plane.
        
        :param value: The Plane about which to create a reflection.
        :returns: A new matrix expressing the reflection.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationX(radians: float) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the X-axis.
        
        :param radians: The amount, in radians, by which to rotate around the X-axis.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationX(radians: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the X-axis, from a center point.
        
        :param radians: The amount, in radians, by which to rotate around the X-axis.
        :param centerPoint: The center point.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationY(radians: float) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the Y-axis.
        
        :param radians: The amount, in radians, by which to rotate around the Y-axis.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationY(radians: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the Y-axis, from a center point.
        
        :param radians: The amount, in radians, by which to rotate around the Y-axis.
        :param centerPoint: The center point.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationZ(radians: float) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the Z-axis.
        
        :param radians: The amount, in radians, by which to rotate around the Z-axis.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateRotationZ(radians: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a matrix for rotating points around the Z-axis, from a center point.
        
        :param radians: The amount, in radians, by which to rotate around the Z-axis.
        :param centerPoint: The center point.
        :returns: The rotation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(xScale: float, yScale: float, zScale: float) -> System.Numerics.Matrix4x4:
        """
        Creates a scaling matrix.
        
        :param xScale: Value to scale by on the X-axis.
        :param yScale: Value to scale by on the Y-axis.
        :param zScale: Value to scale by on the Z-axis.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(xScale: float, yScale: float, zScale: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a scaling matrix with a center point.
        
        :param xScale: Value to scale by on the X-axis.
        :param yScale: Value to scale by on the Y-axis.
        :param zScale: Value to scale by on the Z-axis.
        :param centerPoint: The center point.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scales: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a scaling matrix.
        
        :param scales: The vector containing the amount to scale by on each axis.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scales: System.Numerics.Vector3, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a scaling matrix with a center point.
        
        :param scales: The vector containing the amount to scale by on each axis.
        :param centerPoint: The center point.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scale: float) -> System.Numerics.Matrix4x4:
        """
        Creates a uniform scaling matrix that scales equally on each axis.
        
        :param scale: The uniform scaling factor.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateScale(scale: float, centerPoint: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a uniform scaling matrix that scales equally on each axis with a center point.
        
        :param scale: The uniform scaling factor.
        :param centerPoint: The center point.
        :returns: The scaling matrix.
        """
        ...

    @staticmethod
    def CreateShadow(lightDirection: System.Numerics.Vector3, plane: System.Numerics.Plane) -> System.Numerics.Matrix4x4:
        """
        Creates a Matrix that flattens geometry into a specified Plane as if casting a shadow from a specified light source.
        
        :param lightDirection: The direction from which the light that will cast the shadow is coming.
        :param plane: The Plane onto which the new matrix should flatten geometry so as to cast a shadow.
        :returns: A new Matrix that can be used to flatten geometry onto the specified plane from the specified direction.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateTranslation(position: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a translation matrix.
        
        :param position: The amount to translate in each axis.
        :returns: The translation matrix.
        """
        ...

    @staticmethod
    @typing.overload
    def CreateTranslation(xPosition: float, yPosition: float, zPosition: float) -> System.Numerics.Matrix4x4:
        """
        Creates a translation matrix.
        
        :param xPosition: The amount to translate on the X-axis.
        :param yPosition: The amount to translate on the Y-axis.
        :param zPosition: The amount to translate on the Z-axis.
        :returns: The translation matrix.
        """
        ...

    @staticmethod
    def CreateWorld(position: System.Numerics.Vector3, forward: System.Numerics.Vector3, up: System.Numerics.Vector3) -> System.Numerics.Matrix4x4:
        """
        Creates a world matrix with the specified parameters.
        
        :param position: The position of the object; used in translation operations.
        :param forward: Forward direction of the object.
        :param up: Upward direction of the object; usually [0, 1, 0].
        :returns: The world matrix.
        """
        ...

    @staticmethod
    def Invert(matrix: System.Numerics.Matrix4x4, result: System.Numerics.Matrix4x4) -> bool:
        """
        Attempts to calculate the inverse of the given matrix. If successful, result will contain the inverted matrix.
        
        :param matrix: The source matrix to invert.
        :param result: If successful, contains the inverted matrix.
        :returns: True if the source matrix could be inverted; False otherwise.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Matrix4x4, value2: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Multiplies a matrix by another matrix.
        
        :param value1: The first source matrix.
        :param value2: The second source matrix.
        :returns: The result of the multiplication.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(value1: System.Numerics.Matrix4x4, value2: float) -> System.Numerics.Matrix4x4:
        """
        Multiplies a matrix by a scalar value.
        
        :param value1: The source matrix.
        :param value2: The scaling factor.
        :returns: The scaled matrix.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Returns a new matrix with the negated elements of the given matrix.
        
        :param value: The source matrix.
        :returns: The negated matrix.
        """
        ...

    @staticmethod
    def Subtract(value1: System.Numerics.Matrix4x4, value2: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Subtracts the second matrix from the first.
        
        :param value1: The first source matrix.
        :param value2: The second source matrix.
        :returns: The result of the subtraction.
        """
        ...

    @staticmethod
    def Decompose(matrix: System.Numerics.Matrix4x4, scale: System.Numerics.Vector3, rotation: System.Numerics.Quaternion, translation: System.Numerics.Vector3) -> bool:
        """
        Attempts to extract the scale, translation, and rotation components from the given scale/rotation/translation matrix.
        If successful, the out parameters will contained the extracted values.
        
        :param matrix: The source matrix.
        :param scale: The scaling component of the transformation matrix.
        :param rotation: The rotation component of the transformation matrix.
        :param translation: The translation component of the transformation matrix
        :returns: True if the source matrix was successfully decomposed; False otherwise.
        """
        ...

    @staticmethod
    def Lerp(matrix1: System.Numerics.Matrix4x4, matrix2: System.Numerics.Matrix4x4, amount: float) -> System.Numerics.Matrix4x4:
        """
        Linearly interpolates between the corresponding values of two matrices.
        
        :param matrix1: The first source matrix.
        :param matrix2: The second source matrix.
        :param amount: The relative weight of the second source matrix.
        :returns: The interpolated matrix.
        """
        ...

    @staticmethod
    def Transform(value: System.Numerics.Matrix4x4, rotation: System.Numerics.Quaternion) -> System.Numerics.Matrix4x4:
        """
        Transforms the given matrix by applying the given Quaternion rotation.
        
        :param value: The source matrix to transform.
        :param rotation: The rotation to apply.
        :returns: The transformed matrix.
        """
        ...

    @staticmethod
    def Transpose(matrix: System.Numerics.Matrix4x4) -> System.Numerics.Matrix4x4:
        """
        Transposes the rows and columns of a matrix.
        
        :param matrix: The source matrix.
        :returns: The transposed matrix.
        """
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        """
        Returns a boolean indicating whether the given Object is equal to this matrix instance.
        
        :param obj: The Object to compare against.
        :returns: True if the Object is equal to this matrix; False otherwise.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Matrix4x4) -> bool:
        """
        Returns a boolean indicating whether this matrix instance is equal to the other given matrix.
        
        :param other: The matrix to compare this instance to.
        :returns: True if the matrices are equal; False otherwise.
        """
        ...

    def GetDeterminant(self) -> float:
        """
        Calculates the determinant of the matrix.
        
        :returns: The determinant of the matrix.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a String representing this matrix instance.
        
        :returns: The string representation.
        """
        ...


class Vector2(System.IEquatable[System_Numerics_Vector2], System.IFormattable):
    """A structure encapsulating two single precision floating point values and provides hardware accelerated methods."""

    @property
    def X(self) -> float:
        """The X component of the vector."""
        ...

    @X.setter
    def X(self, value: float):
        """The X component of the vector."""
        ...

    @property
    def Y(self) -> float:
        """The Y component of the vector."""
        ...

    @Y.setter
    def Y(self, value: float):
        """The Y component of the vector."""
        ...

    Zero: System.Numerics.Vector2
    """Returns the vector (0,0)."""

    One: System.Numerics.Vector2
    """Returns the vector (1,1)."""

    UnitX: System.Numerics.Vector2
    """Returns the vector (1,0)."""

    UnitY: System.Numerics.Vector2
    """Returns the vector (0,1)."""

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Constructs a vector whose elements are all the single specified value.
        
        :param value: The element to fill the vector with.
        """
        ...

    @typing.overload
    def __init__(self, x: float, y: float) -> None:
        """
        Constructs a vector with the given individual elements.
        
        :param x: The X component.
        :param y: The Y component.
        """
        ...

    @staticmethod
    def Abs(value: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector whose elements are the absolute values of each of the source vector's elements.
        
        :param value: The source vector.
        :returns: The absolute value vector.
        """
        ...

    @staticmethod
    def Add(left: System.Numerics.Vector2, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Adds two vectors together.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The summed vector.
        """
        ...

    @staticmethod
    def Clamp(value1: System.Numerics.Vector2, min: System.Numerics.Vector2, max: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Restricts a vector between a min and max value.
        
        :param value1: The source vector.
        :param min: The minimum value.
        :param max: The maximum value.
        """
        ...

    @staticmethod
    def Distance(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> float:
        """
        Returns the Euclidean distance between the two given points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance.
        """
        ...

    @staticmethod
    def DistanceSquared(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> float:
        """
        Returns the Euclidean distance squared between the two given points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance squared.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector2, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Divides the first vector by the second.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The vector resulting from the division.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector2, divisor: float) -> System.Numerics.Vector2:
        """
        Divides the vector by the given scalar.
        
        :param left: The source vector.
        :param divisor: The scalar value.
        :returns: The result of the division.
        """
        ...

    @staticmethod
    def Dot(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> float:
        """
        Returns the dot product of two vectors.
        
        :param value1: The first vector.
        :param value2: The second vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def Lerp(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2, amount: float) -> System.Numerics.Vector2:
        """
        Linearly interpolates between two vectors based on the given weighting.
        
        :param value1: The first source vector.
        :param value2: The second source vector.
        :param amount: Value between 0 and 1 indicating the weight of the second source vector.
        :returns: The interpolated vector.
        """
        ...

    @staticmethod
    def Max(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector whose elements are the maximum of each of the pairs of elements in the two source vectors
        
        :param value1: The first source vector
        :param value2: The second source vector
        :returns: The maximized vector
        """
        ...

    @staticmethod
    def Min(value1: System.Numerics.Vector2, value2: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector whose elements are the minimum of each of the pairs of elements in the two source vectors.
        
        :param value1: The first source vector.
        :param value2: The second source vector.
        :returns: The minimized vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector2, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Multiplies two vectors together.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The product vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector2, right: float) -> System.Numerics.Vector2:
        """
        Multiplies a vector by the given scalar.
        
        :param left: The source vector.
        :param right: The scalar value.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: float, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Multiplies a vector by the given scalar.
        
        :param left: The scalar value.
        :param right: The source vector.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Negates a given vector.
        
        :param value: The source vector.
        :returns: The negated vector.
        """
        ...

    @staticmethod
    def Normalize(value: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector with the same direction as the given vector, but with a length of 1.
        
        :param value: The vector to normalize.
        :returns: The normalized vector.
        """
        ...

    @staticmethod
    def Reflect(vector: System.Numerics.Vector2, normal: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns the reflection of a vector off a surface that has the specified normal.
        
        :param vector: The source vector.
        :param normal: The normal of the surface being reflected off.
        :returns: The reflected vector.
        """
        ...

    @staticmethod
    def SquareRoot(value: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Returns a vector whose elements are the square root of each of the source vector's elements.
        
        :param value: The source vector.
        :returns: The square root vector.
        """
        ...

    @staticmethod
    def Subtract(left: System.Numerics.Vector2, right: System.Numerics.Vector2) -> System.Numerics.Vector2:
        """
        Subtracts the second vector from the first.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The difference vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector2, matrix: System.Numerics.Matrix3x2) -> System.Numerics.Vector2:
        """
        Transforms a vector by the given matrix.
        
        :param position: The source vector.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector2, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector2:
        """
        Transforms a vector by the given matrix.
        
        :param position: The source vector.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector2, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector2:
        """
        Transforms a vector by the given Quaternion rotation value.
        
        :param value: The source vector to be rotated.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def TransformNormal(normal: System.Numerics.Vector2, matrix: System.Numerics.Matrix3x2) -> System.Numerics.Vector2:
        """
        Transforms a vector normal by the given matrix.
        
        :param normal: The source vector.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def TransformNormal(normal: System.Numerics.Vector2, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector2:
        """
        Transforms a vector normal by the given matrix.
        
        :param normal: The source vector.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float]) -> None:
        """
        Copies the contents of the vector into the given array.
        
        :param array: The destination array.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float], index: int) -> None:
        """Copies the contents of the vector into the given array, starting from the given index."""
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        """
        Returns a boolean indicating whether the given Object is equal to this Vector2 instance.
        
        :param obj: The Object to compare against.
        :returns: True if the Object is equal to this Vector2; False otherwise.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Vector2) -> bool:
        """
        Returns a boolean indicating whether the given Vector2 is equal to this Vector2 instance.
        
        :param other: The Vector2 to compare this instance to.
        :returns: True if the other Vector2 is equal to this instance; False otherwise.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def Length(self) -> float:
        """
        Returns the length of the vector.
        
        :returns: The vector's length.
        """
        ...

    def LengthSquared(self) -> float:
        """
        Returns the length of the vector squared. This operation is cheaper than Length().
        
        :returns: The vector's length squared.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        """
        Returns a String representing this Vector2 instance.
        
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str) -> str:
        """
        Returns a String representing this Vector2 instance, using the specified format to format individual elements.
        
        :param format: The format of individual elements.
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str, formatProvider: System.IFormatProvider) -> str:
        """
        Returns a String representing this Vector2 instance, using the specified format to format individual elements and the given IFormatProvider.
        
        :param format: The format of individual elements.
        :param formatProvider: The format provider to use when formatting elements.
        :returns: The string representation.
        """
        ...


class BitOperations(System.Object):
    """
    Utility methods for intrinsic bit-twiddling operations.
    The methods use hardware intrinsics when available on the underlying platform,
    otherwise they use optimized software fallbacks.
    """

    @staticmethod
    @typing.overload
    def LeadingZeroCount(value: int) -> int:
        """
        Count the number of leading zero bits in a mask.
        Similar in behavior to the x86 instruction LZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def LeadingZeroCount(value: int) -> int:
        """
        Count the number of leading zero bits in a mask.
        Similar in behavior to the x86 instruction LZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def Log2(value: int) -> int:
        """
        Returns the integer (floor) log of the specified value, base 2.
        Note that by convention, input value 0 returns 0 since log(0) is undefined.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def Log2(value: int) -> int:
        """
        Returns the integer (floor) log of the specified value, base 2.
        Note that by convention, input value 0 returns 0 since log(0) is undefined.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def PopCount(value: int) -> int:
        """
        Returns the population count (number of bits set) of a mask.
        Similar in behavior to the x86 instruction POPCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def PopCount(value: int) -> int:
        """
        Returns the population count (number of bits set) of a mask.
        Similar in behavior to the x86 instruction POPCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def TrailingZeroCount(value: int) -> int:
        """
        Count the number of trailing zero bits in an integer value.
        Similar in behavior to the x86 instruction TZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def TrailingZeroCount(value: int) -> int:
        """
        Count the number of trailing zero bits in an integer value.
        Similar in behavior to the x86 instruction TZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def TrailingZeroCount(value: int) -> int:
        """
        Count the number of trailing zero bits in a mask.
        Similar in behavior to the x86 instruction TZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def TrailingZeroCount(value: int) -> int:
        """
        Count the number of trailing zero bits in a mask.
        Similar in behavior to the x86 instruction TZCNT.
        
        :param value: The value.
        """
        ...

    @staticmethod
    @typing.overload
    def RotateLeft(value: int, offset: int) -> int:
        """
        Rotates the specified value left by the specified number of bits.
        Similar in behavior to the x86 instruction ROL.
        
        :param value: The value to rotate.
        :param offset: The number of bits to rotate by. Any value outside the range [0..31] is treated as congruent mod 32.
        :returns: The rotated value.
        """
        ...

    @staticmethod
    @typing.overload
    def RotateLeft(value: int, offset: int) -> int:
        """
        Rotates the specified value left by the specified number of bits.
        Similar in behavior to the x86 instruction ROL.
        
        :param value: The value to rotate.
        :param offset: The number of bits to rotate by. Any value outside the range [0..63] is treated as congruent mod 64.
        :returns: The rotated value.
        """
        ...

    @staticmethod
    @typing.overload
    def RotateRight(value: int, offset: int) -> int:
        """
        Rotates the specified value right by the specified number of bits.
        Similar in behavior to the x86 instruction ROR.
        
        :param value: The value to rotate.
        :param offset: The number of bits to rotate by. Any value outside the range [0..31] is treated as congruent mod 32.
        :returns: The rotated value.
        """
        ...

    @staticmethod
    @typing.overload
    def RotateRight(value: int, offset: int) -> int:
        """
        Rotates the specified value right by the specified number of bits.
        Similar in behavior to the x86 instruction ROR.
        
        :param value: The value to rotate.
        :param offset: The number of bits to rotate by. Any value outside the range [0..63] is treated as congruent mod 64.
        :returns: The rotated value.
        """
        ...


class Vector4(System.IEquatable[System_Numerics_Vector4], System.IFormattable):
    """A structure encapsulating four single precision floating point values and provides hardware accelerated methods."""

    @property
    def X(self) -> float:
        """The X component of the vector."""
        ...

    @X.setter
    def X(self, value: float):
        """The X component of the vector."""
        ...

    @property
    def Y(self) -> float:
        """The Y component of the vector."""
        ...

    @Y.setter
    def Y(self, value: float):
        """The Y component of the vector."""
        ...

    @property
    def Z(self) -> float:
        """The Z component of the vector."""
        ...

    @Z.setter
    def Z(self, value: float):
        """The Z component of the vector."""
        ...

    @property
    def W(self) -> float:
        """The W component of the vector."""
        ...

    @W.setter
    def W(self, value: float):
        """The W component of the vector."""
        ...

    Zero: System.Numerics.Vector4
    """Returns the vector (0,0,0,0)."""

    One: System.Numerics.Vector4
    """Returns the vector (1,1,1,1)."""

    UnitX: System.Numerics.Vector4
    """Returns the vector (1,0,0,0)."""

    UnitY: System.Numerics.Vector4
    """Returns the vector (0,1,0,0)."""

    UnitZ: System.Numerics.Vector4
    """Returns the vector (0,0,1,0)."""

    UnitW: System.Numerics.Vector4
    """Returns the vector (0,0,0,1)."""

    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Constructs a vector whose elements are all the single specified value.
        
        :param value: The element to fill the vector with.
        """
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Vector2, z: float, w: float) -> None:
        """
        Constructs a Vector4 from the given Vector2 and a Z and W component.
        
        :param value: The vector to use as the X and Y components.
        :param z: The Z component.
        :param w: The W component.
        """
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Vector3, w: float) -> None:
        """
        Constructs a Vector4 from the given Vector3 and a W component.
        
        :param value: The vector to use as the X, Y, and Z components.
        :param w: The W component.
        """
        ...

    @typing.overload
    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        """
        Constructs a vector with the given individual elements.
        
        :param x: X component.
        :param y: Y component.
        :param z: Z component.
        :param w: W component.
        """
        ...

    @staticmethod
    def Abs(value: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector whose elements are the absolute values of each of the source vector's elements.
        
        :param value: The source vector.
        :returns: The absolute value vector.
        """
        ...

    @staticmethod
    def Add(left: System.Numerics.Vector4, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Adds two vectors together.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The summed vector.
        """
        ...

    @staticmethod
    def Clamp(value1: System.Numerics.Vector4, min: System.Numerics.Vector4, max: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Restricts a vector between a min and max value.
        
        :param value1: The source vector.
        :param min: The minimum value.
        :param max: The maximum value.
        :returns: The restricted vector.
        """
        ...

    @staticmethod
    def Distance(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4) -> float:
        """
        Returns the Euclidean distance between the two given points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance.
        """
        ...

    @staticmethod
    def DistanceSquared(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4) -> float:
        """
        Returns the Euclidean distance squared between the two given points.
        
        :param value1: The first point.
        :param value2: The second point.
        :returns: The distance squared.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector4, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Divides the first vector by the second.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The vector resulting from the division.
        """
        ...

    @staticmethod
    @typing.overload
    def Divide(left: System.Numerics.Vector4, divisor: float) -> System.Numerics.Vector4:
        """
        Divides the vector by the given scalar.
        
        :param left: The source vector.
        :param divisor: The scalar value.
        :returns: The result of the division.
        """
        ...

    @staticmethod
    def Dot(vector1: System.Numerics.Vector4, vector2: System.Numerics.Vector4) -> float:
        """
        Returns the dot product of two vectors.
        
        :param vector1: The first vector.
        :param vector2: The second vector.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def Lerp(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4, amount: float) -> System.Numerics.Vector4:
        """
        Linearly interpolates between two vectors based on the given weighting.
        
        :param value1: The first source vector.
        :param value2: The second source vector.
        :param amount: Value between 0 and 1 indicating the weight of the second source vector.
        :returns: The interpolated vector.
        """
        ...

    @staticmethod
    def Max(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector whose elements are the maximum of each of the pairs of elements in the two source vectors.
        
        :param value1: The first source vector.
        :param value2: The second source vector.
        :returns: The maximized vector.
        """
        ...

    @staticmethod
    def Min(value1: System.Numerics.Vector4, value2: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector whose elements are the minimum of each of the pairs of elements in the two source vectors.
        
        :param value1: The first source vector.
        :param value2: The second source vector.
        :returns: The minimized vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector4, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Multiplies two vectors together.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The product vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector4, right: float) -> System.Numerics.Vector4:
        """
        Multiplies a vector by the given scalar.
        
        :param left: The source vector.
        :param right: The scalar value.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: float, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Multiplies a vector by the given scalar.
        
        :param left: The scalar value.
        :param right: The source vector.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Negates a given vector.
        
        :param value: The source vector.
        :returns: The negated vector.
        """
        ...

    @staticmethod
    def Normalize(vector: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector with the same direction as the given vector, but with a length of 1.
        
        :param vector: The vector to normalize.
        :returns: The normalized vector.
        """
        ...

    @staticmethod
    def SquareRoot(value: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Returns a vector whose elements are the square root of each of the source vector's elements.
        
        :param value: The source vector.
        :returns: The square root vector.
        """
        ...

    @staticmethod
    def Subtract(left: System.Numerics.Vector4, right: System.Numerics.Vector4) -> System.Numerics.Vector4:
        """
        Subtracts the second vector from the first.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The difference vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector2, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector4:
        """
        Transforms a vector by the given matrix.
        
        :param position: The source vector.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector2, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector4:
        """
        Transforms a vector by the given Quaternion rotation value.
        
        :param value: The source vector to be rotated.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(position: System.Numerics.Vector3, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector4:
        """
        Transforms a vector by the given matrix.
        
        :param position: The source vector.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector3, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector4:
        """
        Transforms a vector by the given Quaternion rotation value.
        
        :param value: The source vector to be rotated.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(vector: System.Numerics.Vector4, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Vector4:
        """
        Transforms a vector by the given matrix.
        
        :param vector: The source vector.
        :param matrix: The transformation matrix.
        :returns: The transformed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(value: System.Numerics.Vector4, rotation: System.Numerics.Quaternion) -> System.Numerics.Vector4:
        """
        Transforms a vector by the given Quaternion rotation value.
        
        :param value: The source vector to be rotated.
        :param rotation: The rotation to apply.
        :returns: The transformed vector.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float]) -> None:
        """Copies the contents of the vector into the given array."""
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[float], index: int) -> None:
        """Copies the contents of the vector into the given array, starting from index."""
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Vector4) -> bool:
        """
        Returns a boolean indicating whether the given Vector4 is equal to this Vector4 instance.
        
        :param other: The Vector4 to compare this instance to.
        :returns: True if the other Vector4 is equal to this instance; False otherwise.
        """
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        """
        Returns a boolean indicating whether the given Object is equal to this Vector4 instance.
        
        :param obj: The Object to compare against.
        :returns: True if the Object is equal to this Vector4; False otherwise.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def Length(self) -> float:
        """
        Returns the length of the vector. This operation is cheaper than Length().
        
        :returns: The vector's length.
        """
        ...

    def LengthSquared(self) -> float:
        """
        Returns the length of the vector squared.
        
        :returns: The vector's length squared.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        """
        Returns a String representing this Vector4 instance.
        
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str) -> str:
        """
        Returns a String representing this Vector4 instance, using the specified format to format individual elements.
        
        :param format: The format of individual elements.
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str, formatProvider: System.IFormatProvider) -> str:
        """
        Returns a String representing this Vector4 instance, using the specified format to format individual elements
        and the given IFormatProvider.
        
        :param format: The format of individual elements.
        :param formatProvider: The format provider to use when formatting elements.
        :returns: The string representation.
        """
        ...


class Plane(System.IEquatable[System_Numerics_Plane]):
    """A structure encapsulating a 3D Plane"""

    @property
    def Normal(self) -> System.Numerics.Vector3:
        """The normal vector of the Plane."""
        ...

    @Normal.setter
    def Normal(self, value: System.Numerics.Vector3):
        """The normal vector of the Plane."""
        ...

    @property
    def D(self) -> float:
        """The distance of the Plane along its normal from the origin."""
        ...

    @D.setter
    def D(self, value: float):
        """The distance of the Plane along its normal from the origin."""
        ...

    @typing.overload
    def __init__(self, x: float, y: float, z: float, d: float) -> None:
        """
        Constructs a Plane from the X, Y, and Z components of its normal, and its distance from the origin on that normal.
        
        :param x: The X-component of the normal.
        :param y: The Y-component of the normal.
        :param z: The Z-component of the normal.
        :param d: The distance of the Plane along its normal from the origin.
        """
        ...

    @typing.overload
    def __init__(self, normal: System.Numerics.Vector3, d: float) -> None:
        """
        Constructs a Plane from the given normal and distance along the normal from the origin.
        
        :param normal: The Plane's normal vector.
        :param d: The Plane's distance from the origin along its normal vector.
        """
        ...

    @typing.overload
    def __init__(self, value: System.Numerics.Vector4) -> None:
        """
        Constructs a Plane from the given Vector4.
        
        :param value: A vector whose first 3 elements describe the normal vector, and whose W component defines the distance along that normal from the origin.
        """
        ...

    @staticmethod
    def CreateFromVertices(point1: System.Numerics.Vector3, point2: System.Numerics.Vector3, point3: System.Numerics.Vector3) -> System.Numerics.Plane:
        """
        Creates a Plane that contains the three given points.
        
        :param point1: The first point defining the Plane.
        :param point2: The second point defining the Plane.
        :param point3: The third point defining the Plane.
        :returns: The Plane containing the three points.
        """
        ...

    @staticmethod
    def Dot(plane: System.Numerics.Plane, value: System.Numerics.Vector4) -> float:
        """
        Calculates the dot product of a Plane and Vector4.
        
        :param plane: The Plane.
        :param value: The Vector4.
        :returns: The dot product.
        """
        ...

    @staticmethod
    def DotCoordinate(plane: System.Numerics.Plane, value: System.Numerics.Vector3) -> float:
        """
        Returns the dot product of a specified Vector3 and the normal vector of this Plane plus the distance (D) value of the Plane.
        
        :param plane: The plane.
        :param value: The Vector3.
        :returns: The resulting value.
        """
        ...

    @staticmethod
    def DotNormal(plane: System.Numerics.Plane, value: System.Numerics.Vector3) -> float:
        """
        Returns the dot product of a specified Vector3 and the Normal vector of this Plane.
        
        :param plane: The plane.
        :param value: The Vector3.
        :returns: The resulting dot product.
        """
        ...

    @staticmethod
    def Normalize(value: System.Numerics.Plane) -> System.Numerics.Plane:
        """
        Creates a new Plane whose normal vector is the source Plane's normal vector normalized.
        
        :param value: The source Plane.
        :returns: The normalized Plane.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(plane: System.Numerics.Plane, matrix: System.Numerics.Matrix4x4) -> System.Numerics.Plane:
        """
        Transforms a normalized Plane by a Matrix.
        
        :param plane: The normalized Plane to transform. This Plane must already be normalized, so that its Normal vector is of unit length, before this method is called.
        :param matrix: The transformation matrix to apply to the Plane.
        :returns: The transformed Plane.
        """
        ...

    @staticmethod
    @typing.overload
    def Transform(plane: System.Numerics.Plane, rotation: System.Numerics.Quaternion) -> System.Numerics.Plane:
        """
        Transforms a normalized Plane by a Quaternion rotation.
        
        :param plane: The normalized Plane to transform. This Plane must already be normalized, so that its Normal vector is of unit length, before this method is called.
        :param rotation: The Quaternion rotation to apply to the Plane.
        :returns: A new Plane that results from applying the rotation.
        """
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        """
        Returns a boolean indicating whether the given Object is equal to this Plane instance.
        
        :param obj: The Object to compare against.
        :returns: True if the Object is equal to this Plane; False otherwise.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Plane) -> bool:
        """
        Returns a boolean indicating whether the given Plane is equal to this Plane instance.
        
        :param other: The Plane to compare this instance to.
        :returns: True if the other Plane is equal to this instance; False otherwise.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a String representing this Plane instance.
        
        :returns: The string representation.
        """
        ...


class Vector(typing.Generic[System_Numerics_Vector_T], System.IEquatable[System_Numerics_Vector], System.IFormattable):
    """This class has no documentation."""

    IsHardwareAccelerated: bool

    Count: int
    """Returns the number of elements stored in the vector. This value is hardware dependent."""

    Zero: System.Numerics.Vector[System_Numerics_Vector_T]
    """Returns a vector containing all zeroes."""

    One: System.Numerics.Vector[System_Numerics_Vector_T]
    """Returns a vector containing all ones."""

    AllBitsSet: System.Numerics.Vector[System_Numerics_Vector_T]

    @staticmethod
    @typing.overload
    def ConditionalSelect(condition: System.Numerics.Vector[int], left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Creates a new vector with elements selected between the two given source vectors, and based on a mask vector.
        
        :param condition: The integral mask vector used to drive selection.
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The new vector with elements selected based on the mask.
        """
        ...

    @staticmethod
    @typing.overload
    def ConditionalSelect(condition: System.Numerics.Vector[int], left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Creates a new vector with elements selected between the two given source vectors, and based on a mask vector.
        
        :param condition: The integral mask vector used to drive selection.
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The new vector with elements selected based on the mask.
        """
        ...

    @staticmethod
    @typing.overload
    def ConditionalSelect(condition: System.Numerics.Vector[System_Numerics_Vector_T], left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Creates a new vector with elements selected between the two given source vectors, and based on a mask vector.
        
        :param condition: The mask vector used to drive selection.
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The new vector with elements selected based on the mask.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements signal whether the elements in left and right were equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether elements in the left and right floating point vectors were equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left and right were equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether elements in the left and right floating point vectors were equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Equals(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left and right were equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    def EqualsAll(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether each pair of elements in the given vectors are equal.
        
        :param left: The first vector to compare.
        :param right: The first vector to compare.
        :returns: True if all elements are equal; False otherwise.
        """
        ...

    @staticmethod
    def EqualsAny(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether any single pair of elements in the given vectors are equal.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: True if any element pairs are equal; False if no element pairs are equal.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements signal whether the elements in left were less than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether the elements in left were less than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left were less than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether the elements in left were less than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThan(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left were less than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    def LessThanAll(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether all of the elements in left are less than their corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: True if all elements in left are less than their corresponding elements in right; False otherwise.
        """
        ...

    @staticmethod
    def LessThanAny(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether any element in left is less than its corresponding element in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: True if any elements in left are less than their corresponding elements in right; False otherwise.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements signal whether the elements in left were less than or equal to their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether the elements in left were less than or equal to their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left were less than or equal to their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left were less than or equal to their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def LessThanOrEqual(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether the elements in left were less than or equal to their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant integral vector.
        """
        ...

    @staticmethod
    def LessThanOrEqualAll(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether all elements in left are less than or equal to their corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: True if all elements in left are less than or equal to their corresponding elements in right; False otherwise.
        """
        ...

    @staticmethod
    def LessThanOrEqualAny(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether any element in left is less than or equal to its corresponding element in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: True if any elements in left are less than their corresponding elements in right; False otherwise.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements signal whether the elements in left were greater than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether the elements in left were greater than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left were greater than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether the elements in left were greater than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThan(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left were greater than their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    def GreaterThanAll(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether all elements in left are greater than the corresponding elements in right.
        elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: True if all elements in left are greater than their corresponding elements in right; False otherwise.
        """
        ...

    @staticmethod
    def GreaterThanAny(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether any element in left is greater than its corresponding element in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: True if any elements in left are greater than their corresponding elements in right; False otherwise.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements signal whether the elements in left were greater than or equal to their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether the elements in left were greater than or equal to their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant integral vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left were greater than or equal to their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[int], right: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Returns a new vector whose elements signal whether the elements in left were greater than or equal to their
        corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    @typing.overload
    def GreaterThanOrEqual(left: System.Numerics.Vector[float], right: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Returns an integral vector whose elements signal whether the elements in left were greater than or equal to
        their corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: The resultant integral vector.
        """
        ...

    @staticmethod
    def GreaterThanOrEqualAll(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether all of the elements in left are greater than or equal to
        their corresponding elements in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: True if all elements in left are greater than or equal to their corresponding elements in right; False otherwise.
        """
        ...

    @staticmethod
    def GreaterThanOrEqualAny(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether any element in left is greater than or equal to its corresponding element in right.
        
        :param left: The first vector to compare.
        :param right: The second vector to compare.
        :returns: True if any elements in left are greater than or equal to their corresponding elements in right; False otherwise.
        """
        ...

    @staticmethod
    def Abs(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        ...

    @staticmethod
    def Min(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements are the minimum of each pair of elements in the two given vectors.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The minimum vector.
        """
        ...

    @staticmethod
    def Max(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements are the maximum of each pair of elements in the two given vectors.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The maximum vector.
        """
        ...

    @staticmethod
    def Dot(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System_Numerics_Vector_T:
        ...

    @staticmethod
    def SquareRoot(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements are the square roots of the given vector's elements.
        
        :param value: The source vector.
        :returns: The square root vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Ceiling(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Returns a new vector whose elements are the smallest integral values that are greater than or equal to the given vector's elements.
        
        :param value: The source vector.
        :returns: The vector whose elements are the smallest integral values that are greater than or equal to the given vector's elements. If a value is equal to float.NaN, float.NegativeInfinity or float.PositiveInfinity, that value is returned. Note that this method returns a float instead of an integral type.
        """
        ...

    @staticmethod
    @typing.overload
    def Ceiling(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Returns a new vector whose elements are the smallest integral values that are greater than or equal to the given vector's elements.
        
        :param value: The source vector.
        :returns: The vector whose elements are the smallest integral values that are greater than or equal to the given vector's elements. If a value is equal to double.NaN, double.NegativeInfinity or double.PositiveInfinity, that value is returned. Note that this method returns a double instead of an integral type.
        """
        ...

    @staticmethod
    @typing.overload
    def Floor(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Returns a new vector whose elements are the largest integral values that are less than or equal to the given vector's elements.
        
        :param value: The source vector.
        :returns: The vector whose elements are the largest integral values that are less than or equal to the given vector's elements. If a value is equal to float.NaN, float.NegativeInfinity or float.PositiveInfinity, that value is returned. Note that this method returns a float instead of an integral type.
        """
        ...

    @staticmethod
    @typing.overload
    def Floor(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Returns a new vector whose elements are the largest integral values that are less than or equal to the given vector's elements.
        
        :param value: The source vector.
        :returns: The vector whose elements are the largest integral values that are less than or equal to the given vector's elements. If a value is equal to double.NaN, double.NegativeInfinity or double.PositiveInfinity, that value is returned. Note that this method returns a double instead of an integral type.
        """
        ...

    @staticmethod
    def Add(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Creates a new vector whose values are the sum of each pair of elements from the two given vectors.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The summed vector.
        """
        ...

    @staticmethod
    def Subtract(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Creates a new vector whose values are the difference between each pairs of elements in the given vectors.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The difference vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Creates a new vector whose values are the product of each pair of elements from the two given vectors.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The summed vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System_Numerics_Vector_T) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose values are the values of the given vector each multiplied by a scalar value.
        
        :param left: The source vector.
        :param right: The scalar factor.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Multiply(left: System_Numerics_Vector_T, right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose values are the values of the given vector each multiplied by a scalar value.
        
        :param left: The scalar factor.
        :param right: The source vector.
        :returns: The scaled vector.
        """
        ...

    @staticmethod
    def Divide(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose values are the result of dividing the first vector's elements
        by the corresponding elements in the second vector.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The divided vector.
        """
        ...

    @staticmethod
    def Negate(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements are the given vector's elements negated.
        
        :param value: The source vector.
        :returns: The negated vector.
        """
        ...

    @staticmethod
    def BitwiseAnd(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector by performing a bitwise-and operation on each of the elements in the given vectors.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    def BitwiseOr(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector by performing a bitwise-or operation on each of the elements in the given vectors.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    def OnesComplement(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector whose elements are obtained by taking the one's complement of the given vector's elements.
        
        :param value: The source vector.
        :returns: The one's complement vector.
        """
        ...

    @staticmethod
    def Xor(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector by performing a bitwise-exclusive-or operation on each of the elements in the given vectors.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    def AndNot(left: System.Numerics.Vector[System_Numerics_Vector_T], right: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[System_Numerics_Vector_T]:
        """
        Returns a new vector by performing a bitwise-and-not operation on each of the elements in the given vectors.
        
        :param left: The first source vector.
        :param right: The second source vector.
        :returns: The resultant vector.
        """
        ...

    @staticmethod
    def AsVectorByte(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of the given vector into those of a vector of unsigned bytes.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorSByte(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of the given vector into those of a vector of signed bytes.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorUInt16(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of the given vector into those of a vector of 16-bit integers.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorInt16(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of the given vector into those of a vector of signed 16-bit integers.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorUInt32(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of the given vector into those of a vector of unsigned 32-bit integers.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorInt32(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of the given vector into those of a vector of signed 32-bit integers.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorUInt64(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of the given vector into those of a vector of unsigned 64-bit integers.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorInt64(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[int]:
        """
        Reinterprets the bits of the given vector into those of a vector of signed 64-bit integers.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorSingle(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[float]:
        """
        Reinterprets the bits of the given vector into those of a vector of 32-bit floating point numbers.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    def AsVectorDouble(value: System.Numerics.Vector[System_Numerics_Vector_T]) -> System.Numerics.Vector[float]:
        """
        Reinterprets the bits of the given vector into those of a vector of 64-bit floating point numbers.
        
        :param value: The source vector
        :returns: The reinterpreted vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector{Byte} into two Vector{UInt16}'s.
        The source vector whose elements are widened into the outputs.The first output vector, whose elements will contain the widened elements from lower indices in the source vector.The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector{UInt16} into two Vector{UInt32}'s.
        The source vector whose elements are widened into the outputs.The first output vector, whose elements will contain the widened elements from lower indices in the source vector.The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector{UInt32} into two Vector{UInt64}'s.
        The source vector whose elements are widened into the outputs.The first output vector, whose elements will contain the widened elements from lower indices in the source vector.The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector{SByte} into two Vector{Int16}'s.
        The source vector whose elements are widened into the outputs.The first output vector, whose elements will contain the widened elements from lower indices in the source vector.The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector{Int16} into two Vector{Int32}'s.
        The source vector whose elements are widened into the outputs.The first output vector, whose elements will contain the widened elements from lower indices in the source vector.The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[int], low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> None:
        """
        Widens a Vector{Int32} into two Vector{Int64}'s.
        The source vector whose elements are widened into the outputs.The first output vector, whose elements will contain the widened elements from lower indices in the source vector.The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Widen(source: System.Numerics.Vector[float], low: System.Numerics.Vector[float], high: System.Numerics.Vector[float]) -> None:
        """
        Widens a Vector{Single} into two Vector{Double}'s.
        The source vector whose elements are widened into the outputs.The first output vector, whose elements will contain the widened elements from lower indices in the source vector.The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        
        :param source: The source vector whose elements are widened into the outputs.
        :param low: The first output vector, whose elements will contain the widened elements from lower indices in the source vector.
        :param high: The second output vector, whose elements will contain the widened elements from higher indices in the source vector.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector{UInt16}'s into one Vector{Byte}.
        The first source vector, whose elements become the lower-index elements of the return value.The second source vector, whose elements become the higher-index elements of the return value.A Vector{Byte} containing elements narrowed from the source vectors.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector{UInt32}'s into one Vector{UInt16}.
        The first source vector, whose elements become the lower-index elements of the return value.The second source vector, whose elements become the higher-index elements of the return value.A Vector{UInt16} containing elements narrowed from the source vectors.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector{UInt64}'s into one Vector{UInt32}.
        The first source vector, whose elements become the lower-index elements of the return value.The second source vector, whose elements become the higher-index elements of the return value.A Vector{UInt32} containing elements narrowed from the source vectors.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector{Int16}'s into one Vector{SByte}.
        The first source vector, whose elements become the lower-index elements of the return value.The second source vector, whose elements become the higher-index elements of the return value.A Vector{SByte} containing elements narrowed from the source vectors.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector{Int32}'s into one Vector{Int16}.
        The first source vector, whose elements become the lower-index elements of the return value.The second source vector, whose elements become the higher-index elements of the return value.A Vector{Int16} containing elements narrowed from the source vectors.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[int], high: System.Numerics.Vector[int]) -> System.Numerics.Vector[int]:
        """
        Narrows two Vector{Int64}'s into one Vector{Int32}.
        The first source vector, whose elements become the lower-index elements of the return value.The second source vector, whose elements become the higher-index elements of the return value.A Vector{Int32} containing elements narrowed from the source vectors.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        """
        ...

    @staticmethod
    @typing.overload
    def Narrow(low: System.Numerics.Vector[float], high: System.Numerics.Vector[float]) -> System.Numerics.Vector[float]:
        """
        Narrows two Vector{Double}'s into one Vector{Single}.
        The first source vector, whose elements become the lower-index elements of the return value.The second source vector, whose elements become the higher-index elements of the return value.A Vector{Single} containing elements narrowed from the source vectors.
        
        :param low: The first source vector, whose elements become the lower-index elements of the return value.
        :param high: The second source vector, whose elements become the higher-index elements of the return value.
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertToSingle(value: System.Numerics.Vector[int]) -> System.Numerics.Vector[float]:
        """
        Converts a Vector{Int32} to a Vector{Single}.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertToSingle(value: System.Numerics.Vector[int]) -> System.Numerics.Vector[float]:
        """
        Converts a Vector{UInt32} to a Vector{Single}.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertToDouble(value: System.Numerics.Vector[int]) -> System.Numerics.Vector[float]:
        """
        Converts a Vector{Int64} to a Vector{Double}.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertToDouble(value: System.Numerics.Vector[int]) -> System.Numerics.Vector[float]:
        """
        Converts a Vector{UInt64} to a Vector{Double}.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    def ConvertToInt32(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Converts a Vector{Single} to a Vector{Int32}.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    def ConvertToUInt32(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Converts a Vector{Single} to a Vector{UInt32}.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    def ConvertToInt64(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Converts a Vector{Double} to a Vector{Int64}.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @staticmethod
    def ConvertToUInt64(value: System.Numerics.Vector[float]) -> System.Numerics.Vector[int]:
        """
        Converts a Vector{Double} to a Vector{UInt64}.
        
        :param value: The source vector.
        :returns: The converted vector.
        """
        ...

    @typing.overload
    def __init__(self, value: System_Numerics_Vector_T) -> None:
        """Constructs a vector whose components are all ."""
        ...

    @typing.overload
    def __init__(self, values: typing.List[System_Numerics_Vector_T]) -> None:
        """Constructs a vector from the given array. The size of the given array must be at least Count."""
        ...

    @typing.overload
    def __init__(self, values: typing.List[System_Numerics_Vector_T], index: int) -> None:
        """
        Constructs a vector from the given array, starting from the given index.
        The array must contain at least Count from the given index.
        """
        ...

    @typing.overload
    def __init__(self, values: System.ReadOnlySpan[int]) -> None:
        """
        Constructs a vector from the given ReadOnlySpan{Byte}.
        The span must contain at least Vector{Byte}.Count elements.
        """
        ...

    @typing.overload
    def __init__(self, values: System.ReadOnlySpan[System_Numerics_Vector_T]) -> None:
        """
        Constructs a vector from the given ReadOnlySpan{T}.
        The span must contain at least Count elements.
        """
        ...

    @typing.overload
    def __init__(self, values: System.Span[System_Numerics_Vector_T]) -> None:
        """
        Constructs a vector from the given Span{T}.
        The span must contain at least Count elements.
        """
        ...

    @typing.overload
    def CopyTo(self, destination: System.Span[int]) -> None:
        """
        Copies the vector to the given Span{Byte}.
        The destination span must be at least size Vector{Byte}.Count.
        
        :param destination: The destination span which the values are copied into
        """
        ...

    @typing.overload
    def CopyTo(self, destination: System.Span[System_Numerics_Vector_T]) -> None:
        """
        Copies the vector to the given Span{T}.
        The destination span must be at least size Count.
        
        :param destination: The destination span which the values are copied into
        """
        ...

    @typing.overload
    def CopyTo(self, destination: typing.List[System_Numerics_Vector_T]) -> None:
        """
        Copies the vector to the given destination array.
        The destination array must be at least size Count.
        
        :param destination: The destination array which the values are copied into
        """
        ...

    @typing.overload
    def CopyTo(self, destination: typing.List[System_Numerics_Vector_T], startIndex: int) -> None:
        """
        Copies the vector to the given destination array.
        The destination array must be at least size Count.
        
        :param destination: The destination array which the values are copied into
        :param startIndex: The index to start copying to
        """
        ...

    def __getitem__(self, index: int) -> System_Numerics_Vector_T:
        """Returns the element at the given index."""
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        """
        Returns a boolean indicating whether the given Object is equal to this vector instance.
        
        :param obj: The Object to compare against.
        :returns: True if the Object is equal to this vector; False otherwise.
        """
        ...

    @typing.overload
    def Equals(self, other: System.Numerics.Vector[System_Numerics_Vector_T]) -> bool:
        """
        Returns a boolean indicating whether the given vector is equal to this vector instance.
        
        :param other: The vector to compare this instance to.
        :returns: True if the other vector is equal to this instance; False otherwise.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Returns the hash code for this instance.
        
        :returns: The hash code.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        """
        Returns a String representing this vector.
        
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str) -> str:
        """
        Returns a String representing this vector, using the specified format string to format individual elements.
        
        :param format: The format of individual elements.
        :returns: The string representation.
        """
        ...

    @typing.overload
    def ToString(self, format: str, formatProvider: System.IFormatProvider) -> str:
        """
        Returns a String representing this vector, using the specified format string to format individual elements and the given IFormatProvider.
        
        :param format: The format of individual elements.
        :param formatProvider: The format provider to use when formatting elements.
        :returns: The string representation.
        """
        ...

    @typing.overload
    def TryCopyTo(self, destination: System.Span[int]) -> bool:
        """
        Attempts to copy the vector to the given Span{Byte}.
        The destination span must be at least size Vector{Byte}.Count.
        
        :param destination: The destination span which the values are copied into
        :returns: True if the source vector was successfully copied to . False if  is not large enough to hold the source vector.
        """
        ...

    @typing.overload
    def TryCopyTo(self, destination: System.Span[System_Numerics_Vector_T]) -> bool:
        """
        Attempts to copy the vector to the given Span{T}.
        The destination span must be at least size Count.
        
        :param destination: The destination span which the values are copied into
        :returns: True if the source vector was successfully copied to . False if  is not large enough to hold the source vector.
        """
        ...


