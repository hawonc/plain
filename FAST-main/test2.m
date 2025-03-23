BA =  UnitConversionPkg.ConvLength([    0;     0; 22000; 22000;  0], "ft", "m");
EA =  UnitConversionPkg.ConvLength([    0; 22000; 22000;  0;  0], "ft", "m");

EngineType = "Turbofan";
Passengers = 100;
Range = 703;

[Aircraft] = testFunction(EngineType,Passengers,Range,BA,EA);