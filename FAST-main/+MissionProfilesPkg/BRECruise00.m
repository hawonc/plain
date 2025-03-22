function [Aircraft] = BRECruise00(Aircraft)
%
% [Aircraft] = BRECruise00(Aircraft)
% written by Paul Mokotoff, prmoko@umich.edu
% last updated: 26 mar 2024
%
% Fly the entire mission using only the Breguet Range-based cruise segment
% (see below) with no reserves.
%
% mission 1: 1,650 nmi range                 
%
% ___________________________________________
%
%
% INPUTS:
%     Aircraft - aircraft structure (without a mission profile).
%                size/type/units: 1-by-1 / struct / []
%
% OUTPUTS:
%     Aircraft - aircraft structure (with    a mission profile).
%                size/type/units: 1-by-1 / struct / []
%


%% DEFINE THE MISSION TARGETS %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% define the targets (in m or min)
Mission.Target.Valu = UnitConversionPkg.ConvLength(1650, "naut mi", "m");

% define the target types ("Dist" or "Time")
Mission.Target.Type = "Dist";


%% DEFINE THE MISSION SEGMENTS %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% define the segments
Mission.Segs = "CruiseBRE";

% define the mission id (segments in same mission must be consecutive)
Mission.ID   = 1;

% define the starting/ending altitudes (in m)
Mission.AltBeg = UnitConversionPkg.ConvLength(35000, "ft", "m");
Mission.AltEnd = UnitConversionPkg.ConvLength(35000, "ft", "m");

% define the climb rate (in m/s)
Mission.ClbRate =  NaN;

% define the starting/ending speeds (in m/s or mach)
Mission.VelBeg = UnitConversionPkg.ConvVel(460, "kts", "m/s");
Mission.VelEnd = UnitConversionPkg.ConvVel(460, "kts", "m/s");

% define the speed types (either "TAS", "EAS", or "Mach")
Mission.TypeBeg = "TAS";
Mission.TypeEnd = "TAS";


%% REMEMBER THE MISSION PROFILE %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% save the information
Aircraft.Mission.Profile = Mission;

% ----------------------------------------------------------

end