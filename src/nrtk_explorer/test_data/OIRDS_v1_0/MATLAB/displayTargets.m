function displayTargets(excelFile, tab)
% Allows the user to cycle through targets specified in a specific tab
%
% Arguments:
% "excelFile" - The name of the Excel file that contains the target
% information identified in the prevous step
% "tab" - The tab in the Excel File.

    if strcmp(tab, 'Stats')
        FILEPATH_COL = 2;
        FILENAME_COL = 3;
        POLYGON_COL = 8;
        STATS = 1;
    else
        FILENAME_COL = 2;
        POLYGON_COL = 5;
        STATS = 0;
    end

    [num,txt,raw] = xlsread(excelFile, tab);

    imageName = '';

    figure;

    set(gcf, 'KeyPressFcn', @evalRunThroughKeyCallback);

    % set-up dummy user data for the current figure.
    % This is not used, but makes the error checking easier
    userData = struct('Action', 'd');
    set(gcf, 'UserData', userData);

    i = 2;
    while i <= size(raw,1)
        % check if this is a new image file
        if iscellstr(raw(i,FILENAME_COL))
            if STATS
                imageName = strcat(char(raw(i, FILEPATH_COL)), '\', char(raw(i, FILENAME_COL)));
            else
                imageName = char(raw(i,FILENAME_COL));
            end

            display(strcat('Loading image: ', imageName));

            img = imread(imageName);

            imshow(img, 'InitialMagnification', 200);

            setDisplaySettings(img);

            h = gca;

            % Draw the polygon on the image
            rawPoly = raw(i,POLYGON_COL);

            if ~isempty(rawPoly)
                poly = eval(str2mat(rawPoly));

                impoly(h,poly);
            end
            display(strcat('image: ', imageName, ', line num #: ', int2str(i)));
            title(strcat('image: ', imageName, ', line num #: ', int2str(i)), 'Color', [1, 1, 0]);

            waitfor(h);

        end % if iscellStr

        userData = get(gcf, 'UserData');

        if strcmp(userData.Action, 'p')
            % user wants to go to the previous image, decrement the counter
            i = i - 1;
        else
            % user wants to go to the next image, increment the counter
            i = i + 1;
        end % if

    end

end % function - rateSubjectiveValues

