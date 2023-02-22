# LeetCode Parser for create directories and files with data

Installation
------------


#### Clone a repository

```
git clone https://github.com/vadushkin/LeetCodeParser.git
```

#### Change a folder

```
cd Parser_for_leetcode
```

#### Venv

Windows:

```shell
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Linux:

```shell
python3 -m venv venv
source .\venv\bin\activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

#### Poetry

```
poetry install
poetry shell
```

#### Create ```.env``` file or delete ```.example``` from ```.env.example```

#### Example to fill in

```dotenv
ABSOLUTE_PATH="Your absolute path"
YOUR_FAVORITE_LANGUAGE=Python3
```

Examples
---------

### You can add a daily task

```shell
python main.py
```

![img_1.png](examples/img1.png)

```v1.py```:

```python
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        pass


def main():
    s = Solution()
    print(s.shipWithinDays([1,2,3,4,5,6,7,8,9,10],5))


if __name__ == '__main__':
    main()

"""Tests:
1. 

2. 
"""
```

### You can add several tasks at once

```shell
python main.py 105 42
```

![img.png](examples/img2.png)
