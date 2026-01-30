dataref("ADF1", "sim/cockpit/radios/adf1_cardinal_dir", "writable")



--How many degrees should the ADF jump each time if your spinning fast?
ADFFastDegrees = 3 


--How many spins per second (or button presses per second) is considered FAST?
ADFFastTurnsPerSecond = 12


--You shouldnt need to change anything below-----------------------------------

--ADF1TurnTimes is used for both ADF1 and ADF1 to store times since each turn
ADF1TurnTimes = {}
ADF1NumberUpTurns = 1
ADF1NumberDownTurns = 1



local i = 1
local p = 1

for i = 1, ADFFastTurnsPerSecond do
	ADF1TurnTimes[i]=1
end

-------------------------------------------------------------------
function ADF1Increment()
ADF1NumberDownTurns = 1
local TimeNow = os.clock()
ADF1TurnTimes[ADF1NumberUpTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, ADFFastTurnsPerSecond do

	if (ADF1TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

ADF1NumberUpTurns = ADF1NumberUpTurns + 1
if ADF1NumberUpTurns  > ADFFastTurnsPerSecond then
	ADF1NumberUpTurns = 1
end

if ItsFast == 1 then
ADF1 = ADF1 + ADFFastDegrees
else
ADF1 = ADF1 + 1
end

end

-------------------------------------------------------------------------------------------
function ADF1Decrement()
ADF1NumberUpTurns = 1
local TimeNow = os.clock()
ADF1TurnTimes[ADF1NumberDownTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, ADFFastTurnsPerSecond do

	if (ADF1TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

ADF1NumberDownTurns = ADF1NumberDownTurns + 1
if ADF1NumberDownTurns  > ADFFastTurnsPerSecond then
	ADF1NumberDownTurns = 1
end

if ItsFast == 1 then
ADF1 = ADF1 - ADFFastDegrees
else
ADF1 = ADF1 - 1
end

end
----------------------------------




create_command("MFSim/custom/ADFup","Use Rotary to increase ADF1","ADF1Increment()", " ", "ADF1 = ADF1 % 360 ")
create_command("MFSim/custom/ADFdn","Use Rotary to decrease ADF1","ADF1Decrement()", " ", "ADF1 = ADF1 % 360 ")

