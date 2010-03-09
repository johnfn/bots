def split(str):
    while str.find("  ") != -1: str.replace("  ", " ")
    

    str = str[1:-1]
    str = " " + str + " "
        
    depth = [0]*len(str)
    parens = 0
    for i, letter in enumerate(str):
        if letter == '(': parens += 1
        if letter == ')': parens -= 1
            
        if letter==" " and parens==0:
            depth[i] = 0
        else:
            depth[i] = parens+1
    
    print depth
    res = [""]
    for index, i in enumerate(depth):
        if i == 0:
            res.append("")
        else:
            res[-1]+= str[index]
    return res[1:-1]
        
        
def test(case, result):
    print "Testing:", case, ", expecting:", result, "results:", split(case)
    if split(case) == result: return True
    return False

    
if test("0", ["0"]) and test("(1 2 3)", ["1", "2", "3"]) and test("(1 ab 3)",["1", "ab", "3"]) and test("(1 (2 3 4) 3)",["1", "(2 3 4)", "3"]) and test("(progn (set x 0) (set y 0))", ["progn", "(set x 0)", "(set y 0)"]) :
    print "All tests passed!"

    
    
    