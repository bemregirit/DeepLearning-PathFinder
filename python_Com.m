classdef python_Com < matlab.System
    % untitled2 Add summary here
    %
    % This template includes the minimum set of functions required
    % to define a System object.

    % Public, tunable properties
    properties
    
    end

    % Pre-computed constants or internal states
    properties (Access = private)
    x_location = 100;
    y_location = 100;
    end

    methods (Access = protected)
        function setupImpl(obj)
            % Perform one-time calculations, such as computing constants
            
            [result]  = pyrunfile("test.py","returnList");

        end

        function y = stepImpl(obj)
            % Implement algorithm. Calculate y as a function of input u and
            % internal states.
            y = result;
            disp(result)
        end

        function resetImpl(obj)
            % Initialize / reset internal properties
        end
    end
end
