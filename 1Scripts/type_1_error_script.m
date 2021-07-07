global B W a
B = 123;
W = 18606;
a = .5;

x0 = [0.1,0.2]; 
min_bound = [0 0];
max_bound = [1 1];
[x, fval] = patternsearch(@objectiveFun,x0,[],[],[],[],min_bound,max_bound,@constraintsFun)




