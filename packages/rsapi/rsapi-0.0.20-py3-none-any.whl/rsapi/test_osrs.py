import responses
import pytest

import rsapi
import rsapi.osrs


TEST_DATA = """\
1498141,828,11351102
1412883,60,277104
1667382,45,67700
1831076,55,176433
1909176,54,163082
1857378,50,101338
1634834,43,51922
1831798,52,129827
-1,21,5310
73288,96,9873694
1872807,19,4027
-1,23,6591
-1,20,4520
-1,30,14273
-1,31,15243
-1,34,21822
1435551,19,4080
1417780,40,39308
1267203,37,29142
1614597,26,8925
538133,62,355761
1985634,1,0
1440506,9,1000
1665116,1,0
-1,-1
-1,-1
-1,-1
266769,77
70504,13
72338,34
178457,30
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1
-1,-1"""


@pytest.yield_fixture
def mock_hiscores():
    with responses.RequestsMock() as rsps:
        mock_url = f"{rsapi.API_URL}/{rsapi.osrs.HISCORES_PATH}"
        rsps.add(responses.GET, mock_url, body=TEST_DATA, status=200)
        yield rsps


def test_hiscores(mock_hiscores):
    scores = rsapi.osrs.hiscores("jakop")
    assert scores["Overall"]["level"] == 828, "Overall score mismatch"
    assert scores["Overall"]["exp"] == 11351102, "Overall exp mismatch"
    assert scores["Overall"]["rank"] == 1498141, "Overall rank mismatch"
