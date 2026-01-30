dataref("CDI1", "sim/cockpit/radios/nav1_obs_degm", "writable")



--How many degrees should the CDI jump each time if your spinning fast?
CDIFastDegrees = 3 


--How many spins per second (or button presses per second) is considered FAST?
CDIFastTurnsPerSecond = 12


--You shouldnt need to change anything below-----------------------------------

--CDI1TurnTimes is used for both CDI1 and CDI2 to store times since each turn
CDI1TurnTimes = {}
CDI1NumberUpTurns = 1
CDI1NumberDownTurns = 1



local i = 1
local p = 1

for i = 1, CDIFastTurnsPerSecond do
	CDI1TurnTimes[i]=1
end

-------------------------------------------------------------------
function CDI1Increment()
CDI1NumberDownTurns = 1
local TimeNow = os.clock()
CDI1TurnTimes[CDI1NumberUpTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, CDIFastTurnsPerSecond do

	if (CDI1TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

CDI1NumberUpTurns = CDI1NumberUpTurns + 1
if CDI1NumberUpTurns  > CDIFastTurnsPerSecond then
	CDI1NumberUpTurns = 1
end

if ItsFast == 1 then
CDI1 = CDI1 + CDIFastDegrees
else
CDI1 = CDI1 + 1
end

end

-------------------------------------------------------------------------------------------
function CDI1Decrement()
CDI1NumberUpTurns = 1
local TimeNow = os.clock()
CDI1TurnTimes[CDI1NumberDownTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, CDIFastTurnsPerSecond do

	if (CDI1TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

CDI1NumberDownTurns = CDI1NumberDownTurns + 1
if CDI1NumberDownTurns  > CDIFastTurnsPerSecond then
	CDI1NumberDownTurns = 1
end

if ItsFast == 1 then
CDI1 = CDI1 - CDIFastDegrees
else
CDI1 = CDI1 - 1
end

end
----------------------------------




create_command("MFSim/custom/CDIup","Use Rotary to increase CDI1","CDI1Increment()", " ", "CDI1 = CDI1 % 360 ")
create_command("MFSim/custom/CDIdn","Use Rotary to decrease CDI1","CDI1Decrement()", " ", "CDI1 = CDI1 % 360 ")

