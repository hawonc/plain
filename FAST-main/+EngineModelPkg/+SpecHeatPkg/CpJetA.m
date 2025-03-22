function [heat] = CpJetA(T_low,T_high)
%
% [heat] = CpJetA(T_low,T_high)
% Written by Maxfield Arnson
% Updated 10/9/2023
%
% This function returns the specific heat required to raise vaporized Jet-A
% from T_low to T_high. An S curve was fitted to the data referenced at the
% end of this file.
%
%
% INPUTS:
%
% T_low = lower temperature of Jet A
%       size: scalar double
%
% T_low = higher temperature of Jet A
%       size: scalar double
%
%
% OUTPUTS:
%
% heat = specific heat of required for the desired temperature raise
%       size: scalar double

%% Compute
L = 4600;
k = 1/410;
y = 500;
C = 100;

heat = (T_high*(C+L) + L*log(exp(k*(y-T_high))+1)/k) -(T_low*(C+L) + L*log(exp(k*(y-T_low))+1)/k);

%% Data used for curve fitting (For reference only)
% https://web.stanford.edu/group/haiwanglab...
% /HyChem/approach/Report_Jet_Fuel_Thermochemical_Properties_v6.pdf
% 
% 
% % temp (K)   Cp (cal/mol-K)
% data = [
% 298. 54.325   
%  300. 54.646  
%  400. 70.216  
%  500. 84.305  
%  600. 96.474  
%  700. 106.672 
%  800. 115.244 
%  900. 122.926 
%  1000. 130.845
%  1100. 135.847
%  1200. 140.409
%  1300. 144.555
%  1400. 148.310
%  1500. 151.700
%  1600. 154.750
%  1700. 157.485
%  1800. 159.931
%  1900. 162.115
%  2000. 164.064
%  2100. 165.803
%  2200. 167.361
%  2300. 168.766
%  2400. 170.044
%  2500. 171.224];
% MW = 151.9; % grams per mol of jet A
% 
% temp = data(:,1); cp = data(:,2);
% cp = cp*4.184/MW*1e3;
% p = polyfit(temp,cp,3);
% 
% vec = -400:1:4000;
% 
% 
% scatter(temp,cp)
% hold on
% 
% plot(vec,polyval(p,vec))
% 
% L = 4600;
% k = 1/410;
% y = 500;
% C = 100;
% 
% heat = L./(1+exp(-k.*(vec-y)))+ C;
% 
% plot(vec,heat)

end