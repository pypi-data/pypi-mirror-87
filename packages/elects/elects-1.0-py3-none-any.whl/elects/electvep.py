def electVolt(curr, res):

    volt = float(curr) * float(res)

    if volt < 1000:
        print(f"Voltage: {volt}V")
    elif volt >= 1000 and volt < 1000_000:
        kvolt = volt / 1000
        print(f"Voltage: {kvolt}KV")
    else:
        mvolt = volt / 1000_000
        print(f"Voltage: {mvolt}MV")


def electPower(curr1, volt1):

    powr = float(curr1) * float(volt1)

    if powr < 1000:
        print(f"Power: {powr}W")
    elif powr >= 1000 and powr < 1000_000:
        kpowr = powr / 1000
        print(f"Power: {kpowr}KW")
    else:
        mpowr = powr / 1000_000
        print(f"Power: {mpowr}MW")


def electPower1(curr2, res1):

    powr1 = float(curr2**2) * float(res1)

    if powr1 < 1000:
        print(f"Power: {powr1}W")
    elif powr1 >= 1000 and powr1 < 1000_000:
        kpowr1 = powr1 / 1000
        print(f"Power: {kpowr1}KW")
    else:
        mpowr1 = powr1 / 1000_000
        print(f"Power: {mpowr1}MW")


def electPower2(volt2, res2):

    powr2 = float(volt2**2) / float(res2)

    if powr2 < 1000:
        print(f"Power: {powr2}W")
    elif powr2 >= 1000 and powr2 < 1000_000:
        kpowr2 = powr2 / 1000
        print(f"Power: {kpowr2}KW")
    else:
        mpowr2 = powr2 / 1000_000
        print(f"Power: {mpowr2}MW")


def electEnergy1(curr3, volt3, t):

    ener1 = float(curr3) * float(volt3) * float(t)

    if ener1 < 1000:
        print(f"Energy: {ener1}J")
    elif ener1 >= 1000 and ener1 < 1000_000:
        kener1 = ener1 / 1000
        print(f"Energy: {kener1}KJ")
    else:
        mener1 = ener1 / 1000_000
        print(f"Energy: {mener1}MJ")


def electEnergy2(curr3, res3, t):

    ener2 = float(curr3**2) * float(res3) * float(t)

    if ener2 < 1000:
        print(f"Energy: {ener2}J")
    elif ener2 >= 1000 and ener2 < 1000_000:
        kener2 = ener2 / 1000
        print(f"Energy: {kener2}KJ")
    else:
        mener2 = ener2 / 1000_000
        print(f"Energy: {mener2}MJ")


def electEnergy3(res3, volt3, t):

    ener3 = float(volt3**2) * float(t) / float(res3)

    if ener3 < 1000:
        print(f"Energy: {ener3}J")
    elif ener3 >= 1000 and ener3 < 1000_000:
        kener3 = ener3 / 1000
        print(f"Energy: {kener3}KJ")
    else:
        mener3 = ener3 / 1000_000
        print(f"Energy: {mener3}MJ")


def electEnergy4(powr3, t):

    ener4 = float(powr3) * float(t)

    if ener4 < 1000:
        print(f"Energy: {ener4}J")
    elif ener4 >= 1000 and ener4 < 1000_000:
        kener4 = ener4 / 1000
        print(f"Energy: {kener4}KJ")
    else:
        mener4 = ener4 / 1000_000
        print(f"Energy: {mener4}MJ")
