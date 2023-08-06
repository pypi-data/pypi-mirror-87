# Copyright (c) 2020, Manfred Moitzi
# License: MIT License

from pathlib import Path
import math
import ezdxf

DIR = Path('~/Desktop/Outbox').expanduser()

doc = ezdxf.new()
msp = doc.modelspace()

ellipse = msp.add_ellipse(
    center=(0, 0),
    major_axis=(1, 0),
    ratio=0.5,
    start_param=0,
    end_param=math.tau,
    dxfattribs={'layer': 'ellipse'},
)

spline = ellipse.to_spline(replace=False, layout=msp)
spline.dxf.layer = 'B-spline'
spline.dxf.color = 1
doc.set_modelspace_vport(2)

doc.saveas(DIR / 'spline_from_ellipse.dxf')
