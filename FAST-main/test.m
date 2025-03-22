InputAircraft = AircraftSpecsPkg.Example;
InputMission = @MissionProfilesPkg.TurbopropMission02;



[Aircraft,MissionHistory] = Main(InputAircraft,InputMission);

%%
disp(Aircraft.Specs.Weight);