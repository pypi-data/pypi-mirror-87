from collections import deque


def infix_to_postfix(infix_input: list) -> list:
    """
    Converts infix expression to postfix.
    Args:
        infix_input(list): infix expression user entered
    """

    # precedence order and associativity helps to determine which
    # expression is needs to be calculated first
    precedence_order = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}
    associativity = {'+': "LR", '-': "LR", '*': "LR", '/': "LR", '^': "RL"}
    # clean the infix expression
    # clean_infix = self._clean_input(infix_input)
    clean_infix = infix_input

    i = 0
    postfix = []
    operators = "+-/*^"
    stack = deque()
    while i < len(clean_infix):

        char = clean_infix[i]
        # print(f"char: {char}")
        # check if char is operator
        if char in operators:
            # check if the stack is empty or the top element is '('
            if len(stack) == 0 or stack[0] == '(':
                # just push the operator into stack
                stack.appendleft(char)
                i += 1
            # otherwise compare the curr char with top of the element
            else:
                # peek the top element
                top_element = stack[0]
                # check for precedence
                # if they have equal precedence
                if precedence_order[char] == precedence_order[top_element]:
                    # check for associativity
                    if associativity[char] == "LR":
                        # pop the top of the stack and add to the postfix
                        popped_element = stack.popleft()
                        postfix.append(popped_element)
                    # if associativity of char is Right to left
                    elif associativity[char] == "RL":
                        # push the new operator to the stack
                        stack.appendleft(char)
                        i += 1
                elif precedence_order[char] > precedence_order[top_element]:
                    # push the char into stack
                    stack.appendleft(char)
                    i += 1
                elif precedence_order[char] < precedence_order[top_element]:
                    # pop the top element
                    popped_element = stack.popleft()
                    postfix.append(popped_element)
        elif char == '(':
            # add it to the stack
            stack.appendleft(char)
            i += 1
        elif char == ')':
            top_element = stack[0]
            while top_element != '(':
                popped_element = stack.popleft()
                postfix.append(popped_element)
                # update the top element
                top_element = stack[0]
            # now we pop opening parenthases and discard it
            stack.popleft()
            i += 1
        # char is operand
        else:
            postfix.append(char)
            i += 1
        #     print(postfix)
        # print(f"stack: {stack}")

    # empty the stack
    if len(stack) > 0:
        for i in range(len(stack)):
            postfix.append(stack.popleft())
    # while len(stack) > 0:
    #     postfix.append(stack.popleft())

    return postfix