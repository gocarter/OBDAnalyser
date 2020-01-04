import pytest


def test_import():
    from obd_analyser.data_parser import ObdRawSession, import_raw_car_scanner_csv, Path
    import sys
    from types import ModuleType, FunctionType
    from gc import get_referents

    # Custom objects know their class.
    # Function objects seem to know way too much, including modules.
    # Exclude modules as well.
    BLACKLIST = type, ModuleType, FunctionType

    def getsize(obj):
        """sum size of object & members."""
        if isinstance(obj, BLACKLIST):
            raise TypeError(
                'getsize() does not take argument of type: ' + str(type(obj)))
        seen_ids = set()
        size = 0
        objects = [obj]
        while objects:
            need_referents = []
            for obj in objects:
                if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                    seen_ids.add(id(obj))
                    size += sys.getsizeof(obj)
                    need_referents.append(obj)
            objects = get_referents(*need_referents)
        return size
    f = Path(".")
    f = f/"tests"/"sample_files"/"2019-10-29 18-11-52.csv"
    assert(Path(f.as_posix()).exists())

    resp = import_raw_car_scanner_csv(f)
    size = getsize(resp)
    print(resp)
