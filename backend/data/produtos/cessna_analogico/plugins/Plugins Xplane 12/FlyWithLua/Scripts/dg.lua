dataref("dg", "sim/cockpit/gyros/dg_drift_vac_deg", "writable")



--How many degrees should the dg jump each time if your spinning fast?
dgFastDegrees = 3 


--How many spins per second (or button presses per second) is considered FAST?
dgFastTurnsPerSecond = 12


--You shouldnt need to change anything below-----------------------------------

--dgTurnTimes is used for both dg and dg2 to store times since each turn
dgTurnTimes = {}
dgNumberUpTurns = 1
dgNumberDownTurns = 1



local i = 1
local p = 1

for i = 1, dgFastTurnsPerSecond do
	dgTurnTimes[i]=1
end

-------------------------------------------------------------------
function dgIncrement()
dgNumberDownTurns = 1
local TimeNow = os.clock()
dgTurnTimes[dgNumberUpTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, dgFastTurnsPerSecond do

	if (dgTurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

dgNumberUpTurns = dgNumberUpTurns + 1
if dgNumberUpTurns  > dgFastTurnsPerSecond then
	dgNumberUpTurns = 1
end

if ItsFast == 1 then
dg = dg + dgFastDegrees
else
dg = dg + 1
end

end

-------------------------------------------------------------------------------------------
function dgDecrement()
dgNumberUpTurns = 1
local TimeNow = os.clock()
dgTurnTimes[dgNumberDownTurns] = TimeNow

local i = 1
local ItsFast = 1

for i = 1, dgFastTurnsPerSecond do

	if (dgTurnTimes[i] + 1 >= TimeNow) and (ItsFast == 1) then
		ItsFast = 1
	else
		ItsFast = 0
	end
end

dgNumberDownTurns = dgNumberDownTurns + 1
if dgNumberDownTurns  > dgFastTurnsPerSecond then
	dgNumberDownTurns = 1
end

if ItsFast == 1 then
dg = dg - dgFastDegrees
else
dg = dg - 1
end

end
----------------------------------




create_command("MFSim/custom/dgup","Use Rotary to increase dg","dgIncrement()", " ", "dg = dg % 360 ")
create_command("MFSim/custom/dgdn","Use Rotary to decrease dg","dgDecrement()", " ", "dg = dg % 360 ")

