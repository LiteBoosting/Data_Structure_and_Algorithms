Tasks:
1. Add more test cases - (1.1) trivial case; (1.2) verifiable case; (1.3) random case; (1.4) large sample case;
2. Iterate new versions - (2.1) consider operation priority; (2.2) intelligent parsing;

For (2.1) operation priority: we need a major modification for the algorithm:
1. Left paranthesis should be considered, every time we meet a right paranthesis, we pop the list until we get left paranthesis, then do calculation, then return the value back to the stack;
2. We should define a function called no_parethesis_evaluation, which is to evaluate sub_list within a pair of parantheses.
