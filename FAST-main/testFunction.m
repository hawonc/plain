function [MTOW,OEW,Fuel,Length,S] = testFunction(EngineType,Passengers,Range,BA,EA)
%% Create Aircraft
Aircraft = AircraftSpecsPkg.Example;


%% Define User Inputs

Aircraft.Specs.TLAR.Class = EngineType;
Aircraft.Specs.TLAR.MaxPax = Passengers;
Aircraft.Specs.Performance.Range = Range;

%%
% call pre-specprocessing, it will fill in unspecified fields with NaNs if the user forgets one
Aircraft = DataStructPkg.PreSpecProcessing(Aircraft);

% check that an analysis type was provided
if (isnan(Aircraft.Settings.Analysis.Type))
    
    % assume on-design
    warning("WARNING - Main: Analysis type not provided. Assuming on-design (+1).");
    
    % set analysis type to be on-design
    Aircraft.Settings.Analysis.Type = +1;
    
end

% if on-design, use regressions/projections to obtain more knowledge about the aircraft
if (Aircraft.Settings.Analysis.Type > 0)
    Aircraft = DataStructPkg.SpecProcessing(Aircraft);
end

% create the propulsion architecture
Aircraft = PropulsionPkg.CreatePropArch(Aircraft);

% identify any parallel connections (for propulsion analysis)
Aircraft = PropulsionPkg.PropArchConnections(Aircraft);


%% USER-SPECIFIED MISSION PROFILE %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

switch 2
    case 1
        warning("A user-specified mission was not provided. As a default, FAST will use a notional mission parameterized by the input aircraft specifications. Proceed (Y/N)?")
        doc MissionProfilesPkg.NotionalMission00
        proceedvar = input("",'s');
    if strcmpi(proceedvar,"y")
        ProfileFxn = @MissionProfilesPkg.NotionalMission00;
    else
        warning("Aircraft analysis canceled. For more information on specific mission profiles, please see documentation on the MissionProfilesPkg.")
        doc MissionProfilesPkg.README
        return;
    end
end

%% call the respective mission profile function
% define the targets (in m or min)
Mission.Target.Valu = Range;

% define the target types ("Dist" or "Time")
Mission.Target.Type = "Dist";


%% DEFINE THE MISSION SEGMENTS %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% define the segments
Mission.Segs = ["Takeoff"; "Climb"; "Cruise"; "Descent";"Landing"];

% define the mission id (segments in same mission must be consecutive)
Mission.ID   = [        1;       1;        1;        1;  1];

% define the starting/ending altitudes (in m)
Mission.AltBeg =  BA;
Mission.AltEnd =  EA;

% define the climb rate (in m/s)
Mission.ClbRate = [  NaN;   NaN;   NaN;   NaN;   NaN];

% define the starting/ending speeds (in m/s or mach)
Mission.VelBeg =  UnitConversionPkg.ConvVel([    0;   100;   200;   200;   120], "kts", "m/s");
Mission.VelEnd =  UnitConversionPkg.ConvVel([  100;   200;   200;   120;   0], "kts", "m/s");

% define the speed types (either "TAS", "EAS", or "Mach")
Mission.TypeBeg = ["TAS"; "TAS"; "EAS"; "EAS"; "TAS"];
Mission.TypeEnd = ["TAS"; "EAS"; "EAS"; "TAS"; "TAS"];

% save the information
Aircraft.Mission.Profile = Mission;




% process the mission profile
Aircraft = MissionSegsPkg.ProcessProfile(Aircraft);


%% AIRCRAFT ANALYSIS %%
%%%%%%%%%%%%%%%%%%%%%%%

% set the analysis type, done from the aircraft specifications function
%    +1: on -design analysis
%    -1: off-design analysis
Type = Aircraft.Settings.Analysis.Type;

% maximum number of sizing iterations, done from the AircraftSpecsPkg file
MaxIter = Aircraft.Settings.Analysis.MaxIter;

% check if power optimization settings are available
if (isfield(Aircraft, "PowerOpt") == 1)

    % call the optimization routine
    Aircraft = OptimizationPkg.DesOptimize(Aircraft);
     
else
    
    % analyze the aircraft without any optimization
    Aircraft = EAPAnalysis(Aircraft, Type, MaxIter);
    
end


%% MISSION PROFILE PLOTTING %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% plot the results, if desired (if 1, generate plots; if 0, no plotting)
if (Aircraft.Settings.Plotting == 1)
    PlotPkg.PlotMission(Aircraft);
end



% ----------------------------------------------------------

%% MISSION HISTORY TABLE %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% check if a table should be made
if (Aircraft.Settings.Table == 1)
    
    % make the table
    MissionHistory = MissionHistTable(Aircraft);
    
else
    
    % return an empty table
    MissionHistory = table();
    
end

% ----------------------------------------------------------

%% Display
MTOW = Aircraft.Specs.Weight.MTOW;
OEW = Aircraft.Specs.Weight.OEW;
Fuel = Aircraft.Specs.Weight.Fuel;
Length = Aircraft.Geometry.LengthSet;
S = Aircraft.Specs.Aero.S;

end