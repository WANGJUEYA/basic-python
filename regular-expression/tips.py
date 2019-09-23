import re


class Pattern:

    def __init__(self, regexp=".", demo=None, remark="remark"):
        if demo is None:
            demo = ["demo"]
        self.regexp = regexp
        self.demo = demo
        self.remark = remark

    def findall(self):
        for item in self.demo:
            print(item + "==>", end="\t")
            print(re.findall(self.regexp, item))
        print()


patterns = [
    Pattern("^[0-9]*$", ["123", "1fs"], "数字"),
    Pattern("^\d{3,}$", ["12", "123"], "n位的数字"),
    Pattern("^\d{2,}$", ["12", "123"], "至少n位的数字"),
    Pattern("^\d{5,7}$", ["12", "123"], "m-n位的数字"),
    Pattern("^(0|[1-9][0-9]*)$", ["12", "123"], "零和非零开头的数字"),
    Pattern("^([1-9][0-9]*)+(.[0-9]{1,2})?$", ["12", "123"], "非零开头的最多带两位小数的数字"),
    Pattern("^(\-)?\d+(\.\d{1,2})?$", ["12", "123"], "带1-2位小数的正数或负数")
]

if __name__ == "__main__":
    for value in patterns:
        print(value.remark)
        value.findall()
