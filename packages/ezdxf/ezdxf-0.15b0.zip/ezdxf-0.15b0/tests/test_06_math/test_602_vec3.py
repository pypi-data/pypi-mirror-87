# Copyright (c) 2020, Manfred Moitzi
# License: MIT License
import pytest
import math
# Import from 'ezdxf.math.vector' to test Python implementation
from ezdxf.math.vector import Vec3


def test_init_no_params():
    v = Vec3()
    assert v == (0, 0, 0)
    assert v == Vec3()


def test_init_one_param():
    v = Vec3((2, 3))
    assert v == (2, 3)  # z is 0.

    v = Vec3((2, 3, 4))
    assert v == (2, 3, 4)


def test_init_two_params():
    v = Vec3(1, 2)
    assert v == (1, 2)  # z is 0.

    v = Vec3(5, 6, 7) - Vec3(1, 1, 1)
    assert v == (4, 5, 6)

    v = Vec3.from_deg_angle(0)
    assert v == (1, 0)

    length, angle = 7, 45
    v = Vec3.from_deg_angle(angle, length)
    x = math.cos(math.radians(angle)) * length
    y = math.sin(math.radians(angle)) * length
    assert v == (x, y)


def test_init_three_params():
    v = Vec3(1, 2, 3)
    assert v == (1, 2, 3)


def test_from_angle():
    angle = math.radians(50)
    length = 3.
    assert Vec3.from_angle(angle, length) == (
        math.cos(angle) * length, math.sin(angle) * length, 0)


def test_vector_as_tuple():
    v = Vec3(1, 2, 3)
    assert v[0] == 1
    assert v[1] == 2
    assert v[2] == 3
    assert tuple(v) == (1, 2, 3)

    assert isinstance(v[:2], tuple)
    assert v[:2] == (1, 2)
    assert v[1:] == (2, 3)
    assert isinstance(v.xyz, tuple)
    assert v.xyz == (1, 2, 3)


def test_vec2():
    v = Vec3(1, 2, 3)
    assert len(v) == 3
    v2 = v.vec2
    assert len(v2) == 2
    assert v2 == (1, 2)


def test_round():
    v = Vec3(1.123, 2.123, 3.123)
    v2 = v.round(1)
    assert v2 == (1.1, 2.1, 3.1)


def test_iter():
    assert sum(Vec3(1, 2, 3)) == 6


def test_deep_copy():
    import copy

    v = Vec3(1, 2, 3)
    l1 = [v, v, v]
    l2 = copy.copy(l1)
    assert l2[0] is l2[1]
    assert l2[1] is l2[2]
    assert l2[0] is v

    l3 = copy.deepcopy(l1)
    assert l3[0] is l3[1]
    assert l3[1] is l3[2]
    assert l3[0] is not v


def test_get_angle():
    v = Vec3(3, 3)
    assert math.isclose(v.angle_deg, 45)
    assert math.isclose(v.angle, math.radians(45))


def test_spatial_angle():
    v = Vec3(3, 3, 0)
    assert math.isclose(v.spatial_angle_deg, 45)
    assert math.isclose(v.spatial_angle, math.radians(45))


def test_compare_vectors():
    v1 = Vec3(1, 2, 3)
    assert v1 == (1, 2, 3)
    assert (1, 2, 3) == v1

    v2 = Vec3(2, 3, 4)
    assert v2 > v1
    assert v1 < v2


def test_xy():
    assert Vec3(1, 2, 3).xy == Vec3(1, 2)


def test_is_null():
    v = Vec3()
    assert v.is_null

    v1 = Vec3(23.56678, 56678.56778, 2.56677) * (1.0 / 14.5667)
    v2 = Vec3(23.56678, 56678.56778, 2.56677) / 14.5667
    assert (v2 - v1).is_null

    assert Vec3(0, 0, 0).is_null


def test_bool():
    v = Vec3()
    assert bool(v) is False

    v1 = Vec3(23.56678, 56678.56778, 2.56677) * (1.0 / 14.5667)
    v2 = Vec3(23.56678, 56678.56778, 2.56677) / 14.5667
    result = v2 - v1
    assert bool(result) is False
    # actual precision is abs_tol=1e-9
    assert not Vec3(1e-8, 0, 0).is_null


def test_magnitude():
    v = Vec3(3, 4, 5)
    assert math.isclose(abs(v), 7.0710678118654755)
    assert math.isclose(v.magnitude, 7.0710678118654755)


def test_magnitude_square():
    v = Vec3(3, 4, 5)
    assert math.isclose(v.magnitude_square, 50)


def test_normalize():
    v = Vec3(2, 0, 0)
    assert v.normalize() == (1, 0, 0)


def test_normalize_to_length():
    v = Vec3(2, 0, 0)
    assert v.normalize(4) == (4, 0, 0)


def test_orthogonal_ccw():
    v = Vec3(3, 4)
    assert v.orthogonal() == (-4, 3)


def test_orthogonal_cw():
    v = Vec3(3, 4)
    assert v.orthogonal(False) == (4, -3)


def test_negative():
    v = Vec3(2, 3, 4)
    assert -v == (-2, -3, -4)


def test_add_scalar_type_error():
    with pytest.raises(TypeError):
        Vec3(2, 3, 4) + 3


def test_radd_scalar_type_error():
    with pytest.raises(TypeError):
        3 + Vec3(2, 3, 4)


def test_iadd_scalar_type_error():
    v = Vec3(2, 3, 4)
    with pytest.raises(TypeError):
        v += 3


def test_sub_scalar_type_error():
    with pytest.raises(TypeError):
        Vec3(2, 3, 4) - 3


