$(function () {
    function PantiltViewModel(parameters) {
        var self = this;

        self.loginState = parameters[0];

        self.stepSize = ko.observable(1);

        self.panValue = ko.observable(0);
        self.tiltValue = ko.observable(0);

        self.requestData = function () {
            OctoPrint.simpleApiGet("octo_pantiltcamera").done(function (
                response
            ) {
                self.panValue(response.panValue);
                self.tiltValue(response.tiltValue);
            });
        };

        self.onStartup = function () {
            var webcam = $("#webcam_container");
            if (webcam === undefined) return;

            webcam.after(self.createPanel());
            self.requestData();
        };

        self.createPanel = function () {
            var panel = $(
                "<!-- ko allowBindings: false --><div id='control_pantilt'></div><!-- /ko -->"
            );
            panel.append($("<h1>Webcam Pan/Tilt</h1>"));

            var buttons = $("<div style='margin-right: 20px'></div>");
            buttons.append(self.createButton("left"));
            buttons.append(self.createButton("right"));
            buttons.append(self.createButton("up"));
            buttons.append(self.createButton("down"));
            panel.append(buttons);

            var values = $("<div></div>");
            values.append(self.createInput("Pan", "panValue"));
            values.append(self.createInput("Tilt", "tiltValue"));
            values.append(
                $(
                    "<button id='control-pantilt-set' class='btn pull-left' data-bind=\"loginState.isUser(), click: function() { $root.sendSetCommand(); }\">Set</button>"
                )
            );
            panel.append(values);

            return panel;
        };

        self.createButton = function (command) {
            var button = $(
                "<button id='control-pantilt-" +
                    command +
                    "' class='btn box pull-left' data-bind=\"loginState.isUser(), click: function() { $root.sendCommand('" +
                    command +
                    "'); }\"></button>"
            );
            button.append($("<i class='icon-arrow-" + command + "'></i>"));
            return button;
        };

        self.createInput = function (name, variable) {
            var div = $(
                "<div class='pull-left' style='margin-right: 10px'></div>"
            );
            div.append(document.createTextNode(name + ": "));
            div.append(
                $(
                    "<input type='number' style='width: 60px' data-bind='value: " +
                        variable +
                        "'>"
                )
            );

            return div;
        };

        self.sendSetCommand = function () {
            OctoPrint.simpleApiCommand("octo_pantiltcamera", "set", {
                panValue: self.panValue(),
                tiltValue: self.tiltValue(),
            }).done(self.requestData);
        };
        self.sendCommand = function (command) {
            OctoPrint.simpleApiCommand("octo_pantiltcamera", command, {
                stepSize: self.stepSize(),
            }).done(self.requestData);
        };
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        PantiltViewModel,
        ["loginStateViewModel"],
        ["#control_pantilt"],
    ]);
});
