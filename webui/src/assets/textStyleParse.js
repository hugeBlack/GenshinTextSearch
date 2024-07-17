export class MyDomElement {
    constructor() {
        this.tagName = null;
        this.tagValue = {};
        this.children = [];
    }
}

// 目标是建立一棵dom树，函数返回以自己为root的dom树，以及自己的结尾位置，对每一行处理
function closedTagParser(text, startIndex) {
    const ans = new MyDomElement();
    let endIndex = text.length;
    // 下一个要读取的字符i
    let lastIndex = startIndex;
    let tagName = '';
    let tagValue = '';

    // 先读取标签, 找到起始标签末尾
    let tagEnded = false;
    if (text[startIndex] === '<') {
        let tagNameEnded = false;
        for (let i = startIndex + 1; i < endIndex; i++) {
            if (text[i] === '>') {
                lastIndex = i + 1;
                tagEnded = true;
                break;
            } else if (!tagNameEnded && text[i] === '=') {
                tagNameEnded = true;
            } else {
                if (!tagNameEnded) {
                    tagName += text[i];
                } else {
                    tagValue += text[i];
                }
            }
        }
    } else {
        // 如果开始不是'<'，则说明第一个元素是一个text类型，要一直读到尾部
        // 好像没什么要特殊处理的？
        tagEnded = true;
    }

    if (!tagEnded) {
        throw new Error(`Tag Not Ended at position ${startIndex}`);
    }

    ans.tagName = tagName;
    ans.tagValue = tagValue;

    // 开始扫描后续内容
    // 遇到<xxx 而不是</xxx 则说明遇到了新元素，要进行递归，把当前读到的元素写到ans里

    for (let i = lastIndex; i < endIndex; i++) {
        if (text[i] === '<') {
            if (i !== endIndex - 1) {
                if (text[i + 1] !== '/') {
                    // 遇到新元素了！
                    ans.children.push(text.substring(lastIndex, i));
                    const [child, childEndIndex] = closedTagParser(text, i);
                    ans.children.push(child);
                    i = childEndIndex;
                    lastIndex = childEndIndex + 1;
                } else {
                    // 遇到同级tag的结尾，检查下是否和自己的tagName相符
                    if (tagName === '') {
                        throw new Error("String tag should NOT have tail tag!");
                    }
                    if (i + tagName.length + 2 > endIndex || text.substring(i + 2, i + 3 + tagName.length) !== tagName + '>') {
                        throw new Error(`Tag head and Tail Not Match at ${i}`);
                    }
                    // 可以结束了
                    ans.children.push(text.substring(lastIndex, i));
                    return [ans, i + 2 + tagName.length];
                }
            }
        }
    }

    // 到头了tag还没结束，没提前返回?，检查是否为文本类型，是的话就正常，否则报错
    if (tagName === "") {
        ans.children.push(text.substring(lastIndex, text.length));
        return [ans, endIndex - 1];
    } else {
        throw new Error("Tag Not Closed!");
    }
}

export function parse(text) {
    if (!text || text.length === 0) {
        return [];
    }

    let lastIndex = -1;
    const ans = [];
    const length = text.length;
    while (lastIndex !== length - 1) {
        const [child, newIndex] = closedTagParser(text, lastIndex + 1);
        ans.push(child);
        lastIndex = newIndex;
    }

    return ans;
}