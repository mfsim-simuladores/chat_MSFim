dataref("OBS2", "sim/cockpit/radios/nav2_obs_degm", "writable")



--How many degrees should the OBS jump each time if your spinning fast?
OBSFastDegrees = 3 


--How many spins per second (or button presses per second) is considered FAST?
OBSFastTurnsPerSecond = 12


--You shouldnt need to change anything below-----------------------------------

--OBS2TurnTimes is used for both OBS2 and OBS2 to store times since each turn
OBS2TurnTimes = {}
OBS2NumberUpTurns = 1
OBS2NumberDownTurns = 1



local i = 1
local p = 1

for i = 1, OBSFastTurnsPerSecond do
	OBS2TurnTimes[i]=1
end

-------------------------------------------------------------------
function OBS2Increment()
OBS2NumberDownTurns = 1
local TimeNow = os.clock()
OBS2TurnTimes[OBS2NumberUpTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, OBSFastTurnsPerSecond do

	if (OBS2TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

OBS2NumberUpTurns = OBS2NumberUpTurns + 1
if OBS2NumberUpTurns  > OBSFastTurnsPerSecond then
	OBS2NumberUpTurns = 1
end

if ItsFast == 1 then
OBS2 = OBS2 + OBSFastDegrees
else
OBS2 = OBS2 + 0.5
end

end

-------------------------------------------------------------------------------------------
function OBS2Decrement()
OBS2NumberUpTurns = 1
local TimeNow = os.clock()
OBS2TurnTimes[OBS2NumberDownTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, OBSFastTurnsPerSecond do

	if (OBS2TurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

OBS2NumberDownTurns = OBS2NumberDownTurns + 1
if OBS2NumberDownTurns  > OBSFastTurnsPerSecond then
	OBS2NumberDownTurns = 1
end

if ItsFast == 1 then
OBS2 = OBS2 - OBSFastDegrees
else
OBS2 = OBS2 - 0.5
end

end
----------------------------------




create_command("MFSim/custom/OBS2up","Use Rotary to increase OBS2","OBS2Increment()", " ", "OBS2 = OBS2 % 360 ")
create_command("MFSim/custom/OBS2dn","Use Rotary to decrease OBS2","OBS2Decrement()", " ", "OBS2 = OBS2 % 360 ")

