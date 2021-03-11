from ...utils.constants import Icon
import os

print(Icon.png('previous'))
print(os.path.exists(Icon.png('previous')))