def test_rsub_scalar_vector_type_error():
    with pytest.raises(TypeError):
        7 - Vec3(2, 3, 4)


def test_isub_scalar_type_error():
    v = Vec3(2, 3, 4)
    with pytest.raises(TypeError):
        v -= 3


def test_add_vector():
    v = Vec3(2, 3, 4)
    assert v + (7, 7, 7) == (9, 10, 11)


def test_iadd_vector():
    v = Vec3(2, 3, 4)
    v += (7, 7, 7)
    assert v == (9, 10, 11)


def test_radd_vector():
    v = Vec3(2, 3, 4)
    assert (7, 7, 7) + v == (9, 10, 11)


def test_sub_vector():
    v = Vec3(2, 3, 4)
    assert v - (7, 7, 7) == (-5, -4, -3)


def test_isub_vector():
    v = Vec3(2, 3, 4)
    v -= (7, 7, 7)
    assert v == (-5, -4, -3)


def test_rsub_vector():
    v = Vec3(2, 3, 4)
    assert (7, 7, 7) - v == (5, 4, 3)


def test_mul_scalar():
    v = Vec3(2, 3, 4)
    assert v * 2 == (4, 6, 8)


def test_imul_scalar():
    v = Vec3(2, 3, 4)
    v *= 2
    assert v == (4, 6, 8)


def test_rmul_scalar():
    v = Vec3(2, 3, 4)
    assert 2 * v == (4, 6, 8)


def test_div_scalar():
    v = Vec3(2, 3, 4)
    assert v / 2 == (1, 1.5, 2)


def test_idiv_scalar():
    v = Vec3(2, 3, 4)
    v /= 2
    assert v == (1, 1.5, 2)


def test_rdiv_scalar():
    v = Vec3(2, 3, 4)
    assert 2 / v == (1, 0.66666666667, 0.5)


def test_dot_product():
    v1 = Vec3(2, 7, 1)
    v2 = Vec3(3, 9, 8)
    assert math.isclose(v1.dot(v2), 77)


def test_angle_deg():
    assert math.isclose(Vec3(0, 1).angle_deg, 90)
    assert math.isclose(Vec3(0, -1).angle_deg, -90)
    assert math.isclose(Vec3(1, 1).angle_deg, 45)
    assert math.isclose(Vec3(-1, 1).angle_deg, 135)


def test_angle_between():
    v1 = Vec3(0, 1)
    v2 = Vec3(1, 1)
    angle = v1.angle_between(v2)
    assert math.isclose(angle, math.pi / 4)
    # reverse order, same result
    angle = v2.angle_between(v1)
    assert math.isclose(angle, math.pi / 4)
    angle = v1.angle_between(Vec3(0, -1))
    assert math.isclose(angle, math.pi)


def test_angle_about():
    extrusion = Vec3(0, 0, 1)
    a = Vec3(1, 0, 0)
    b = Vec3(1, 1, 0)
    assert math.isclose(a.angle_between(b), math.pi / 4)
    assert math.isclose(extrusion.angle_about(a, b), math.pi / 4)

    extrusion = Vec3(0, 0, -1)
    assert math.isclose(a.angle_between(b), math.pi / 4)
    assert math.isclose(extrusion.angle_about(a, b), (-math.pi / 4) % math.tau)

    extrusion = Vec3(0, 0, 1)
    a = Vec3(1, 1, 0)
    b = Vec3(1, 1, 0)
    assert math.isclose(a.angle_between(b), 0, abs_tol=1e-5)
    assert math.isclose(extrusion.angle_about(a, b), 0)

    extrusion = Vec3(0, 1, 0)
    a = Vec3(1, 1, 0)
    b = Vec3(0, 1, -1)
    assert math.isclose(a.angle_between(b), math.pi / 3, abs_tol=1e-5)
    c = a.cross(b)
    assert math.isclose(a.angle_between(b), c.angle_about(a, b))
    assert math.isclose(extrusion.angle_about(a, b), math.pi / 2)


def test_cross_product():
    v1 = Vec3(2, 7, 9)
    v2 = Vec3(3, 9, 1)
    assert v1.cross(v2) == (-74, 25, -3)


def test_rot_z():
    assert Vec3(2, 2, 7).rotate_deg(90) == (-2, 2, 7)


def test_lerp():
    v1 = Vec3(1, 1, 1)
    v2 = Vec3(4, 4, 4)
    assert v1.lerp(v2, .5) == (2.5, 2.5, 2.5)
    assert v1.lerp(v2, 0) == (1, 1, 1)
    assert v1.lerp(v2, 1) == (4, 4, 4)


def test_replace():
    v = Vec3(1, 2, 3)
    assert v.replace(x=7) == (7, 2, 3)
    assert v.replace(y=7) == (1, 7, 3)
    assert v.replace(z=7) == (1, 2, 7)
    assert v.replace(x=7, z=7) == (7, 2, 7)


def test_project():
    v = Vec3(10, 0, 0)
    assert v.project((5, 0, 0)) == (5, 0, 0)
    assert v.project((5, 5, 0)) == (5, 0, 0)
    assert v.project((5, 5, 5)) == (5, 0, 0)

    v = Vec3(10, 10, 0)
    assert v.project((10, 0, 0)) == (5, 5, 0)


def test_vec3_sum():
    assert Vec3.sum([]).is_null is True
    assert Vec3.sum([Vec3(1, 1, 1)]) == (1, 1, 1)
    assert Vec3.sum([Vec3(1, 1, 1), (2, 2, 2)]) == (3, 3, 3)
