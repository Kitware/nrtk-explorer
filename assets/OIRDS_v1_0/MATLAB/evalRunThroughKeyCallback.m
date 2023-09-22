function evalRunThroughKeyCallback(src, evnt)
% This is a keystroke callback so users can cycle through targets
% when input is waiting on the current axis.  This function only cares
% about 'n' key for NEXT target and 'p' key for previous target
%
% Arguments:
% src - The source of the call back event (ignored)
% evnt - The actual key event
%
    userData = struct('Action', evnt.Character);
    set(gcf, 'UserData', userData);
    
    if strcmp(evnt.Character, 'n')
        delete(gca);
    end 
    
    if strcmp(evnt.Character, 'p')
       delete(gca); 
    end
    
end