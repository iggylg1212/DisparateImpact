function f_sum = objectiveFun(inParam)
global B W a
 p = inParam(1);
 q = inParam(2);

for i=1:(W+1)
  alpha = (a*B*(i-1))/((1-a)*B+W);
  f_xy(i) = -1*(1-binocdf(alpha,B,p))*(binopdf((i-1),W,q)); 
end
f_sum = sum(f_xy);
display(f_sum)
end
