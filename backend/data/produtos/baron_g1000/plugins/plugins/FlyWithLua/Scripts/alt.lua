dataref("ALT1", "sim/cockpit/misc/barometer_setting", "writable")



--How many degrees should the ALT jump each time if your spinning fast?
ALTFastDegrees = 0.06


--How many spins per second (or button presses per second) is considered FAST?
ALTFastTurnsPerSecond = 12


--You shouldnt need to change anything below-----------------------------------

--ALT1TurnTimes is used for both ALT1 and ALT1 to store times since each turn
ALT1TurnTimes = {}
ALT1NumberUpTurns = 1
ALT1NumberDownTurns = 1



local i = 1
local p = 1

for i = 1, ALTFastTurnsPerSecond do
	ALT1TurnTimes[i]=1
end

-------------------------------------------------------------------
function ALT1Increment()
ALT1NumberDownTurns = 1
local TimeNow = os.clock()
ALT1TurnTimes[ALT1NumberUpTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, ALTFastTurnsPerSecond do

	if (ALT1TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

ALT1NumberUpTurns = ALT1NumberUpTurns + 1
if ALT1NumberUpTurns  > ALTFastTurnsPerSecond then
	ALT1NumberUpTurns = 1
end

if ItsFast == 1 then
ALT1 = ALT1 + ALTFastDegrees
else
ALT1 = ALT1 + 0.01
end

end

-------------------------------------------------------------------------------------------
function ALT1Decrement()
ALT1NumberUpTurns = 1
local TimeNow = os.clock()
ALT1TurnTimes[ALT1NumberDownTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, ALTFastTurnsPerSecond do

	if (ALT1TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

ALT1NumberDownTurns = ALT1NumberDownTurns + 1
if ALT1NumberDownTurns  > ALTFastTurnsPerSecond then
	ALT1NumberDownTurns = 1
end

if ItsFast == 1 then
ALT1 = ALT1 - ALTFastDegrees
else
ALT1 = ALT1 - 0.01
end

end
----------------------------------




create_command("MFSim/custom/ALTup","Use Rotary to increase ALT1","ALT1Increment()", " ", "ALT1 = ALT1 % 360 ")
create_command("MFSim/custom/ALTdn","Use Rotary to decrease ALT1","ALT1Decrement()", " ", "ALT1 = ALT1 % 360 ")

