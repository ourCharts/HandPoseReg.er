## HandPoseReg
Regcognize some gesture to control your PC.👌
### Environment
In order to build the environment, run
```python
pip install -r requirements.txt
```
### getdata.py
Run getdata.py to get some training samples.<br>
Press "s" to start recording your gesture.<br>
Press "q" to quit.
### genLabel.py
Run genLabel.py to generate labels for the images in data folder.
### train.py
Run train.py to train the model.
### How to control the position of roi(the green region)?
| key  | operation  |
| ---- | ---------- |
| j    | move left  |
| l    | move right |
| i    | move up    |
| k    | move down  |