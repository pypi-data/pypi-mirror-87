import pytest
import os
import bagheera.main as main
import itertools

fdescs_old = os.walk(os.path.join("test","errors"))
next(fdescs_old)

def fdesc2id(fdesc):
    path, dirs, files = fdesc
    return path

fdescs,id_old = itertools.tee(fdescs_old)
ids = map(fdesc2id,id_old)


@pytest.mark.parametrize('fdesc', fdescs, ids=ids)
def test_errors(fdesc):
    path, dirs, files = fdesc
    assert len(dirs) == 0
    parsed = None
    parsed_ast = None
    ast = None
    expected = None
    for filename in files:
        if filename.endswith(".b"):
            try:
                main.parse(os.path.join(path,filename))
            except Exception as e:
                parsed = str(e)
            else:
                assert False
        elif filename.endswith(".out"):
            with open(os.path.join(path,filename)) as f:
                expected = f.read()
    assert parsed == expected