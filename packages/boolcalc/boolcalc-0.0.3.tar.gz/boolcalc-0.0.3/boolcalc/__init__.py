class ArrayListStack:
    def __init__(self):
        self.s = []

    def isEmpty(self):
        return len(self.s) == 0

    def size(self):
        return len(self.s)

    def push(self, e):
        self.s.append(e)

    def peek(self):
        return self.s[-1]

    def pop(self):
        return self.s.pop()


def chackParenthesis(l=[]):
    stack = ArrayListStack()
    for s in l:
        if(s == "("):
            stack.push(s)
        elif (s == ")"):
            if(not stack.isEmpty()):
                stack.pop()
            else:
                return False
    return stack.isEmpty()


def infix_to_postfix(infix="T ^ F <--> ( T --> F v ( F ^ T ) )".split(" ")):
    if(not chackParenthesis(infix)):
        return "Invalid Parenthesis"

    def get_out_val(s):
        ind = operator.index(s)
        return out_stack_val[ind]

    def get_in_val(s):
        ind = operator.index(s)
        return in_stack_val[ind]

    stack = ArrayListStack()
    operator = ["^", "v", "-->", "<-->", "~", "(", ")"]
    in_stack_val = [10, 10, 10, 10, 10, 0]
    out_stack_val = [10, 10, 10, 10, 10, 100, 1]
    postfix = []
    for s in infix:
        if(not s in operator):
            postfix.append(s)
        else:
            point = get_out_val(s)
            while(not stack.isEmpty() and get_in_val(stack.peek()) >= point):
                postfix.append(stack.pop())
            if(s == ")"):
                stack.pop()
            else:
                stack.push(s)
    while(not stack.isEmpty()):
        postfix.append(stack.pop())
    return postfix


def cal_logic(a, b, c):
    if b == "-->":
        if (a == "T" or a == True) and (c == "F" or c == False):
            return "F"
        else:
            return "T"
    elif b == "<-->":
        if (a == "T" or a == True) and (c == "T" or c == True):
            return "T"
        elif (a == "F" or a == False) and (c == "F" or c == False):
            return "T"
        else:
            return "F"
    elif b == "v":
        if (a == "F" or a == False) and (c == "F" or c == False):
            return "F"
        else:
            return "T"
    elif b == "^":
        if (a == "T" or a == True) and (c == "T" or c == True):
            return "T"
        else:
            return "F"


class Node:
    def __init__(self, e, l, r):
        self.element = e
        self.left = l
        self.right = r

    def isLeaf(self):
        return not self.left and not self.right


class ExpressionTree:
    def __init__(self, infix="T ^ T <--> ( T --> F v ( T ^ T ) )".split(" ")):
        postfix = infix_to_postfix(infix)
        if(postfix == "Invalid Parenthesis"):
            raise ArithmeticError("คนไรใส่วงเล็บผิด")
        operator = ["^", "v", "-->", "<-->", "~", "(", ")"]
        s = ArrayListStack()
        for e in postfix:
            if(not e in operator):
                s.push(Node(e, None, None))
            else:
                right = s.pop()
                left = s.pop()
                s.push(Node(e, left, right))
        self.root = s.pop()

    def num_nodes(self, r=Node(Node, None, None)):
        if(not r):
            return 0
        return 1 + self.num_nodes(r.left) + self.num_nodes(r.right)

    def eval(self):
        return self.__eval__(self.root)

    def __eval__(self, r=Node(None, None, None)):
        if(not r):
            return
        if(r.isLeaf()):
            return r.element
        bool_left = self.__eval__(r.left)
        bool_right = self.__eval__(r.right)
        k = cal_logic(bool_left, r.element, bool_right)
        if(k == "T"):
            return True
        elif(k == "F"):
            return False
        else:
            return "Something went wrong ..."


def calculate(infix=[]):
    postfix = infix_to_postfix(infix)
    ex = ExpressionTree(postfix)
    return ex.eval()
