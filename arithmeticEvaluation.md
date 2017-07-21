Plan:
1. Add more test cases - (1) trivial case; (2) verifiable case; (3) random case; (4) large sample case;
2. Iterate new versions - (1) consider operation priority; (2) intelligent parsing;

intelligent parsing: this has been done
operation priority: we need a major modification for the algorithm - (1) left paranthesis should be considered, every time we meet a right paranthesis, we pop the list until we get left paranthesis, then do calculation, then return the value back to the stack; (2) we should define a function called no_parathesis_evaluation, which is to evaluate sub_expressions within a pair of paranthesis.
