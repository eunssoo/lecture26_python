# 1 math 모듈 전체를 가져온다.
import math

# 모듈 전체를 가져왔으므로 math.pi 형태로 사용
print(math.pi)

# 2 math 모듈을 m이라는 이름으로 줄여서 가져온다.
import math as m

# math 대신 별칭 m을 사용
print(m.pi)

# 3 math 모듈에서 pi만 가져온다.
from math import pi

# pi만 가져왔으므로 모듈명 없이 바로 사용
print(pi)

# 4 math 모듈에서 pi를 가져오되 p라는 이름으로 바꾼다.
from math import pi as p

# pi 대신 별칭 p를 사용
print(p)