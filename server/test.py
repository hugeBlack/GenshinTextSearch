class MyDomElement:
    def __init__(self):
        self.tagName = None
        self.tagValue = {}
        self.children: 'list[MyDomElement | str]' = []


# 目标是建立一棵dom树，函数返回以自己为root的dom树，以及自己的结尾位置，对每一行处理
def closedTagParser(text: str, startIndex: int) -> 'tuple[MyDomElement, int]':
    ans = MyDomElement()
    endIndex = len(text)
    # 下一个要读取的字符i
    lastIndex = startIndex
    tagName = ''
    tagValue = ''
    # 先读取标签

    tagEnded = False
    if text[startIndex] == '<':

        tagNameEnded = False
        # 找到起始标签末尾
        for i in range(startIndex + 1, endIndex):
            if text[i] == '>':
                lastIndex = i + 1
                tagEnded = True
                break
            elif not tagNameEnded and text[i] == '=':
                tagNameEnded = True
            else:
                if not tagNameEnded:
                    tagName += text[i]
                else:
                    tagValue += text[i]
    else:
        # 如果开始不是'<'，则说明第一个元素是一个text类型，要一直读到尾部
        # 好像没什么要特殊处理的？
        tagEnded = True

    if not tagEnded:
        raise Exception("Tag Not Ended at position {}".format(startIndex))

    ans.tagName = tagName
    ans.tagValue = tagValue

    # 开始扫描后续内容
    # 遇到<xxx 而不是</xxx 则说明遇到了新元素，要进行递归，把当前读到的元素写到ans里面

    # 不能用for循环因为python的for循环全是迭代器
    i = lastIndex
    while i < endIndex:
        if text[i] == '<':
            if i != endIndex - 1:
                if text[i + 1] != '/':
                    # 遇到新元素了！
                    ans.children.append(text[lastIndex: i])
                    child, childEndIndex = closedTagParser(text, i)
                    ans.children.append(child)
                    i = childEndIndex
                    lastIndex = childEndIndex + 1
                else:
                    # 遇到同级tag的结尾，检查下是否和自己的tagName相符
                    if tagName == '':
                        raise Exception("String tag should NOT have tail tag!")
                    if i + len(tagName) + 2 > endIndex or text[i + 2: i + 3 + len(tagName)] != tagName + '>':
                        raise Exception("Tag head and Tail Not Match at {}".format(i))
                    # 可以结束了
                    ans.children.append(text[lastIndex:i])
                    return ans, i + 2 + len(tagName)
        else:
            pass

        i += 1

    # 到头了tag还没结束，没提前返回?，检查是否为文本类型，是的话就正常，否则报错
    if tagName == "":
        ans.children.append(text[lastIndex: len(text)])
        return ans, endIndex - 1
    else:
        raise Exception("Tag Not Closed!")


def tagParse(text: str):
    if len(text) == 0:
        return None

    lastIndex = -1
    ans = []
    length = len(text)
    while lastIndex != length - 1:
        child, lastIndex = closedTagParser(text, lastIndex + 1)
        ans.append(child)

    return ans


if __name__ == "__main__":
    t = "<color=nmsl>sd<i>hahahahaha</i>sd</color>sasdadsadsadsas"
    ans1 = tagParse(t)
    print(ans1)

