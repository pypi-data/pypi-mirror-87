import ezdxf
from ezdxf.addons.dxf2code import entities_to_code

NAME = "A_000217"
DXF_FILE = r"D:\Source\dxftest\CADKitSamples\{}.dxf".format(NAME)
# DXF_FILE = r"C:\Users\manfred\Desktop\Outbox\{}.dxf".format(NAME)
SOUCE_CODE_FILE = r"C:\Users\manfred\Desktop\Outbox\{}.py".format(NAME)

doc = ezdxf.readfile(DXF_FILE)
msp = doc.modelspace()

source = entities_to_code(msp)

print('writing ' + SOUCE_CODE_FILE)
with open(SOUCE_CODE_FILE, mode='wt') as f:
    f.write(source.import_str())
    f.write('\n\n')
    f.write(source.code_str())
    f.write('\n')

print('done.')
