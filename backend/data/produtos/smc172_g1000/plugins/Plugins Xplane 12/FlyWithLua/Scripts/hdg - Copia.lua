dataref("HDG1", "sim/cockpit/autopilot/heading", "writable")



--How many degrees should the HDG jump each time if your spinning fast?
HDGFastDegrees = 3 


--How many spins per second (or button presses per second) is considered FAST?
HDGFastTurnsPerSecond = 12


--You shouldnt need to change anything below-----------------------------------

--HDG1TurnTimes is used for both HDG1 and HDG2 to store times since each turn
HDG1TurnTimes = {}
HDG1NumberUpTurns = 1
HDG1NumberDownTurns = 1



local i = 1
local p = 1

for i = 1, HDGFastTurnsPerSecond do
	HDG1TurnTimes[i]=1
end

-------------------------------------------------------------------
function HDG1Increment()
HDG1NumberDownTurns = 1
local TimeNow = os.clock()
HDG1TurnTimes[HDG1NumberUpTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, HDGFastTurnsPerSecond do

	if (HDG1TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

HDG1NumberUpTurns = HDG1NumberUpTurns + 1
if HDG1NumberUpTurns  > HDGFastTurnsPerSecond then
	HDG1NumberUpTurns = 1
end

if ItsFast == 1 then
HDG1 = HDG1 + HDGFastDegrees
else
HDG1 = HDG1 + 0.5
end

end

-------------------------------------------------------------------------------------------
function HDG1Decrement()
HDG1NumberUpTurns = 1
local TimeNow = os.clock()
HDG1TurnTimes[HDG1NumberDownTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, HDGFastTurnsPerSecond do

	if (HDG1TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

HDG1NumberDownTurns = HDG1NumberDownTurns + 1
if HDG1NumberDownTurns  > HDGFastTurnsPerSecond then
	HDG1NumberDownTurns = 1
end

if ItsFast == 1 then
HDG1 = HDG1 - HDGFastDegrees
else
HDG1 = HDG1 - 0.5
end

end
----------------------------------




create_command("MFSim/custom/hdgup","Use Rotary to increase HDG1","HDG1Increment()", " ", "HDG1 = HDG1 % 360 ")
create_command("MFSim/custom/hdgdn","Use Rotary to decrease HDG1","HDG1Decrement()", " ", "HDG1 = HDG1 % 360 ")

